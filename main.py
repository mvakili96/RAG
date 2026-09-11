#########################################################################################################################################
# 1- Load the document
#########################################################################################################################################
import json
import re
from pathlib import Path

import faiss
import pypdf
import yaml
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
from transformers import GenerationConfig


def find_explicit_sources(question, available_sources):
    # Example: according to "Probabilistic Machine Learning.pdf", what is ...?
    mentioned_names = re.findall(
        r"\baccording to\s+(?:the\s+(?:file|document)\s+)?[\"\u201c']([^\"\u201d']+)[\"\u201d']",
        question,
        flags=re.IGNORECASE
    )

    matched_sources = []

    for mentioned_name in mentioned_names:
        for source in available_sources:
            if mentioned_name == source:
                if source not in matched_sources:
                    matched_sources.append(source)

    return matched_sources


class RAGPipeline:
    def __init__(self, config, pdf_paths):
        self.config = config
        self.pdf_paths = pdf_paths
        self.available_sources = [pdf_path.name for pdf_path in pdf_paths]

        self.documents = self.load_documents()
        self.chunks = self.chunk_documents(self.documents)
        self.source_chunks = {
            source: [
                chunk
                for chunk in self.chunks
                if chunk.metadata["source"] == source
            ]
            for source in self.available_sources
        }
        self.embedding_model = self.create_embedding_model()
        self.source_vector_stores = self.build_dense_indexes()
        self.global_bm25 = self.build_bm25(self.chunks)
        self.subset_bm25_cache = {
            (source,): (chunks, self.build_bm25(chunks))
            for source, chunks in self.source_chunks.items()
        }
        self.llm = self.load_llm()
        self.reranker = None

    def load_documents(self):
        documents = []

        for pdf_path in self.pdf_paths:
            reader = pypdf.PdfReader(pdf_path)

            for page_number, page in enumerate(reader.pages):

                # the following text totally ignores figures. Object type is a string.
                text = page.extract_text() or ""

                doc = Document(
                    page_content=text,
                    metadata={
                        "source": pdf_path.name,
                        "page": page_number + 1
                    }
                )

                documents.append(doc)

        print(200*"#")
        print("DONE with parsing the reference files!")
        print(200*"#")
        return documents

    #########################################################################################################################################
    # 2- Chunk the document
    #########################################################################################################################################
    def chunk_documents(self, documents):
        # LangChain's recursive splitter tries paragraph boundaries first, then progressively smaller separators instead of blindly cutting every N characters.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config["chunking"]["chunk_size"],
            chunk_overlap=self.config["chunking"]["chunk_overlap"],
            add_start_index=self.config["chunking"]["add_start_index"]
        )

        # chunks is a list of chunks. Each chunk has metadata such as page_content, source, page, start_index, and so on.
        # Here, start_index means the index of the first character of this chunk corresponds to character start_index of the original pagetext.
        chunks = splitter.split_documents(documents)

        # This ID is stored in both retrieval systems so the same chunk can be
        # recognized and deduplicated after dense and sparse retrieval.
        for chunk in chunks:
            chunk.metadata["chunk_id"] = (
                f"{chunk.metadata['source']}::"
                f"page={chunk.metadata['page']}::"
                f"start={chunk.metadata['start_index']}"
            )

        return chunks

    #########################################################################################################################################
    # 3- Turn chunks into embeddings
    #########################################################################################################################################
    def create_embedding_model(self):
        embedding_model = HuggingFaceEmbeddings(
            model_name=self.config["embedding"]["model_name"],
            encode_kwargs={
                "normalize_embeddings": self.config["embedding"]["normalize_embeddings"]
            }
        )

        return embedding_model

    """
    Analyze and diagnose embeddings:
    text = chunks[50].page_content
    vector = embedding_model.embed_query(text)

    print(type(vector))
    print("Embedding dimensions:", len(vector))
    print(vector[:10])
    """

    #########################################################################################################################################
    # 4- Build the dense and sparse retrieval indexes
    #########################################################################################################################################
    def tokenize_for_bm25(self, text):
        return re.findall(
            self.config["retrieval"]["bm25_token_pattern"],
            text.lower()
        )

    def build_faiss_vector_store(self, chunks, embedding_dimension=None):
        dense_index_type = self.config["retrieval"]["dense_index_type"]

        if dense_index_type == "flat":
            return FAISS.from_documents(
                documents=chunks,
                embedding=self.embedding_model
            )
        if dense_index_type == "hnsw":
            faiss_index = faiss.IndexHNSWFlat(
                embedding_dimension,
                self.config["retrieval"]["hnsw_m"]
            )
            faiss_index.hnsw.efConstruction = self.config["retrieval"]["hnsw_ef_construction"]
            faiss_index.hnsw.efSearch = self.config["retrieval"]["hnsw_ef_search"]
            vector_store = FAISS(
                embedding_function=self.embedding_model,
                index=faiss_index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )
            vector_store.add_documents(chunks)
            return vector_store

        raise ValueError('retrieval.dense_index_type must be either "flat" or "hnsw".')

    def build_dense_indexes(self):
        # LangChain's vector-store abstraction exists to associate embeddings with their original documents and perform similarity search over them.
        # In the earlier single-query layout:
        # When a source was named, chunks contains only that source. Otherwise, it
        # contains all chunks from all sources in one global FAISS index.
        # Each source has its own FAISS index. Searching every source index and
        # merging the results lets the same pipeline restrict retrieval per query.
        dense_index_type = self.config["retrieval"]["dense_index_type"]
        embedding_dimension = None

        if dense_index_type == "hnsw":
            embedding_dimension = len(
                self.embedding_model.embed_query("FAISS dimension probe")
            )

        source_vector_stores = {}
        for source, chunks in self.source_chunks.items():
            source_vector_stores[source] = self.build_faiss_vector_store(
                chunks,
                embedding_dimension
            )

        print("Dense FAISS index:", dense_index_type)
        return source_vector_stores

    def build_bm25(self, chunks):
        # Unlike a vector store, BM25 indexes tokenized words(so here, by token, we mean a word) rather than embeddings.
        # It is built once during ingestion and reused for every query.
        # bm25_corpus is a list of all chunks, each chunk represented with a list of its words as strings
        bm25_corpus = [self.tokenize_for_bm25(chunk.page_content) for chunk in chunks]
        return BM25Okapi(
            bm25_corpus,
            k1=self.config["retrieval"]["bm25_k1"],
            b=self.config["retrieval"]["bm25_b"],
            epsilon=self.config["retrieval"]["bm25_epsilon"]
        )

    def bm25_for_sources(self, sources):
        source_key = tuple(sorted(sources))

        if len(source_key) == len(self.available_sources):
            return self.chunks, self.global_bm25

        if source_key not in self.subset_bm25_cache:
            chunks = [
                chunk
                for source in source_key
                for chunk in self.source_chunks[source]
            ]
            self.subset_bm25_cache[source_key] = (
                chunks,
                self.build_bm25(chunks)
            )

        return self.subset_bm25_cache[source_key]

    """
    For huge documents, the index can be saved with vector_store.save_local(...),
    then loaded on later runs so the chunks do not need to be embedded again.

    LangChain’s FAISS vector store is like this:
    FAISS Vector Store
    │
    ├── index
    │   ├── vector 0  → [0.12, -0.43, 0.08, ...]
    │   ├── vector 1  → [0.31,  0.17, -0.22, ...]
    │   └── vector 2  → [-0.14, 0.52, 0.09, ...]
    │
    ├── index_to_docstore_id
    │   ├── 0 → "abc123"
    │   ├── 1 → "def456"
    │   └── 2 → "ghi789"
    │
    └── docstore
        ├── "abc123"
        │    ├── page_content: "Machine learning is..."
        │    └── metadata: {page: 1, start_index: 0}
        │
        ├── "def456"
        │    ├── page_content: "Neural networks are..."
        │    └── metadata: {page: 1, start_index: 850}
        │
        └── "ghi789"
             ├── page_content: "Transformers use..."
             └── metadata: {page: 2, start_index: 0}


    To inspect vector store:

    vector = vector_store.index.reconstruct(0)
    print(vector)
    index_to_docstore_id = vector_store.index_to_docstore_id[0]
    print(index_to_docstore_id)
    doc = vector_store.docstore.search(index_to_docstore_id)
    print(doc)

    To inspect bm25_index:

    Following shows all available attributes/methods you can access with bm25_index.something.
    print(dir(bm25_index))

    Following shows a dict for each chunk, with key being the word inside the chunk and value being the frequency of the word inside the chunk
    for freq_dict in bm25_index.doc_freqs:
        print(freq_dict)

    bm25_index.idf["draft"] measures each token’s importance across all chunks.
    idf = Inverse Document Frequency. It measures how rare a word is across your chunks.
    In rank_bm25, roughly:
    IDF(t)= log[(N-df(t)+0.5)/(df(t)+0.5)]
    where:
    N = total number of chunks
    df(t) = number of chunks containing that word
    So:
    word appears in few chunks → high IDF → more informative
    word appears in many chunks → low IDF → less informative

    bm25_index.get_scores(query_tokens) → BM25 score for every chunk for a query.
    rank_bm25.get_scores() effectively scores every chunk in doc_freqs. So it is brute-force over the corpus rather than using an inverted index.
    For each query word and each chunk, BM25 combines:
    score = IDF(q) * TF(q,d)*(k_1+1) / (TF(q,d)+k_1(1-b+b*|d|/avgdl))
    where:
    IDF(q) = how rare the query word is across chunks
    TF(q,d) = how many times it occurs in that chunk
    |d| = chunk length
    avgdl = average chunk length
    Then it adds the scores for all query words. So for a query, it's key/important/rare words already contribute a lot
    to the aggregate score, whereas the common words add only a bit.
    Therefore, LLM for matching is mainly used for extracting synonyms, rather than localizing keywords
    One limitation of BM25 is its unawareness about a combo of keywords like "neural radiance field", even though it
    handles all its rare words.
    """

    #########################################################################################################################################
    # 5- Load a local LLM and expand the query for BM25
    #########################################################################################################################################
    def load_llm(self):
        generation_config = GenerationConfig.from_pretrained(
            self.config["llm"]["model_id"]
        )

        generation_config.max_new_tokens = self.config["llm"]["generation"]["max_new_tokens"]
        generation_config.do_sample = self.config["llm"]["generation"]["do_sample"]

        # These only matter when sampling is enabled
        generation_config.temperature = self.config["llm"]["generation"]["temperature"]
        generation_config.top_p = self.config["llm"]["generation"]["top_p"]
        generation_config.top_k = self.config["llm"]["generation"]["top_k"]

        return HuggingFacePipeline.from_model_id(
            model_id=self.config["llm"]["model_id"],
            task=self.config["llm"]["task"],

            pipeline_kwargs={
                "generation_config": generation_config,
                "return_full_text": self.config["llm"]["return_full_text"],
            },

            device_map=self.config["llm"]["device_map"],
        )

    def keep_conservative_terms(self, values, maximum):
        kept_terms = []
        seen_terms = set()

        if not isinstance(values, list):
            return kept_terms

        for value in values:
            if not isinstance(value, str):
                continue

            term = value.strip()
            normalized_term = term.lower()

            if (
                term
                and len(term) <= self.config["query_expansion"]["max_term_length"]
                and normalized_term not in seen_terms
            ):
                kept_terms.append(term)
                seen_terms.add(normalized_term)

        return kept_terms[:maximum]

    def expand_query(self, query):
        expansion_prompt = self.config["query_expansion"]["prompt"].format(
            query=query,
            max_key_terms=self.config["query_expansion"]["max_key_terms"],
            max_acronyms=self.config["query_expansion"]["max_acronyms"],
            min_variations=self.config["query_expansion"]["min_variations"],
            max_variations=self.config["query_expansion"]["max_variations"]
        )

        expansion_response = self.llm.invoke(
            expansion_prompt,
            pipeline_kwargs={
                "max_new_tokens": self.config["query_expansion"]["max_new_tokens"]
            }
        )
        json_start = expansion_response.find("{")

        try:
            # raw_decode reads the first complete JSON object and ignores any text the
            # LLM may have generated after it.
            parsed_expansion, _ = json.JSONDecoder().raw_decode(
                expansion_response[json_start:]
            ) if json_start != -1 else ({}, 0)
        except json.JSONDecodeError:
            parsed_expansion = {}

        if not isinstance(parsed_expansion, dict):
            parsed_expansion = {}

        query_expansion = {
            "key_terms": self.keep_conservative_terms(
                parsed_expansion.get("key_terms"),
                self.config["query_expansion"]["max_key_terms"]
            ),
            "acronyms": self.keep_conservative_terms(
                parsed_expansion.get("acronyms"),
                self.config["query_expansion"]["max_acronyms"]
            ),
            "variations": self.keep_conservative_terms(
                parsed_expansion.get("variations"),
                self.config["query_expansion"]["max_variations"]
            )
        }

        expanded_terms = (
            query_expansion["key_terms"]
            + query_expansion["acronyms"]
            + query_expansion["variations"]
        )
        expanded_query = " ".join([query, *expanded_terms])

        # print("\nEXPANDED QUERY TERMS")
        # print(json.dumps(query_expansion, indent=2, ensure_ascii=False))
        # print("BM25 query:", expanded_query)

        return query_expansion, expanded_query

    #########################################################################################################################################
    # 6- Retrieve dense and sparse candidates, then merge them
    #########################################################################################################################################
    def selected_sources(self, query):
        explicit_sources = find_explicit_sources(query, self.available_sources)
        return explicit_sources or self.available_sources

    def retrieve_candidates(self, query, expanded_query):
        sources = self.selected_sources(query)
        query_vector = self.embedding_model.embed_query(query)

        # If a source was explicitly named, this searches only its chunks. Otherwise,
        # this searches all chunks from all sources.
        dense_results_with_scores = []
        for source in sources:
            dense_results_with_scores.extend(
                self.source_vector_stores[source].similarity_search_with_score_by_vector(
                    query_vector,
                    k=self.config["retrieval"]["dense_top_k"]
                )
            )
        dense_results_with_scores.sort(key=lambda item: item[1])
        dense_results_with_scores = dense_results_with_scores[
            :self.config["retrieval"]["dense_top_k"]
        ]
        dense_candidate_docs = [doc for doc, _ in dense_results_with_scores]

        bm25_chunks, bm25_index = self.bm25_for_sources(sources)
        bm25_query_tokens = list(
            dict.fromkeys(self.tokenize_for_bm25(expanded_query))
        )
        bm25_scores = bm25_index.get_scores(bm25_query_tokens)
        top_bm25_indices = bm25_scores.argsort()[
            ::-1
        ][:self.config["retrieval"]["bm25_top_k"]]
        bm25_results_with_scores = [
            (bm25_chunks[index], float(bm25_scores[index]))
            for index in top_bm25_indices
            if bm25_scores[index] > self.config["retrieval"]["bm25_min_score"]
        ]
        bm25_candidate_docs = [doc for doc, _ in bm25_results_with_scores]

        """
        print("\nBM25 CANDIDATES")
        for rank, (doc, score) in enumerate(bm25_results_with_scores, start=1):
            print(
                f"{rank}. score={score:.4f} | {doc.metadata['chunk_id']} | "
                f"{doc.page_content[:200].replace(chr(10), ' ')}"
            )

        print("\nDENSE CANDIDATES")
        for rank, (doc, score) in enumerate(dense_results_with_scores, start=1):
            print(
                f"{rank}. distance={score:.4f} | {doc.metadata['chunk_id']} | "
                f"{doc.page_content[:200].replace(chr(10), ' ')}"
            )
        """

        candidate_docs = []
        candidate_methods = {}

        for retrieval_method, retrieved_docs in (
            ("dense", dense_candidate_docs),
            ("BM25", bm25_candidate_docs)
        ):
            for doc in retrieved_docs:
                chunk_id = doc.metadata["chunk_id"]

                if chunk_id not in candidate_methods:
                    candidate_docs.append(doc)
                    candidate_methods[chunk_id] = []

                candidate_methods[chunk_id].append(retrieval_method)

        """
        print("\nMERGED CANDIDATES")
        for rank, doc in enumerate(candidate_docs, start=1):
            methods = ", ".join(candidate_methods[doc.metadata["chunk_id"]])
            print(
                f"{rank}. retrieved_by={methods} | {doc.metadata['chunk_id']} | "
                f"{doc.page_content[:200].replace(chr(10), ' ')}"
            )


        Now you can print the retrieved results using:

        for i, doc in enumerate(dense_candidate_docs):

            print("=" * 80)

            print("RESULT:", i + 1)
            print("PAGE:", doc.metadata["page"])

            print(doc.page_content[:500])


        You can use dense_results_with_scores to get the score/distance of each chunk too:

        for i, (doc, score) in enumerate(dense_results_with_scores):

            print("=" * 80)

            print("Rank:", i + 1)
            print("FAISS distance:", score)
            print("Page:", doc.metadata["page"])
            print(doc.page_content[:300])

        """

        return {
            "selected_sources": sources,
            "dense_results_with_scores": dense_results_with_scores,
            "bm25_results_with_scores": bm25_results_with_scores,
            "candidate_docs": candidate_docs,
            "candidate_methods": candidate_methods,
        }

    #########################################################################################################################################
    # 7- Rerank the n candidates
    #########################################################################################################################################
    def rerank_candidates(self, query, candidate_docs):
        """
        the previous retrieval step is optimized for speed, not perfect relevance. FAISS quickly finds chunks whose embeddings are close to the query, but embedding similarity can still return chunks that are only loosely related.

        Reranking takes those top candidates and uses a stronger/more expensive model to score them more carefully against the actual query.
        """

        if self.reranker is None:
            self.reranker = HuggingFaceCrossEncoder(
                model_name=self.config["reranking"]["model_name"]
            )

        pairs = [
            (query, doc.page_content)
            for doc in candidate_docs
        ]

        rerank_scores = self.reranker.score(pairs)

        scored_docs = list(
            zip(candidate_docs, rerank_scores)
        )

        scored_docs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        reranked_docs = scored_docs[:self.config["reranking"]["final_top_k"]]

        """
        print("\nRERANKED RESULTS")
        for rank, (doc, score) in enumerate(reranked_docs, start=1):
            print(
                f"{rank}. score={score:.4f} | {doc.metadata['chunk_id']} | "
                f"{doc.page_content[:500].replace(chr(10), ' ')}"
            )
        """

        """
        for rank, (doc, score) in enumerate(reranked_docs, start=1):

            print("=" * 80)

            print("Reranked position:", rank)
            print("Reranker score:", score)
            print("Page:", doc.metadata["page"])

            print(doc.page_content[:500])
        """

        return reranked_docs

    #########################################################################################################################################
    # 8- Build the retrieved context
    #########################################################################################################################################
    def build_context(self, reranked_docs):
        context_parts = []
        final_chunks = []

        for rank, (doc, score) in enumerate(reranked_docs, start=1):

            source = doc.metadata["source"]
            page = doc.metadata["page"]

            context_parts.append(
                self.config["rag"]["context_entry_template"].format(
                    source=source,
                    page=page,
                    page_content=doc.page_content
                )
            )
            final_chunks.append(
                {
                    "chunk_id": doc.metadata["chunk_id"],
                    "rank": rank,
                    "reranker_score": float(score),
                    "source": source,
                    "page": page,
                    "start_index": doc.metadata["start_index"],
                    "text": doc.page_content,
                }
            )

        context = self.config["rag"]["context_separator"].join(context_parts)

        # print(context)
        return context, final_chunks

    #########################################################################################################################################
    # 9- Construct the actual RAG prompt
    #########################################################################################################################################
    def build_prompt(self, context, query):
        rag_prompt = PromptTemplate.from_template(self.config["rag"]["prompt"])

        formatted_prompt = rag_prompt.format(
            context=context,
            question=query
        )

        # print(formatted_prompt)
        return formatted_prompt

    #########################################################################################################################################
    # 10- Generate the grounded response with the already-loaded LLM
    #########################################################################################################################################
    def generate_answer(self, formatted_prompt):
        return self.llm.invoke(formatted_prompt)

    def run(self, query):
        query_expansion, expanded_query = self.expand_query(query)
        retrieval = self.retrieve_candidates(query, expanded_query)
        reranked_docs = self.rerank_candidates(
            query,
            retrieval["candidate_docs"]
        )
        context, final_chunks = self.build_context(reranked_docs)
        formatted_prompt = self.build_prompt(context, query)
        response = self.generate_answer(formatted_prompt)

        return {
            "selected_sources": retrieval["selected_sources"],
            "explicit_source_restriction_detected": bool(
                find_explicit_sources(query, self.available_sources)
            ),
            "query_expansion": query_expansion,
            "final_context": context,
            "final_chunks": final_chunks,
            "generated_answer": response,
        }


def main():
    with Path("config.yml").open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    pdf_paths = sorted(Path(".").glob(config["documents"]["pdf_glob"]))

    if not pdf_paths:
        raise FileNotFoundError("No PDF files were found in the current directory.")

    query = config["query"]
    selected_sources = find_explicit_sources(
        query,
        [pdf_path.name for pdf_path in pdf_paths]
    )

    if selected_sources:
        print("Source explicitly selected:", ", ".join(selected_sources))
        pdf_paths_to_load = [
            pdf_path
            for pdf_path in pdf_paths
            if pdf_path.name in selected_sources
        ]
    else:
        print("No source explicitly selected; searching all sources.")
        pdf_paths_to_load = pdf_paths

    pipeline = RAGPipeline(config, pdf_paths_to_load)
    result = pipeline.run(query)
    print(result["generated_answer"])


if __name__ == "__main__":
    main()
