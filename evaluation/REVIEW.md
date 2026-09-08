# RAG Benchmark Source-Audit Review — v1.1.0

> All included examples passed a Codex source audit and are eligible for evaluation. This is automated source verification, not human approval or a guarantee of correctness.

PDF page numbers are one-based physical PDF pages and match `main.py`; printed page labels are recorded separately.

## ragbench-v1-001

**Question:** According to "Computer Vision: Algorithms and Applications.pdf", how does the original Hough transform use edge points, and what orientation-aware alternative is suggested for non-punctate points?

**Category / difficulty:** `multi_fact_lookup` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** In the original Hough transform, each edge point votes for every possible line through it, and high accumulator/bin values identify candidate line fits. For non-punctate line points, the book recommends using each edgel’s local orientation to vote for one accumulator cell.

**Required facts:**

- `ragbench-v1-001-f1`: Each edge point votes for all possible lines through it, and high accumulator or bin values are examined as possible line fits. (evidence: ragbench-v1-001-e1)
- `ragbench-v1-001-f2`: For points on a line that are not truly punctate, local edgel orientation can be used to vote for one accumulator cell. (evidence: ragbench-v1-001-e1)

**Evidence:**

- `ragbench-v1-001-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 504 (printed label 478); supports ragbench-v1-001-f1, ragbench-v1-001-f2

> The Hough transform, named after its original inventor (Hough 1962), is a well-known
> technique for having edges “vote” for plausible line locations (Duda and Hart 1972; Ballard
> 1981; Illingworth and Kittler 1988). In its original formulation (Figure 7.46), each edge point
> votes for all possible lines passing through it, and lines corresponding to highaccumulator or
> bin values are examined for potential line ﬁts.15 Unless the points on a line are truly punctate,
> a better approach is to use the local orientation information at each edgel to vote for a single
> accumulator cell (Figure 7.47), as described below.

**Required evidence groups:**

- `ragbench-v1-001-g1`: any one of [ragbench-v1-001-e1] supports ragbench-v1-001-f1.
- `ragbench-v1-001-g2`: any one of [ragbench-v1-001-e1] supports ragbench-v1-001-f2.

**Terminology examples:**

- Hough transform: Hough voting, accumulator voting, edge voting for lines

**Verified distractors:**

- `ragbench-v1-001-d1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 374 (printed label 348): This passage mentions Hough voting for object-alignment transformations, but it does not explain the original line-detection formulation asked about.

> Because images can be highly cluttered and similar features may belong to several objects,
> the original set of feature matches can have a large number of outliers. For this reason, Lowe
> (2004) suggests using a Hough transform (Section 7.4.2) to accumulate votes for likely geo-
> metric transformations. In his system, he uses an afﬁne transformation between the database
> object and the collection of scene features, which works well for objects that are mostly pla-
> nar, or where at least several corresponding features share a quasi-planar geometry.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-002

**Question:** How is the raw SIFT descriptor constructed, and what normalization and clipping steps make it less sensitive to photometric changes?

**Category / difficulty:** `multi_passage_synthesis` / `hard`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** SIFT computes gradients in a 16×16 window around a keypoint. Each 4×4 subregion contributes an eight-bin orientation histogram, producing 128 non-negative descriptor values. The vector is normalized to unit length, values are clipped to 0.2, and it is normalized again.

**Required facts:**

- `ragbench-v1-002-f1`: SIFT computes gradients in a 16×16 window around the detected keypoint. (evidence: ragbench-v1-002-e1)
- `ragbench-v1-002-f2`: A 4×4 array of eight-bin orientation histograms yields 128 non-negative values. (evidence: ragbench-v1-002-e2)
- `ragbench-v1-002-f3`: The 128-D vector is normalized to unit length, clipped at 0.2, and renormalized. (evidence: ragbench-v1-002-e2)

**Evidence:**

- `ragbench-v1-002-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 461 (printed label 435); supports ragbench-v1-002-f1

> Scale invariant feature transform (SIFT). SIFT features (Lowe 2004) are formed by com-
> puting the gradient at each pixel in a 16× 16 window around the detected keypoint, using the
> appropriate level of the Gaussian pyramid at which the keypoint was detected. The gradient
> magnitudes are downweighted by a Gaussian fall-off function (shown as a blue circle in Fig-
> ure 7.16a) to reduce the inﬂuence of gradients far from the center, as these are more affected
> by small misregistrations.
> In each 4 × 4 quadrant, a gradient orientation histogram is formed by (conceptually)
> adding the gradient values weighted by the Gaussian fall-off function to one of eight orienta-
> tion histogram bins.

- `ragbench-v1-002-e2` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 462 (printed label 436); supports ragbench-v1-002-f2, ragbench-v1-002-f3

> The 4x4 array of eight-bin histogram yields 128 non-negative values form a raw version
> of the SIFT descriptor vector. To reduce the effects of contrast or gain (additive variations are
> already removed by the gradient), the 128-D vector is normalized to unit length. To further
> make the descriptor robust to other photometric variations, values are clipped to 0.2 and the
> resulting vector is once again renormalized to unit length.

**Required evidence groups:**

- `ragbench-v1-002-g1`: any one of [ragbench-v1-002-e1] supports ragbench-v1-002-f1.
- `ragbench-v1-002-g2`: any one of [ragbench-v1-002-e2] supports ragbench-v1-002-f2.
- `ragbench-v1-002-g3`: any one of [ragbench-v1-002-e2] supports ragbench-v1-002-f3.

**Terminology examples:**

- scale invariant feature transform: SIFT, 128-D SIFT descriptor, gradient orientation descriptor

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-003

**Question:** What does hysteresis thresholding allow a contour tracker to do when an edge temporarily becomes weak?

**Category / difficulty:** `direct_factual_lookup` / `easy`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** It uses two thresholds and lets a curve that is being tracked above the higher threshold temporarily fall as low as the lower threshold.

**Required facts:**

- `ragbench-v1-003-f1`: Hysteresis uses two thresholds and permits a curve tracked above the high threshold to dip to the low threshold. (evidence: ragbench-v1-003-e1)

**Evidence:**

- `ragbench-v1-003-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 489 (printed label 463); supports ragbench-v1-003-f1

> Once the edgels have been linked into chains, we can apply an optional thresholding
> with hysteresis to remove low-strength contour segments (Canny 1986). The basic idea of
> hysteresis is to set two different thresholds and allow a curve being tracked above the higher
> threshold to dip in strength down to the lower threshold.

**Required evidence groups:**

- `ragbench-v1-003-g1`: any one of [ragbench-v1-003-e1] supports ragbench-v1-003-f1.

**Terminology examples:**

- thresholding with hysteresis: hysteresis thresholding, dual-threshold edge linking

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-004

**Question:** Why can a straight edge not fully determine patch motion in the aperture problem, and which component remains reliable?

**Category / difficulty:** `technical_distinction` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A straight segment at a single orientation suffers from the aperture problem: the patch can be aligned reliably only in the direction normal to the edge.

**Required facts:**

- `ragbench-v1-004-f1`: Straight-line patches at one orientation suffer from the aperture problem. (evidence: ragbench-v1-004-e1)
- `ragbench-v1-004-f2`: Only the motion/alignment component normal to the edge is reliably recoverable. (evidence: ragbench-v1-004-e1)

**Evidence:**

- `ragbench-v1-004-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 448 (printed label 422); supports ragbench-v1-004-f1, ragbench-v1-004-f2

> As you may notice, textureless patches are nearly impossible
> to localize. Patches with large contrast changes (gradients) are easier to localize, although
> straight line segments at a single orientation suffer from the aperture problem (Horn and
> Schunck 1981; Lucas and Kanade 1981; Anandan 1989), i.e., it is only possible to align
> the patches along the direction normal to the edge direction

**Required evidence groups:**

- `ragbench-v1-004-g1`: any one of [ragbench-v1-004-e1] supports ragbench-v1-004-f1.
- `ragbench-v1-004-g2`: any one of [ragbench-v1-004-e1] supports ragbench-v1-004-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-005

**Question:** For RANSAC-based correspondence fitting, how are hypotheses generated and scored, what inlier tolerance is described as common, and how do Preemptive RANSAC and PROSAC reduce work?

**Category / difficulty:** `multi_passage_synthesis` / `hard`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** RANSAC randomly selects k correspondences to estimate parameters, scores a hypothesis by counting predicted locations within an application-dependent tolerance often around 1–3 pixels, repeats the sampling, and keeps the sample with the most inliers. Preemptive RANSAC initially scores only a subset of measurements, while PROSAC initially samples from the most confident matches.

**Required facts:**

- `ragbench-v1-005-f1`: A random subset of k correspondences is used to compute an initial parameter estimate. (evidence: ragbench-v1-005-e1)
- `ragbench-v1-005-f2`: RANSAC counts inliers within an application-dependent tolerance that is often around 1–3 pixels, repeats the random selection, and retains the sample with the most inliers. (evidence: ragbench-v1-005-e2)
- `ragbench-v1-005-f3`: Preemptive RANSAC initially scores only a subset of measurements to select plausible hypotheses for further scoring. (evidence: ragbench-v1-005-e3)
- `ragbench-v1-005-f4`: PROSAC initially draws random samples from the most confident matches. (evidence: ragbench-v1-005-e3)

**Evidence:**

- `ragbench-v1-005-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 537 (printed label 511); supports ragbench-v1-005-f1

> Two widely used approaches to this problem are called RANdom SAmple Consensus, or
> RANSAC for short (Fischler and Bolles 1981), andleast median of squares(LMS) (Rousseeuw
> 1984). Both techniques start by selecting (at random) a subset ofk correspondences, which is
> then used to compute an initial estimate forp.

- `ragbench-v1-005-e2` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 537 (printed label 511); supports ragbench-v1-005-f2

> The RANSAC technique then counts the number of inliers that are within ϵ of their pre-
> dicted location, i.e., whose ‖ri‖ ≤ϵ. (The ϵ value is application dependent but is often
> around 1–3 pixels.) Least median of squares ﬁnds the median value of the‖ri‖2 values. The
> random selection process is repeated S times and the sample set with the largest number of
> inliers (or with the smallest median residual) is kept as the ﬁnal solution. Either the initial
> parameter guess p or the full set of computed inliers is then passed on to the next data ﬁtting
> stage.

- `ragbench-v1-005-e3` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 537 (printed label 511); supports ragbench-v1-005-f3, ragbench-v1-005-f4

> When the number of measurements is quite large, it may be preferable to only score a
> subset of the measurements in an initial round that selects the most plausible hypotheses for
> additional scoring and selection. This modiﬁcation of RANSAC, which can signiﬁcantly
> speed up its performance, is called Preemptive RANSAC (Nist´er 2003). In another variant on
> RANSAC called PROSAC (PROgressive SAmple Consensus), random samples are initially
> added from the most “conﬁdent” matches, thereby speeding up the process of ﬁnding a (sta-
> tistically) likely good set of inliers (Chum and Matas 2005). Raguram, Chum et al. (2012)
> provide a uniﬁed framework from which most of these techniques can be derived as well as a
> nice experimental comparison.

**Required evidence groups:**

- `ragbench-v1-005-g1`: any one of [ragbench-v1-005-e1] supports ragbench-v1-005-f1.
- `ragbench-v1-005-g2`: any one of [ragbench-v1-005-e2] supports ragbench-v1-005-f2.
- `ragbench-v1-005-g3`: any one of [ragbench-v1-005-e3] supports ragbench-v1-005-f3.
- `ragbench-v1-005-g4`: any one of [ragbench-v1-005-e3] supports ragbench-v1-005-f4.

**Terminology examples:**

- RANdom SAmple Consensus: RANSAC, random-sample consensus, robust correspondence fitting

**Verified distractors:**

- `ragbench-v1-005-d1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 574 (printed label 548): This confirms that RANSAC is a common robust initializer and names variants, but does not give the requested scoring rule, tolerance, or trial argument.

> The most commonly used robust initialization technique in computer
> vision is RANdom SAmple Consensus (RANSAC) (Fischler and Bolles 1981), which has
> spawned a series of more efﬁcient variants (Torr and Zisserman 2000; Nist´er 2003; Chum and
> Matas 2005; Raguram, Chum et al. 2012; Brachmann, Krull et al. 2017; Barath and Matas
> 2018; Barath, Matas, and Noskova 2019; Brachmann and Rother 2019). The MAGSAC++
> paper by Barath, Noskova et al. (2020) compares many of these variants.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-006

**Question:** When object scale is unknown, why does the book prefer scale-stable feature extraction over matching every pyramid scale, and how does Lowe's approach locate such features?

**Category / difficulty:** `method_comparison` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Matching features across many extracted scales is inefficient when object scale is unknown, so features stable in both location and scale are preferred. Lowe's method finds 3D space-plus-scale maxima across Difference-of-Gaussian sub-octave filters and refines the space-scale location with a quadratic fit; the cited implementation uses three sub-octave levels.

**Required facts:**

- `ragbench-v1-006-f1`: When object scale is unknown, extracting and cross-matching many scales is less efficient than extracting features stable in location and scale. (evidence: ragbench-v1-006-e1)
- `ragbench-v1-006-f2`: Lowe's method searches for 3D space-plus-scale maxima in Difference-of-Gaussian responses and uses a quadratic fit for sub-pixel space-scale localization. (evidence: ragbench-v1-006-e1)
- `ragbench-v1-006-f3`: The number of sub-octave levels is three. (evidence: ragbench-v1-006-e1)

**Evidence:**

- `ragbench-v1-006-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 455 (printed label 429); supports ragbench-v1-006-f1, ragbench-v1-006-f2, ragbench-v1-006-f3

> However, for most object recognition applications, the scale of the object in the image
> is unknown. Instead of extracting features at many different scales and then matching all of
> them, it is more efﬁcient to extract features that are stable in both location and scale (Lowe
> 2004; Mikolajczyk and Schmid 2004).
> Early investigations into scale selection were performed by Lindeberg (1993; 1998b),
> who ﬁrst proposed using extrema in the Laplacian of Gaussian (LoG) function as interest
> point locations. Based on this work, Lowe (2004) proposed computing a set of sub-octave
> Difference of Gaussian ﬁlters (Figure 7.11a), looking for 3D (space+scale) maxima in the re-
> sulting structure (Figure 7.11b), and then computing a sub-pixel space+scale location using a
> quadratic ﬁt (Brown and Lowe 2002). The number of sub-octave levels was determined, after
> careful empirical investigation, to be three, which corresponds to a quarter-octave pyramid,
> which is the same as used by Triggs (2004).

**Required evidence groups:**

- `ragbench-v1-006-g1`: any one of [ragbench-v1-006-e1] supports ragbench-v1-006-f1.
- `ragbench-v1-006-g2`: any one of [ragbench-v1-006-e1] supports ragbench-v1-006-f2.
- `ragbench-v1-006-g3`: any one of [ragbench-v1-006-e1] supports ragbench-v1-006-f3.

**Terminology examples:**

- Difference of Gaussian: DoG, difference-of-Gaussian scale space, space-plus-scale extrema

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-007

**Question:** How does MOPS reduce sensitivity to detector-position errors and affine photometric changes?

**Category / difficulty:** `direct_factual_lookup` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** MOPS samples patches at five-pixel spacing relative to detection scale from a coarser pyramid level, reducing aliasing and sensitivity to location, orientation, and scale errors. It rescales intensities to zero mean and unit variance to compensate for linear exposure bias and gain.

**Required facts:**

- `ragbench-v1-007-f1`: MOPS samples at five-pixel spacing relative to detection scale from a coarser pyramid level to reduce aliasing and detector inaccuracies. (evidence: ragbench-v1-007-e1)
- `ragbench-v1-007-f2`: MOPS rescales patch intensities to mean zero and variance one to compensate for affine photometric bias and gain. (evidence: ragbench-v1-007-e1)

**Evidence:**

- `ragbench-v1-007-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 461 (printed label 435); supports ragbench-v1-007-f1, ragbench-v1-007-f2

> To com-
> pensate for slight inaccuracies in the feature point detector (location, orientation, and scale),
> multi-scale oriented patches (MOPS) are sampled at a spacing of ﬁve pixels relative to the
> detection scale, using a coarser level of the image pyramid to avoid aliasing. To compen-
> sate for afﬁne photometric variations (linear exposure changes or bias and gain, (3.3)), patch
> intensities are re-scaled so that their mean is zero and their variance is one.

**Required evidence groups:**

- `ragbench-v1-007-g1`: any one of [ragbench-v1-007-e1] supports ragbench-v1-007-f1.
- `ragbench-v1-007-g2`: any one of [ragbench-v1-007-e1] supports ragbench-v1-007-f2.

**Terminology examples:**

- multi-scale oriented patches: MOPS, bias-and-gain-normalized intensity patches

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-008

**Question:** How should edge-detector scale be chosen differently for sharp-edge detection versus detecting edges at multiple resolutions?

**Category / difficulty:** `conditional_claim` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** For sharp edges, filter width can be selected from the image-noise characteristics. To detect edges occurring at different resolutions, a scale-space method that detects and selects edges across scales may be required.

**Required facts:**

- `ragbench-v1-008-f1`: For sharp-edge detection, filter width can be determined from image-noise characteristics. (evidence: ragbench-v1-008-e1)
- `ragbench-v1-008-f2`: For edges at different resolutions, a scale-space detection-and-selection approach may be necessary. (evidence: ragbench-v1-008-e1)

**Evidence:**

- `ragbench-v1-008-e1` — `Computer Vision: Algorithms and Applications.pdf`, PDF page 485 (printed label 459); supports ragbench-v1-008-f1, ragbench-v1-008-f2

> As we mentioned before, the derivative, Laplacian, and Difference of Gaussian ﬁlters (7.20–
> 7.23) all require the selection of a spatial scale parameter σ. If we are only interested in
> detecting sharp edges, the width of the ﬁlter can be determined from image noise characteris-
> tics (Canny 1986; Elder and Zucker 1998). However, if we want to detect edges that occur at
> different resolutions (Figures 7.33b–c), a scale-space approach that detects and then selects
> edges at different scales may be necessary

**Required evidence groups:**

- `ragbench-v1-008-g1`: any one of [ragbench-v1-008-e1] supports ragbench-v1-008-f1.
- `ragbench-v1-008-g2`: any one of [ragbench-v1-008-e1] supports ragbench-v1-008-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-009

**Question:** According to "Designing Data-Intensive Applications.pdf", what usually limits a data-intensive application, and which standard building blocks support search and asynchronous handling?

**Category / difficulty:** `direct_factual_lookup` / `easy`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Raw CPU power is rarely the main limit; the amount, complexity, and rate of change of data are usually bigger problems. Search indexes support keyword/filter search, while stream-processing systems send work to another process for asynchronous handling.

**Required facts:**

- `ragbench-v1-009-f1`: Data amount, complexity, and rate of change usually matter more than raw CPU power for data-intensive applications. (evidence: ragbench-v1-009-e1)
- `ragbench-v1-009-f2`: Search indexes provide keyword or filtered search. (evidence: ragbench-v1-009-e1)
- `ragbench-v1-009-f3`: Stream processing supports sending a message to another process for asynchronous handling. (evidence: ragbench-v1-009-e1)

**Evidence:**

- `ragbench-v1-009-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 25 (printed label 3); supports ragbench-v1-009-f1, ragbench-v1-009-f2, ragbench-v1-009-f3

> Many applications today are data-intensive, as opposed to compute-intensive. Raw
> CPU power is rarely a limiting factor for these applications—bigger problems are
> usually the amount of data, the complexity of data, and the speed at which it is
> changing.
> A data-intensive application is typically built from standard building blocks that pro‐
> vide commonly needed functionality. For example, many applications need to:
> • Store data so that they, or another application, can find it again later (databases)
> • Remember the result of an expensive operation, to speed up reads (caches)
> • Allow users to search data by keyword or filter it in various ways (search indexes)
> • Send a message to another process, to be handled asynchronously ( stream pro‐
> cessing)
> • Periodically crunch a large amount of accumulated data (batch processing)

**Required evidence groups:**

- `ragbench-v1-009-g1`: any one of [ragbench-v1-009-e1] supports ragbench-v1-009-f1.
- `ragbench-v1-009-g2`: any one of [ragbench-v1-009-e1] supports ragbench-v1-009-f2.
- `ragbench-v1-009-g3`: any one of [ragbench-v1-009-e1] supports ragbench-v1-009-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-010

**Question:** What is the book's distinction between a fault and a failure, and why can deliberately triggering faults improve confidence in a system?

**Category / difficulty:** `technical_distinction` / `medium`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A fault is one component deviating from its specification; a failure is the whole system stopping the required user service. Deliberately inducing faults continually exercises error-handling and fault-tolerance machinery, increasing confidence that naturally occurring faults will be handled.

**Required facts:**

- `ragbench-v1-010-f1`: A fault is a component deviating from its specification, whereas a failure is the system as a whole ceasing to provide the required service. (evidence: ragbench-v1-010-e1)
- `ragbench-v1-010-f2`: Deliberately induced faults continuously exercise fault-tolerance mechanisms and can increase confidence in their behavior under natural faults. (evidence: ragbench-v1-010-e1)

**Evidence:**

- `ragbench-v1-010-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 29 (printed label 7); supports ragbench-v1-010-f1, ragbench-v1-010-f2

> Note that a fault is not the same as a failure [ 2]. A fault is usually defined as one com‐
> ponent of the system deviating from its spec, whereas a failure is when the system as a
> whole stops providing the required service to the user. It is impossible to reduce the
> probability of a fault to zero; therefore it is usually best to design fault-tolerance
> mechanisms that prevent faults from causing failures. In this book we cover several
> techniques for building reliable systems from unreliable parts.
> Counterintuitively, in such fault-tolerant systems, it can make sense to increase the
> rate of faults by triggering them deliberately—for example, by randomly killing indi‐
> vidual processes without warning. Many critical bugs are actually due to poor error
> handling [ 3]; by deliberately inducing faults, you ensure that the fault-tolerance
> machinery is continually exercised and tested, which can increase your confidence
> that faults will be handled correctly when they occur naturally. The Netflix Chaos
> Monkey [4] is an example of this approach.

**Required evidence groups:**

- `ragbench-v1-010-g1`: any one of [ragbench-v1-010-e1] supports ragbench-v1-010-f1.
- `ragbench-v1-010-g2`: any one of [ragbench-v1-010-e1] supports ragbench-v1-010-f2.

**Verified distractors:**

- `ragbench-v1-010-d1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 127 (printed label 127): This discusses recovery from a failed crawler, but it does not define the fault-versus-failure distinction.

> We should use consistent hashing for distribution among crawling servers. 
> Consistent hashing will not only help in replacing a dead host, but also help in 
> distributing load among crawling servers. 
> All our crawling servers will be performing regular checkpointing and storing their 
> FIFO queues to disks. If a server goes down, we can replace it. Meanwhile, consistent 
> hashing should shift the load to other servers.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-011

**Question:** What makes a partial failure in a distributed system especially difficult to reason about?

**Category / difficulty:** `direct_factual_lookup` / `easy`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Only some components may be broken while others work, and the behavior is nondeterministic: an operation across nodes and the network may sometimes work and sometimes fail, and message-delay uncertainty can leave success itself unknown.

**Required facts:**

- `ragbench-v1-011-f1`: A partial failure leaves some system parts broken while others continue working. (evidence: ragbench-v1-011-e1)
- `ragbench-v1-011-f2`: Partial failures are nondeterministic, and network delay can make it unclear whether an operation succeeded. (evidence: ragbench-v1-011-e1)

**Evidence:**

- `ragbench-v1-011-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 297 (printed label 275); supports ragbench-v1-011-f1, ragbench-v1-011-f2

> In a distributed system, there may well be some parts of the system that are broken in
> some unpredictable way, even though other parts of the system are working fine. This
> is known as a partial failure. The difficulty is that partial failures are nondeterministic:
> if you try to do anything involving multiple nodes and the network, it may sometimes
> work and sometimes unpredictably fail. As we shall see, you may not even know
> whether something succeeded or not, as the time it takes for a message to travel
> across a network is also nondeterministic!
> This nondeterminism and possibility of partial failures is what makes distributed sys‐
> tems hard to work with [5].

**Required evidence groups:**

- `ragbench-v1-011-g1`: any one of [ragbench-v1-011-e1] supports ragbench-v1-011-f1.
- `ragbench-v1-011-g2`: any one of [ragbench-v1-011-e1] supports ragbench-v1-011-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-012

**Question:** For Dynamo-style leaderless replication, what does w + r > n mean, and how many unavailable nodes can the cited n=5, w=3, r=3 setup tolerate?

**Category / difficulty:** `multi_passage_synthesis` / `medium`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** With n replicas, a write must be confirmed by w nodes and a read must query at least r nodes. If w + r > n, the read and write sets overlap in at least one up-to-date replica. For n=5 and w=r=3, the system can tolerate two unavailable nodes.

**Required facts:**

- `ragbench-v1-012-f1`: n is the replica count, w is the minimum write confirmations, and r is the minimum replicas queried for a read. (evidence: ragbench-v1-012-e1)
- `ragbench-v1-012-f2`: w + r > n is intended to ensure that at least one read replica is up to date through read/write-set overlap. (evidence: ragbench-v1-012-e1, ragbench-v1-012-e3)
- `ragbench-v1-012-f3`: The n=5, w=3, r=3 configuration tolerates two unavailable nodes. (evidence: ragbench-v1-012-e2)

**Evidence:**

- `ragbench-v1-012-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 201 (printed label 179); supports ragbench-v1-012-f1, ragbench-v1-012-f2

> More generally, if there are n replicas, every write must be confirmed by w nodes to
> be considered successful, and we must query at least r nodes for each read. (In our
> example, n = 3, w = 2, r = 2.) As long as w + r > n, we expect to get an up-to-date
> value when reading, because at least one of the r nodes we’re reading from must be
> up to date. Reads and writes that obey these r and w values are called quorum reads
> and writes [44].vii You can think of r and w as the minimum number of votes required
> for the read or write to be valid.

- `ragbench-v1-012-e2` — `Designing Data-Intensive Applications.pdf`, PDF page 202 (printed label 180); supports ragbench-v1-012-f3

> The quorum condition, w + r > n, allows the system to tolerate unavailable nodes as
> follows:
> • If w < n, we can still process writes if a node is unavailable.
> • If r < n, we can still process reads if a node is unavailable.
> • With n = 3, w = 2, r = 2 we can tolerate one unavailable node.
> • With n = 5, w = 3, r = 3 we can tolerate two unavailable nodes.

- `ragbench-v1-012-e3` — `Designing Data-Intensive Applications.pdf`, PDF page 203 (printed label 181); supports ragbench-v1-012-f2

> If you have n replicas, and you choose w and r such that w + r > n, you can generally
> expect every read to return the most recent value written for a key. This is the case
> because the set of nodes to which you’ve written and the set of nodes from which
> you’ve read must overlap. That is, among the nodes you read there must be at least
> one node with the latest value

**Required evidence groups:**

- `ragbench-v1-012-g1`: any one of [ragbench-v1-012-e1] supports ragbench-v1-012-f1.
- `ragbench-v1-012-g2`: any one of [ragbench-v1-012-e1; ragbench-v1-012-e3] supports ragbench-v1-012-f2.
- `ragbench-v1-012-g3`: any one of [ragbench-v1-012-e2] supports ragbench-v1-012-f3.

**Terminology examples:**

- quorum reads and writes: read/write quorum, w plus r greater than n, Dynamo-style quorum

**Verified distractors:**

- `ragbench-v1-012-d1` — `Designing Data-Intensive Applications.pdf`, PDF page 388 (printed label 366): This is about a majority needed for consensus termination, not the n/w/r rule for leaderless reads and writes.

> There is a limit to the number of failures that an
> algorithm can tolerate: in fact, it can be proved that any consensus algorithm requires
> at least a majority of nodes to be functioning correctly in order to assure termination
> [67]. That majority can safely form a quorum (see “Quorums for reading and writ‐
> ing” on page 179).

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-013

**Question:** Why can a Dynamo-style system still return stale data even when w + r > n? Give the two edge cases identified in the text.

**Category / difficulty:** `limitations_and_exceptions` / `hard`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A sloppy quorum can place the w writes on different nodes from the r reads, eliminating guaranteed overlap. Also, concurrent writes have no clear first-write ordering; timestamp-based last-write-wins can lose writes because of clock skew.

**Required facts:**

- `ragbench-v1-013-f1`: With a sloppy quorum, the write and read node sets may not overlap even if w + r > n. (evidence: ragbench-v1-013-e1)
- `ragbench-v1-013-f2`: Concurrent writes have ambiguous ordering, and timestamp-based last-write-wins can lose writes due to clock skew. (evidence: ragbench-v1-013-e1)

**Evidence:**

- `ragbench-v1-013-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 203 (printed label 181); supports ragbench-v1-013-f1, ragbench-v1-013-f2

> However, even with w + r > n, there are likely to be edge cases where stale values are
> returned. These depend on the implementation, but possible scenarios include:
> • If a sloppy quorum is used (see “Sloppy Quorums and Hinted Handoff”  on page
> 183), the w writes may end up on different nodes than the r reads, so there is no
> longer a guaranteed overlap between the r nodes and the w nodes [46].
> • If two writes occur concurrently, it is not clear which one happened first. In this
> case, the only safe solution is to merge the concurrent writes (see “Handling
> Write Conflicts” on page 171). If a winner is picked based on a timestamp (last
> write wins), writes can be lost due to clock skew [ 35]. We will return to this topic
> in “Detecting Concurrent Writes” on page 184.

**Required evidence groups:**

- `ragbench-v1-013-g1`: any one of [ragbench-v1-013-e1] supports ragbench-v1-013-f1.
- `ragbench-v1-013-g2`: any one of [ragbench-v1-013-e1] supports ragbench-v1-013-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-014

**Question:** How do serializability and linearizability differ, and what is the name for a database that provides both?

**Category / difficulty:** `technical_distinction` / `hard`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Serializability is a transaction-isolation property: multi-object transactions behave as if run in some serial order, which need not match real time. Linearizability is a recency guarantee for reads and writes of one object and does not group operations into transactions. Providing both is called strict serializability or strong one-copy serializability (strong-1SR).

**Required facts:**

- `ragbench-v1-014-f1`: Serializability makes multi-object transactions behave as if executed in some serial order, which may differ from actual execution order. (evidence: ragbench-v1-014-e1)
- `ragbench-v1-014-f2`: Linearizability is a recency guarantee for individual-object reads and writes and does not group operations into transactions. (evidence: ragbench-v1-014-e1)
- `ragbench-v1-014-f3`: The combination is called strict serializability or strong one-copy serializability (strong-1SR). (evidence: ragbench-v1-014-e1)

**Evidence:**

- `ragbench-v1-014-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 351 (printed label 329); supports ragbench-v1-014-f1, ragbench-v1-014-f2, ragbench-v1-014-f3

> Linearizability is easily confused with serializability (see “Serializability” on page 251),
> as both words seem to mean something like “can be arranged in a sequential order.”
> However, they are two quite different guarantees, and it is important to distinguish
> between them:
> Serializability
> Serializability is an isolation property of transactions, where every transaction
> may read and write multiple objects (rows, documents, records)—see “Single-
> Object and Multi-Object Operations” on page 228. It guarantees that transac‐
> tions behave the same as if they had executed in some serial order (each
> transaction running to completion before the next transaction starts). It is okay
> for that serial order to be different from the order in which transactions were
> actually run [12].
> Linearizability
> Linearizability is a recency guarantee on reads and writes of a register (an indi‐
> vidual object). It doesn’t group operations together into transactions, so it does
> not prevent problems such as write skew (see “Write Skew and Phantoms” on
> page 246), unless you take additional measures such as materializing conflicts
> (see “Materializing conflicts” on page 251).
> A database may provide both serializability and linearizability, and this combination
> is known as strict serializability or strong one-copy serializability (strong-1SR) [4, 13].

**Required evidence groups:**

- `ragbench-v1-014-g1`: any one of [ragbench-v1-014-e1] supports ragbench-v1-014-f1.
- `ragbench-v1-014-g2`: any one of [ragbench-v1-014-e1] supports ragbench-v1-014-f2.
- `ragbench-v1-014-g3`: any one of [ragbench-v1-014-e1] supports ragbench-v1-014-f3.

**Terminology examples:**

- strong one-copy serializability: strict serializability, strong-1SR

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-015

**Question:** What concrete performance penalty is reported for MySQL distributed transactions, and which two mechanisms account for much of two-phase commit's inherent cost?

**Category / difficulty:** `numerical_factual_lookup` / `medium`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Distributed transactions in MySQL are reported to be more than 10 times slower than single-node transactions. Much of 2PC's cost comes from extra disk forcing (fsync) needed for crash recovery and extra network round trips.

**Required facts:**

- `ragbench-v1-015-f1`: MySQL distributed transactions are reported as over 10 times slower than single-node transactions. (evidence: ragbench-v1-015-e1)
- `ragbench-v1-015-f2`: Additional fsync for crash recovery and additional network round trips cause much of two-phase commit's inherent cost. (evidence: ragbench-v1-015-e1)

**Evidence:**

- `ragbench-v1-015-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 382 (printed label 360); supports ragbench-v1-015-f1, ragbench-v1-015-f2

> Some implementations of distributed transactions carry a heavy performance penalty
> —for example, distributed transactions in MySQL are reported to be over 10 times
> slower than single-node transactions [ 87], so it is not surprising when people advise
> against using them. Much of the performance cost inherent in two-phase commit is
> due to the additional disk forcing (fsync) that is required for crash recovery [88], and
> the additional network round-trips.

**Required evidence groups:**

- `ragbench-v1-015-g1`: any one of [ragbench-v1-015-e1] supports ragbench-v1-015-f1.
- `ragbench-v1-015-g2`: any one of [ragbench-v1-015-e1] supports ragbench-v1-015-f2.

**Terminology examples:**

- two-phase commit: 2PC, distributed atomic commit

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-016

**Question:** If an XA transaction coordinator crashes after participants prepare, why can the transaction block other transactions that need the same data until recovery?

**Category / difficulty:** `causal_explanation` / `hard`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Prepared participants remain in doubt until the application server restarts and the coordinator recovers the commit/abort outcome from its local log. A two-phase-commit transaction retains its locks while in doubt, so transactions needing the same rows can be blocked. If the coordinator log is lost, the locks may remain until an administrator resolves the transaction manually.

**Required facts:**

- `ragbench-v1-016-f1`: Prepared participants remain in doubt until the server restarts and the coordinator recovers the decision from its local log. (evidence: ragbench-v1-016-e1)
- `ragbench-v1-016-f2`: A two-phase-commit transaction holds its locks throughout the time it is in doubt. (evidence: ragbench-v1-016-e2)
- `ragbench-v1-016-f3`: While those locks are held, other transactions that access the same rows can be blocked. (evidence: ragbench-v1-016-e3)
- `ragbench-v1-016-f4`: If the coordinator log is lost, the locks may remain until manual resolution by an administrator. (evidence: ragbench-v1-016-e4)

**Evidence:**

- `ragbench-v1-016-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 384 (printed label 362); supports ragbench-v1-016-f1

> If the application process crashes, or the machine on which the application is running
> dies, the coordinator goes with it. Any participants with prepared but uncommitted
> transactions are then stuck in doubt. Since the coordinator’s log is on the application
> server’s local disk, that server must be restarted, and the coordinator library must
> read the log to recover the commit/abort outcome of each transaction. Only then can
> the coordinator use the database driver’s XA callbacks to ask participants to commit
> or abort, as appropriate. The database server cannot contact the coordinator directly,
> since all communication must go via its client library.

- `ragbench-v1-016-e2` — `Designing Data-Intensive Applications.pdf`, PDF page 384 (printed label 362); supports ragbench-v1-016-f2

> Therefore, when using two-phase commit,
> a transaction must hold onto the locks throughout the time it is in doubt.

- `ragbench-v1-016-e3` — `Designing Data-Intensive Applications.pdf`, PDF page 384 (printed label 362); supports ragbench-v1-016-f3

> While those locks are held, no other transaction can modify those rows. Depending
> on the database, other transactions may even be blocked from reading those rows.
> Thus, other transactions cannot simply continue with their business—if they want to
> access that same data, they will be blocked.

- `ragbench-v1-016-e4` — `Designing Data-Intensive Applications.pdf`, PDF page 384 (printed label 362); supports ragbench-v1-016-f4

> If the coordinator’s log is entirely lost for some reason, those locks
> will be held forever—or at least until the situation is manually resolved by an admin‐
> istrator.

**Required evidence groups:**

- `ragbench-v1-016-g1`: any one of [ragbench-v1-016-e1] supports ragbench-v1-016-f1.
- `ragbench-v1-016-g2`: any one of [ragbench-v1-016-e2] supports ragbench-v1-016-f2.
- `ragbench-v1-016-g3`: any one of [ragbench-v1-016-e3] supports ragbench-v1-016-f3.
- `ragbench-v1-016-g4`: any one of [ragbench-v1-016-e4] supports ragbench-v1-016-f4.

**Terminology examples:**

- X/Open XA: XA, heterogeneous two-phase commit, in-doubt transaction

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-017

**Question:** Why do microbatching or checkpointing alone stop providing exactly-once effects once stream output reaches an external system?

**Category / difficulty:** `limitations_and_exceptions` / `medium`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Inside the stream processor, failed output can be discarded and work restarted. Once output has reached an external database, broker, or email system, the framework cannot discard it; retrying the failed task may repeat the external side effect. Exactly-once appearance then requires all outputs, state changes, and input acknowledgments to succeed or fail atomically.

**Required facts:**

- `ragbench-v1-017-f1`: The framework cannot discard output that has already left the stream processor for an external system. (evidence: ragbench-v1-017-e1)
- `ragbench-v1-017-f2`: Restarting a failed task can repeat an external side effect, so microbatching/checkpointing alone is insufficient. (evidence: ragbench-v1-017-e1)
- `ragbench-v1-017-f3`: Exactly-once appearance requires outputs, side effects, state changes, and acknowledgments to take effect atomically with processing success. (evidence: ragbench-v1-017-e1)

**Evidence:**

- `ragbench-v1-017-e1` — `Designing Data-Intensive Applications.pdf`, PDF page 499 (printed label 477); supports ragbench-v1-017-f1, ragbench-v1-017-f2, ragbench-v1-017-f3

> Within the confines of the stream processing framework, the microbatching and
> checkpointing approaches provide the same exactly-once semantics as batch process‐
> ing. However, as soon as output leaves the stream processor (for example, by writing
> to a database, sending messages to an external message broker, or sending emails),
> the framework is no longer able to discard the output of a failed batch. In this case,
> restarting a failed task causes the external side effect to happen twice, and micro‐
> batching or checkpointing alone is not sufficient to prevent this problem.
> Atomic commit revisited
> In order to give the appearance of exactly-once processing in the presence of faults,
> we need to ensure that all outputs and side effects of processing an event take effect if
> and only if  the processing is successful. Those effects include any messages sent to
> downstream operators or external messaging systems (including email or push notifi‐
> cations), any database writes, any changes to operator state, and any acknowledg‐
> ment of input messages (including moving the consumer offset forward in a log-
> based message broker).

**Required evidence groups:**

- `ragbench-v1-017-g1`: any one of [ragbench-v1-017-e1] supports ragbench-v1-017-f1.
- `ragbench-v1-017-g2`: any one of [ragbench-v1-017-e1] supports ragbench-v1-017-f2.
- `ragbench-v1-017-g3`: any one of [ragbench-v1-017-e1] supports ragbench-v1-017-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-018

**Question:** For the URL-shortening design, how many strings does a six-character base64 key provide, and why can truncating an MD5-derived base64 string still cause trouble?

**Category / difficulty:** `numerical_factual_lookup` / `medium`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A six-character base64 key provides about 68.7 billion strings. MD5 produces a 128-bit value whose base64 form exceeds 21 characters; taking only the first six or eight characters can create duplicate keys, requiring another character selection or swap.

**Required facts:**

- `ragbench-v1-018-f1`: Six base64 characters provide 64^6, approximately 68.7 billion, possible strings. (evidence: ragbench-v1-018-e1)
- `ragbench-v1-018-f2`: A 128-bit MD5 hash becomes more than 21 base64 characters. (evidence: ragbench-v1-018-e2)
- `ragbench-v1-018-f3`: Truncating that encoding to six or eight characters can cause duplicate keys. (evidence: ragbench-v1-018-e2)

**Evidence:**

- `ragbench-v1-018-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 17 (printed label 17); supports ragbench-v1-018-f1

> Using base64 encoding, a 6 letter long key would result in 64^6 = ~68.7 billion 
> possible strings

- `ragbench-v1-018-e2` — `Grokking-the-system-design-interview-free.pdf`, PDF page 18 (printed label 18); supports ragbench-v1-018-f2, ragbench-v1-018-f3

> If we use the MD5 algorithm as our hash function, it’ll produce a 128-bit hash value. 
> After base64 encoding, we’ll get a string having more than 21 characters (since each 
> base64 character encodes 6 bits of the hash value). Since we only have space for 8 
> characters per short key, how will we choose our key then? We can take the first 6 
> (or 8) letters for the key. This could result in key duplication though, upon which we 
> can choose some other characters out of the encoding string or swap some 
> characters.

**Required evidence groups:**

- `ragbench-v1-018-g1`: any one of [ragbench-v1-018-e1] supports ragbench-v1-018-f1.
- `ragbench-v1-018-g2`: any one of [ragbench-v1-018-e2] supports ragbench-v1-018-f2.
- `ragbench-v1-018-g3`: any one of [ragbench-v1-018-e2] supports ragbench-v1-018-f3.

**Terminology examples:**

- base64 encoding: base-64, six-character short key, URL hash encoding

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-019

**Question:** How does the proposed offline Key Generation Service prevent two application servers from receiving the same short key, and what loss is accepted if the service dies?

**Category / difficulty:** `causal_explanation` / `medium`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** KGS keeps unused and used key tables, moves keys to the used table as soon as it hands or loads them into memory, and synchronizes or locks its in-memory key structure before removal. If KGS dies before assigning every loaded key, those keys are wasted, which the design accepts because the keyspace is huge.

**Required facts:**

- `ragbench-v1-019-f1`: KGS separates unused and used keys and moves keys to the used set when giving or loading them for a server. (evidence: ragbench-v1-019-e1)
- `ragbench-v1-019-f2`: KGS must synchronize or lock the in-memory key data structure before removing and giving keys. (evidence: ragbench-v1-019-e2)
- `ragbench-v1-019-f3`: Keys loaded but not assigned before a KGS failure may be wasted, and the design considers that acceptable. (evidence: ragbench-v1-019-e1)

**Evidence:**

- `ragbench-v1-019-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 21 (printed label 21); supports ragbench-v1-019-f1, ragbench-v1-019-f3

> Can concurrency cause problems? As soon as a key is used, it should be marked 
> in the database to ensure it doesn’t get used again. If there are multiple servers 
> reading keys concurrently, we might get a scenario where two or more servers try to 
> read the same key from the database. How can we solve this concurrency problem? 
> Servers can use KGS to read/mark keys in the database. KGS can use two tables to 
> store keys: one for keys that are not used yet, and one for all the used keys. As soon 
> as KGS gives keys to one of the servers, it can move them to the used keys table. KGS 
> can always keep some keys in memory so that it can quickly provide them whenever 
> a server needs them. 
> For simplicity, as soon as KGS loads some keys in memory, it can move them to the 
> used keys table. This ensures each server gets unique keys. If KGS dies before 
> assigning all the loaded keys to some server, we will be wasting those keys–which is 
> acceptable, given the huge number of keys we have.

- `ragbench-v1-019-e2` — `Grokking-the-system-design-interview-free.pdf`, PDF page 22 (printed label 22); supports ragbench-v1-019-f2

> KGS also has to make sure not to give the same key to multiple servers. For that, it 
> must synchronize (or get a lock on) the data structure holding the keys before 
> removing keys from it and giving them to a server

**Required evidence groups:**

- `ragbench-v1-019-g1`: any one of [ragbench-v1-019-e1] supports ragbench-v1-019-f1.
- `ragbench-v1-019-g2`: any one of [ragbench-v1-019-e2] supports ragbench-v1-019-f2.
- `ragbench-v1-019-g3`: any one of [ragbench-v1-019-e1] supports ragbench-v1-019-f3.

**Terminology examples:**

- Key Generation Service: KGS, offline key generator, key-DB service

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-020

**Question:** What storage size is estimated for all six-character base64 keys, and how does the design address KGS being a single point of failure?

**Category / difficulty:** `multi_fact_lookup` / `easy`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The estimated key database size is 412 GB for 68.7 billion six-character keys at one byte per character. A standby KGS replica takes over if the primary dies.

**Required facts:**

- `ragbench-v1-020-f1`: Storing all 68.7 billion six-character keys at one byte per character is estimated at 412 GB. (evidence: ragbench-v1-020-e1)
- `ragbench-v1-020-f2`: A standby KGS replica is proposed to take over after primary failure. (evidence: ragbench-v1-020-e1)

**Evidence:**

- `ragbench-v1-020-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 22 (printed label 22); supports ragbench-v1-020-f1, ragbench-v1-020-f2

> What would be the key-DB size? With base64 encoding, we can generate 68.7B 
> unique six letters keys. If we need one byte to store one alpha-numeric character, we 
> can store all these keys in: 
> 6 (characters per key) * 68.7B (unique keys) = 412 GB. 
> Isn’t KGS a single point of failure? Yes, it is. To solve this, we can have a standby 
> replica of KGS. Whenever the primary server dies, the standby server can take over 
> to generate and provide keys.

**Required evidence groups:**

- `ragbench-v1-020-g1`: any one of [ragbench-v1-020-e1] supports ragbench-v1-020-f1.
- `ragbench-v1-020-g2`: any one of [ragbench-v1-020-e1] supports ragbench-v1-020-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-021

**Question:** How does the distributed URL frontier enforce politeness toward each web server?

**Category / difficulty:** `direct_factual_lookup` / `medium`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Each crawler server maintains distinct FIFO subqueues, one per worker. A URL's canonical hostname is hashed to a thread/subqueue, so at most one worker contacts a given web server, while FIFO ordering prevents that server from being overloaded.

**Required facts:**

- `ragbench-v1-021-f1`: Each worker thread has a separate FIFO crawling subqueue. (evidence: ragbench-v1-021-e1)
- `ragbench-v1-021-f2`: Canonical hostname hashing assigns URLs to a thread, limiting a web server to one worker and using FIFO order to avoid overload. (evidence: ragbench-v1-021-e1)

**Evidence:**

- `ragbench-v1-021-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 124 (printed label 124); supports ragbench-v1-021-f1, ragbench-v1-021-f2

> Following politeness requirements must be kept in mind while designing a 
> distributed URL frontier: 
> 1. Our crawler should not overload a server by downloading a lot of pages from 
> it. 
> 2. We should not have multiple machines connecting a web server. 
> To implement this politeness constraint our crawler can have a collection of distinct 
> FIFO sub-queues on each server. Each worker thread will have its separate sub-
> queue, from which it removes URLs for crawling. When a new URL needs to be 
> added, the FIFO sub-queue in which it is placed will be determined by the URL’s 
> canonical hostname. Our hash function can map each hostname to a thread number. 
> Together, these two points imply that, at most, one worker thread will download 
> documents from a given Web server and also, by using FIFO queue, it’ll not overload 
> a Web server.

**Required evidence groups:**

- `ragbench-v1-021-g1`: any one of [ragbench-v1-021-e1] supports ragbench-v1-021-f1.
- `ragbench-v1-021-g2`: any one of [ragbench-v1-021-e1] supports ragbench-v1-021-f2.

**Terminology examples:**

- URL frontier: crawl frontier, crawler queue, polite crawling

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-022

**Question:** According to "Grokking-the-system-design-interview-free.pdf", what are the main read/write tradeoffs of feed fan-out, and how does the hybrid design treat celebrity accounts?

**Category / difficulty:** `method_comparison` / `hard`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Fan-out-on-load lets clients pull recent feed data but can delay new items and waste empty polling requests. Fan-out-on-write reduces feed-read work by pushing a new post immediately, but is expensive for accounts with millions of followers. The hybrid pushes ordinary users' posts but makes followers pull celebrity updates.

**Required facts:**

- `ragbench-v1-022-f1`: Fan-out-on-load can delay visibility until a pull and can waste resources through empty polling. (evidence: ragbench-v1-022-e1)
- `ragbench-v1-022-f2`: Fan-out-on-write reduces read operations but becomes costly for users with millions of followers. (evidence: ragbench-v1-022-e1)
- `ragbench-v1-022-f3`: The hybrid pushes posts for lower-follower accounts and uses pull for celebrity updates. (evidence: ragbench-v1-022-e2)

**Evidence:**

- `ragbench-v1-022-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 134 (printed label 134); supports ragbench-v1-022-f1, ragbench-v1-022-f2

> The process of pushing a post to all the followers is called a fanout. By analogy, the 
> push approach is called fanout-on-write, while the pull approach is called fanout-on-
> load. Let’s discuss different options for publishing feed data to users. 
> 1. “Pull” model or Fan-out-on-load: This method involves keeping all the 
> recent feed data in memory so that users can pull it from the server whenever 
> they need it. Clients can pull the feed data on a regular basis or manually 
> whenever they need it. Possible problems with this approach are a) New data 
> might not be shown to the users until they issue a pull request, b) It’s hard to 
> find the right pull cadence, as most of the time pull requests will result in an 
> empty response if there is no new data, causing waste of resources. 
> 2. “Push” model or Fan-out-on-write: For a push system, once a user has 
> published a post, we can immediately push this post to all the followers. The 
> advantage is that when fetching feed you don’t need to go through your 
> friend’s list and get feeds for each of them. It significantly reduces read 
> operations. To efficiently handle this, users have to maintain a Long 
> Poll request with the server for receiving the updates. A possible problem with 
> this approach is that when a user has millions of followers (a celebrity-user) 
> the server has to push updates to a lot of people.

- `ragbench-v1-022-e2` — `Grokking-the-system-design-interview-free.pdf`, PDF page 135 (printed label 135); supports ragbench-v1-022-f3

> 3. Hybrid: An alternate method to handle feed data could be to use a hybrid 
> approach, i.e., to do a combination of fan-out-on-write and fan-out-on-load. 
> Specifically, we can stop pushing posts from users with a high number of 
> followers (a celebrity user) and only push data for those users who have a few 
> hundred (or thousand) followers. For celebrity users, we can let the followers 
> pull the updates. Since the push operation can be extremely costly for users 
> who have a lot of friends or followers, by disabling fanout for them, we can 
> save a huge number of resources. Another alternate approach could be that, 
> once a user publishes a post, we can limit the fanout to only her online friends. 
> Also, to get benefits from both the approaches, a combination of ‘push to 
> notify’ and ‘pull for serving’ end users is a great way to go. Purely a push or 
> pull model is less versatile.

**Required evidence groups:**

- `ragbench-v1-022-g1`: any one of [ragbench-v1-022-e1] supports ragbench-v1-022-f1.
- `ragbench-v1-022-g2`: any one of [ragbench-v1-022-e1] supports ragbench-v1-022-f2.
- `ragbench-v1-022-g3`: any one of [ragbench-v1-022-e2] supports ragbench-v1-022-f3.

**Terminology examples:**

- fanout-on-write: fan-out-on-write, push model, precomputed feed
- fanout-on-load: fan-out-on-load, pull model, read-time feed assembly

**Verified distractors:**

- `ragbench-v1-022-d1` — `Designing Data-Intensive Applications.pdf`, PDF page 35 (printed label 13): This other PDF independently describes a similar celebrity hybrid. It is topically compelling but inadmissible because the question explicitly restricts the answer to the Grokking PDF.

> The final twist of the Twitter anecdote: now that approach 2 is robustly implemented,
> Twitter is moving to a hybrid of both approaches. Most users’ tweets continue to be
> fanned out to home timelines at the time when they are posted, but a small number
> of users with a very large number of followers (i.e., celebrities) are excepted from this
> fan-out. Tweets from any celebrities that a user may follow are fetched separately and
> merged with that user’s home timeline when it is read, like in approach 1. This hybrid
> approach is able to deliver consistently good performance.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-023

**Question:** Which client-side typeahead behaviors are recommended to avoid needless requests while a user is still typing?

**Category / difficulty:** `direct_factual_lookup` / `easy`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The client should wait until no key has been pressed for 50 ms before contacting the server, cancel an in-progress request if typing continues, and initially wait for a couple of characters.

**Required facts:**

- `ragbench-v1-023-f1`: The client waits for 50 ms of keyboard inactivity before contacting the server. (evidence: ragbench-v1-023-e1)
- `ragbench-v1-023-f2`: Continued typing cancels in-progress requests. (evidence: ragbench-v1-023-e1)
- `ragbench-v1-023-f3`: The client can wait for a couple of initial characters before requesting suggestions. (evidence: ragbench-v1-023-e1)

**Evidence:**

- `ragbench-v1-023-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 99 (printed label 99); supports ragbench-v1-023-f1, ragbench-v1-023-f2, ragbench-v1-023-f3

> We can perform the following optimizations on the client to improve user’s 
> experience: 
> 1. The client should only try hitting the server if the user has not pressed any key 
> for 50ms. 
> 2. If the user is constantly typing, the client can cancel the in-progress requests. 
> 3. Initially, the client can wait until the user enters a couple of characters.

**Required evidence groups:**

- `ragbench-v1-023-g1`: any one of [ragbench-v1-023-e1] supports ragbench-v1-023-f1.
- `ragbench-v1-023-g2`: any one of [ragbench-v1-023-e1] supports ragbench-v1-023-f2.
- `ragbench-v1-023-g3`: any one of [ragbench-v1-023-e1] supports ragbench-v1-023-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-024

**Question:** Once a relational database is sharded, why are cross-shard joins and foreign-key enforcement difficult, and what workarounds are proposed?

**Category / difficulty:** `limitations_and_exceptions` / `medium`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Cross-shard joins require collecting data from multiple servers and are inefficient, so denormalization can move formerly joined data into one table, at the cost of possible inconsistency. Cross-database foreign keys are often unsupported, so applications enforce referential integrity themselves and may run cleanup SQL jobs for dangling references.

**Required facts:**

- `ragbench-v1-024-f1`: Cross-shard joins are inefficient because data must be compiled from multiple servers. (evidence: ragbench-v1-024-e1)
- `ragbench-v1-024-f2`: Denormalization can avoid joins but introduces data-inconsistency risks. (evidence: ragbench-v1-024-e1)
- `ragbench-v1-024-f3`: Applications may enforce cross-shard referential integrity and clean dangling references because many RDBMSs do not support cross-server foreign keys. (evidence: ragbench-v1-024-e1)

**Evidence:**

- `ragbench-v1-024-e1` — `Grokking-the-system-design-interview-free.pdf`, PDF page 180 (printed label 180); supports ragbench-v1-024-f1, ragbench-v1-024-f2, ragbench-v1-024-f3

> 3. Common Problems of Sharding 
> On a sharded database there are certain extra constraints on the different operations 
> that can be performed. Most of these constraints are due to the fact that operations 
> across multiple tables or multiple rows in the same table will no longer run on the 
> same server. Below are some of the constraints and additional complexities 
> introduced by sharding: 
> a. Joins and Denormalization: Performing joins on a database which is running on 
> one server is straightforward, but once a database is partitioned and spread across 
> multiple machines it is often not feasible to perform joins that span database shards. 
> Such joins will not be performance efficient since data has to be compiled from 
> multiple servers. A common workaround for this problem is to denormalize the 
> database so that queries that previously required joins can be performed from a 
> single table. Of course, the service now has to deal with all the perils of 
> denormalization such as data inconsistency. 
> b. Referential integrity: As we saw that performing a cross-shard query on a 
> partitioned database is not feasible, similarly, trying to enforce data integrity 
> constraints such as foreign keys in a sharded database can be extremely difficult. 
> Most of RDBMS do not support foreign keys constraints across databases on 
> different database servers. Which means that applications that require referential 
> integrity on sharded databases often have to enforce it in application code. Often in 
> such cases, applications have to run regular SQL jobs to clean up dangling 
> references.

**Required evidence groups:**

- `ragbench-v1-024-g1`: any one of [ragbench-v1-024-e1] supports ragbench-v1-024-f1.
- `ragbench-v1-024-g2`: any one of [ragbench-v1-024-e1] supports ragbench-v1-024-f2.
- `ragbench-v1-024-g3`: any one of [ragbench-v1-024-e1] supports ragbench-v1-024-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-025

**Question:** In the reference entry for Add Two Numbers, how are the integers represented, what form must the result take, and what typical complexity is targeted?

**Category / difficulty:** `source_specific_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The two non-negative integers are encoded as reverse-order linked lists, and the sum is returned in the same representation. The typical target is O(m+n) time and O(1) auxiliary space.

**Required facts:**

- `ragbench-v1-025-f1`: The inputs are non-negative integers encoded in reverse-order linked lists, and the output uses the same representation. (evidence: ragbench-v1-025-e1)
- `ragbench-v1-025-f2`: The typical target is O(m+n) time and O(1) auxiliary space. (evidence: ragbench-v1-025-e1)

**Evidence:**

- `ragbench-v1-025-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 162 (printed label 162); supports ragbench-v1-025-f1, ragbench-v1-025-f2

> 2. Add Two Numbers
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Add two non-negative integers encoded in reverse-order linked lists and return the sum in the same representation.
> Key concepts:
> Linked list; carry handling; simulation
> Typical target:
> O(m+n) time, O(1) auxiliary space

**Required evidence groups:**

- `ragbench-v1-025-g1`: any one of [ragbench-v1-025-e1] supports ragbench-v1-025-f1.
- `ragbench-v1-025-g2`: any one of [ragbench-v1-025-e1] supports ragbench-v1-025-f2.

**Verified distractors:**

- `ragbench-v1-025-d1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 310 (printed label 310): This is the similarly named Add Two Numbers II entry, not problem 2, and it does not state the reverse-order representation asked about.

> 445. Add Two Numbers II
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Solve the algorithmic task described by 'Add Two Numbers II', with the main study focus on Linked List, Math.
> Key concepts:
> Linked List; Math; Stack
> Typical target:
> Typically O(n) time with O(1) auxiliary space unless recursion or extra indexing is used

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-026

**Question:** Which technique and data structures does the reference associate with finding the longest substring that has no repeated characters?

**Category / difficulty:** `source_specific_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** It associates the task with a sliding window, a hash map or set, and two pointers; the target is O(n) time and O(k) space.

**Required facts:**

- `ragbench-v1-026-f1`: The task uses a sliding window, hash map/set, and two pointers. (evidence: ragbench-v1-026-e1)
- `ragbench-v1-026-f2`: The typical target is O(n) time and O(k) space. (evidence: ragbench-v1-026-e1)

**Evidence:**

- `ragbench-v1-026-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 162 (printed label 162); supports ragbench-v1-026-f1, ragbench-v1-026-f2

> 3. Longest Substring Without Repeating Characters
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Determine the maximum length of a contiguous substring containing no repeated characters.
> Key concepts:
> Sliding window; hash map/set; two pointers
> Typical target:
> O(n) time, O(k) space

**Required evidence groups:**

- `ragbench-v1-026-g1`: any one of [ragbench-v1-026-e1] supports ragbench-v1-026-f1.
- `ragbench-v1-026-g2`: any one of [ragbench-v1-026-e1] supports ragbench-v1-026-f2.

**Terminology examples:**

- Longest Substring Without Repeating Characters: longest unique-character substring, non-repeating contiguous substring, sliding-window substring

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-027

**Question:** What runtime and space target does the reference give for computing the median of two sorted arrays?

**Category / difficulty:** `numerical_factual_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** It gives O(log min(m,n)) time and O(1) space, with binary search and partitioning as the key concepts.

**Required facts:**

- `ragbench-v1-027-f1`: The typical runtime is O(log min(m,n)) with O(1) space. (evidence: ragbench-v1-027-e1)
- `ragbench-v1-027-f2`: The associated concepts are binary search, partitioning, and sorted arrays. (evidence: ragbench-v1-027-e1)

**Evidence:**

- `ragbench-v1-027-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 163 (printed label 163); supports ragbench-v1-027-f1, ragbench-v1-027-f2

> 4. Median of Two Sorted Arrays
> HARD
> |
> Open on LeetCode
> Summary:
> Compute the median of two sorted arrays while meeting a logarithmic-time requirement.
> Key concepts:
> Binary search; partitioning; sorted arrays
> Typical target:
> O(log min(m,n)) time, O(1) space

**Required evidence groups:**

- `ragbench-v1-027-g1`: any one of [ragbench-v1-027-e1] supports ragbench-v1-027-f1.
- `ragbench-v1-027-g2`: any one of [ragbench-v1-027-e1] supports ragbench-v1-027-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-028

**Question:** What special correctness condition accompanies reversing a signed integer, and what typical complexity does the reference target?

**Category / difficulty:** `source_specific_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The reversed decimal digits must remain safe under signed 32-bit overflow handling. The typical target is O(log |x|) time and O(1) space.

**Required facts:**

- `ragbench-v1-028-f1`: Reversing the digits must safely handle signed 32-bit overflow. (evidence: ragbench-v1-028-e1)
- `ragbench-v1-028-f2`: The typical target is O(log |x|) time and O(1) space. (evidence: ragbench-v1-028-e1)

**Evidence:**

- `ragbench-v1-028-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 164 (printed label 164); supports ragbench-v1-028-f1, ragbench-v1-028-f2

> 7. Reverse Integer
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Reverse the decimal digits of a signed 32-bit integer while safely handling overflow.
> Key concepts:
> Math; digit extraction; overflow checks
> Typical target:
> O(log |x|) time, O(1) space

**Required evidence groups:**

- `ragbench-v1-028-g1`: any one of [ragbench-v1-028-e1] supports ragbench-v1-028-f1.
- `ragbench-v1-028-g2`: any one of [ragbench-v1-028-e1] supports ragbench-v1-028-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-029

**Question:** For Regular Expression Matching, does the reference ask for a partial or full-string match, which pattern operators are named, and what typical bound is listed?

**Category / difficulty:** `multi_fact_lookup` / `medium`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** It asks whether the entire string matches a pattern with dot and star semantics. The typical target is O(mn) time and O(mn) space, usually using dynamic programming or recursion/memoization.

**Required facts:**

- `ragbench-v1-029-f1`: The task is full-string matching, not partial matching. (evidence: ragbench-v1-029-e1)
- `ragbench-v1-029-f2`: The pattern supports dot and star semantics. (evidence: ragbench-v1-029-e1)
- `ragbench-v1-029-f3`: The typical target is O(mn) time and O(mn) space. (evidence: ragbench-v1-029-e1)

**Evidence:**

- `ragbench-v1-029-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 165 (printed label 165); supports ragbench-v1-029-f1, ragbench-v1-029-f2, ragbench-v1-029-f3

> 10. Regular Expression Matching
> HARD
> |
> Open on LeetCode
> Summary:
> Check whether an entire string matches a pattern supporting dot and star semantics.
> Key concepts:
> Dynamic programming; recursion/memoization; pattern matching
> Typical target:
> O(mn) time, O(mn) space typical

**Required evidence groups:**

- `ragbench-v1-029-g1`: any one of [ragbench-v1-029-e1] supports ragbench-v1-029-f1.
- `ragbench-v1-029-g2`: any one of [ragbench-v1-029-e1] supports ragbench-v1-029-f2.
- `ragbench-v1-029-g3`: any one of [ragbench-v1-029-e1] supports ragbench-v1-029-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-030

**Question:** What output uniqueness requirement and typical time target are stated for 4Sum?

**Category / difficulty:** `source_specific_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The result must contain all unique quadruples whose values equal the requested target. The listed typical runtime is O(n^3).

**Required facts:**

- `ragbench-v1-030-f1`: 4Sum returns unique value quadruples that sum to the target. (evidence: ragbench-v1-030-e1)
- `ragbench-v1-030-f2`: The typical target is O(n^3) time. (evidence: ragbench-v1-030-e1)

**Evidence:**

- `ragbench-v1-030-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 167 (printed label 167); supports ragbench-v1-030-f1, ragbench-v1-030-f2

> 18. 4Sum
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Return all unique quadruples whose values sum to the requested target.
> Key concepts:
> Sorting; two pointers; k-sum; pruning
> Typical target:
> O(n^3) time typical

**Required evidence groups:**

- `ragbench-v1-030-g1`: any one of [ragbench-v1-030-e1] supports ragbench-v1-030-f1.
- `ragbench-v1-030-g2`: any one of [ragbench-v1-030-e1] supports ragbench-v1-030-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-031

**Question:** What pointer strategy and resource target are listed for removing the nth node counted from the end of a singly linked list?

**Category / difficulty:** `source_specific_lookup` / `easy`

**Allowed sources:** LeetCode_4000_Problem_Reference.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The entry lists fast/slow pointers with a dummy node, targeting O(n) time and O(1) space.

**Required facts:**

- `ragbench-v1-031-f1`: The listed technique uses fast/slow pointers and a dummy node. (evidence: ragbench-v1-031-e1)
- `ragbench-v1-031-f2`: The typical target is O(n) time and O(1) space. (evidence: ragbench-v1-031-e1)

**Evidence:**

- `ragbench-v1-031-e1` — `LeetCode_4000_Problem_Reference.pdf`, PDF page 168 (printed label 168); supports ragbench-v1-031-f1, ragbench-v1-031-f2

> 19. Remove Nth Node From End of List
> MEDIUM
> |
> Open on LeetCode
> Summary:
> Delete the node located n positions from the end of a singly linked list.
> Key concepts:
> Linked list; fast/slow pointers; dummy node
> Typical target:
> O(n) time, O(1) space

**Required evidence groups:**

- `ragbench-v1-031-g1`: any one of [ragbench-v1-031-e1] supports ragbench-v1-031-f1.
- `ragbench-v1-031-g2`: any one of [ragbench-v1-031-e1] supports ragbench-v1-031-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-032

**Question:** What question does a posterior predictive check ask, and how does it use synthetic datasets and test statistics to diagnose a poor model?

**Category / difficulty:** `method_explanation` / `medium`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** It asks whether observed data look typical of data expected under the fitted model. Synthetic future datasets are drawn from the posterior predictive distribution, selected scalar test statistics are computed for them and the observed data, and a large discrepancy indicates that the model may be poor.

**Required facts:**

- `ragbench-v1-032-f1`: Model checking asks whether observed data are typical of what the model would generate if it were correct. (evidence: ragbench-v1-032-e1)
- `ragbench-v1-032-f2`: A posterior predictive check generates synthetic future datasets from the posterior predictive distribution. (evidence: ragbench-v1-032-e2)
- `ragbench-v1-032-f3`: Selected scalar test statistics on synthetic datasets are compared with the statistic on the observed data. (evidence: ragbench-v1-032-e3)
- `ragbench-v1-032-f4`: A large discrepancy between the synthetic-statistic distribution and the observed statistic suggests a poor model. (evidence: ragbench-v1-032-e3)

**Evidence:**

- `ragbench-v1-032-e1` — `Probabilistic Machine Learning.pdf`, PDF page 162 (printed label 128); supports ragbench-v1-032-f1

> Instead we are just trying to see if the data we observe is “typical” of
> what we might expect if our model were correct. This is calledmodel checking.

- `ragbench-v1-032-e2` — `Probabilistic Machine Learning.pdf`, PDF page 162 (printed label 128); supports ragbench-v1-032-f2

> To evaluate how good a candidate modelM is, after seeing some dataD, we can imagine using the
> model to generate synthetic future datasets, by drawing from the posterior predictive distribution:

- `ragbench-v1-032-e3` — `Probabilistic Machine Learning.pdf`, PDF page 162 (printed label 128); supports ragbench-v1-032-f3, ragbench-v1-032-f4

> These represent “plausible hallucinations” of the model. To assess the quality of our model, we can
> compute how “typical” our observed dataD is compared to the model’s hallucinations. To perform
> this comparison, we create one or more scalartest statistics,test( ˜Ds), and compare them to the
> test statistics on the actual data,test(D). These statistics should measure features of interest (since
> it will not, in general, be possible to capture every aspect of the data with a given model). If there is
> a large difference between the distribution oftest( ˜Ds)across different s and the value oftest(D), it
> suggests the model is not a good one. This approach called aposterior predictive check[Rub84].

**Required evidence groups:**

- `ragbench-v1-032-g1`: any one of [ragbench-v1-032-e1] supports ragbench-v1-032-f1.
- `ragbench-v1-032-g2`: any one of [ragbench-v1-032-e2] supports ragbench-v1-032-f2.
- `ragbench-v1-032-g3`: any one of [ragbench-v1-032-e3] supports ragbench-v1-032-f3.
- `ragbench-v1-032-g4`: any one of [ragbench-v1-032-e3] supports ragbench-v1-032-f4.

**Terminology examples:**

- posterior predictive check: posterior predictive check, posterior-predictive model check, model checking with posterior predictive data

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-033

**Question:** Why does minimizing forward KL tend to cover modes while minimizing reverse KL tends to select modes?

**Category / difficulty:** `technical_distinction` / `hard`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Forward/inclusive KL, DKL(p∥q), becomes infinite unless q is positive wherever p is positive, encouraging q to cover p's modes (zero-avoiding). Reverse/exclusive KL, DKL(q∥p), becomes infinite unless q is zero wherever p is zero, encouraging q to select modes and avoid unsupported regions (zero-forcing).

**Required facts:**

- `ragbench-v1-033-f1`: DKL(p∥q) is called inclusive or forwards KL, while DKL(q∥p) is called exclusive or reverse KL. (evidence: ragbench-v1-033-e1)
- `ragbench-v1-033-f2`: Forwards KL requires q to have support wherever p does and therefore has mode-covering or zero-avoiding behavior. (evidence: ragbench-v1-033-e2)
- `ragbench-v1-033-f3`: Reverse KL requires q to vanish where p vanishes and therefore has mode-seeking or zero-forcing behavior. (evidence: ragbench-v1-033-e3)

**Evidence:**

- `ragbench-v1-033-e1` — `Probabilistic Machine Learning.pdf`, PDF page 259 (printed label 225); supports ragbench-v1-033-f1

> The asymmetry of KL means that finding aq that is close top by minimizingDKL (p∥q) (also
> called theinclusive KLorforwards KL) gives different behavior than minimizing DKL (q∥p)
> (also called theexclusive KLorreverse KL).

- `ragbench-v1-033-e2` — `Probabilistic Machine Learning.pdf`, PDF page 259 (printed label 225); supports ragbench-v1-033-f2

> To preventDKL (p∥q) from becoming infinite, we must haveq > 0whenever p > 0(i.e., q
> must have support everywherep does), soq tends tocoverboth modes as it must be nonvanishing
> everywhere p is; this is calledmode-coveringorzero-avoidingbehavior

- `ragbench-v1-033-e3` — `Probabilistic Machine Learning.pdf`, PDF page 259 (printed label 225); supports ragbench-v1-033-f3

> By
> contrast, to preventDKL (q∥p) from becoming infinite, we must haveq = 0whenever p = 0, which
> createsmode-seekingorzero-forcingbehavior

**Required evidence groups:**

- `ragbench-v1-033-g1`: any one of [ragbench-v1-033-e1] supports ragbench-v1-033-f1.
- `ragbench-v1-033-g2`: any one of [ragbench-v1-033-e2] supports ragbench-v1-033-f2.
- `ragbench-v1-033-g3`: any one of [ragbench-v1-033-e3] supports ragbench-v1-033-f3.

**Terminology examples:**

- forwards KL: forward KL, inclusive KL, DKL(p||q), mode-covering, zero-avoiding
- reverse KL: exclusive KL, DKL(q||p), mode-seeking, zero-forcing

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-034

**Question:** In reparameterized variational inference, how is randomness separated from the variational parameters, and what does that enable?

**Category / difficulty:** `method_explanation` / `medium`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A draw from the parameterized latent distribution is rewritten as a differentiable, invertible transformation of noise whose distribution does not depend on the variational parameters. This enables gradients to propagate back through the transformation and is called reparameterized variational inference (RVI).

**Required facts:**

- `ragbench-v1-034-f1`: The latent draw is rewritten as a differentiable, invertible transformation of noise whose distribution does not depend on the variational parameters. (evidence: ragbench-v1-034-e1)
- `ragbench-v1-034-f2`: The rewrite allows gradients to propagate back through the transformation and is called reparameterized VI or RVI. (evidence: ragbench-v1-034-e2)

**Evidence:**

- `ragbench-v1-034-e1` — `Probabilistic Machine Learning.pdf`, PDF page 481 (printed label 447); supports ragbench-v1-034-f1

> The key trick is to rewrite the random variablez∼q ϕ(z|x)as some differentiable (and invertible)
> transformation g of another random variableϵ∼p (ϵ), which does not depend onϕ

- `ragbench-v1-034-e2` — `Probabilistic Machine Learning.pdf`, PDF page 481 (printed label 447); supports ragbench-v1-034-f2

> This lets us propagate gradients back
> through theffunction. See Figure 10.4 for an illustration. This is calledreparameterized VIor
> RVI.

**Required evidence groups:**

- `ragbench-v1-034-g1`: any one of [ragbench-v1-034-e1] supports ragbench-v1-034-f1.
- `ragbench-v1-034-g2`: any one of [ragbench-v1-034-e2] supports ragbench-v1-034-f2.

**Terminology examples:**

- reparameterization trick: reparameterized VI, RVI, reparameterization trick

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-035

**Question:** Why must HMC resample momentum on every iteration, and what problem does NUTS solve?

**Category / difficulty:** `multi_fact_lookup` / `hard`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** HMC approximately preserves Hamiltonian energy along a trajectory, so fixed momentum would keep the sampler from reaching states above that energy; new random momentum is needed for ergodicity and full-space exploration. NUTS adaptively chooses the number of leapfrog steps L so exploration is long enough without doubling back and wasting computation through correlated samples.

**Required facts:**

- `ragbench-v1-035-f1`: HMC resamples momentum for ergodicity because approximately constant trajectory energy otherwise restricts reachable states. (evidence: ragbench-v1-035-e1)
- `ragbench-v1-035-f2`: NUTS adaptively selects leapfrog count L to explore without doubling back and wasting computation with correlated samples. (evidence: ragbench-v1-035-e1)

**Evidence:**

- `ragbench-v1-035-e1` — `Probabilistic Machine Learning.pdf`, PDF page 554 (printed label 520); supports ragbench-v1-035-f1, ragbench-v1-035-f2

> We need to sample a new momentum at each iteration to satisfy ergodicity. To see why, recall that
> H(θ,v )stays approximately constant as we move through phase space. IfH(θ,v ) =E(θ) + 1
> 2vTΣv,
> then clearlyE(θ)≤H (θ,v ) =h for all locationsθ along the trajectory. Thus the sampler cannot
> reach states whereE(θ)>h . To ensure the sampler explores the full space, we must pick a random
> momentum at the start of each iteration.
> 12.5.4 Tuning HMC
> We need to specify three hyperparameters for HMC: the number of leapfrog stepsL, the step sizeη,
> and the covarianceΣ.
> 12.5.4.1 Choosing the number of steps using NUTS
> We want to choose the number of leapfrog stepsL to be large enough that the algorithm explores
> the level set of constant energy, but without doubling back on itself, which would waste computation,
> due to correlated samples. Fortunately, there is an algorithm, known as theno-U-turn sampleror
> NUTSalgorithm [HG14], which can adaptively chooseLfor us.

**Required evidence groups:**

- `ragbench-v1-035-g1`: any one of [ragbench-v1-035-e1] supports ragbench-v1-035-f1.
- `ragbench-v1-035-g2`: any one of [ragbench-v1-035-e1] supports ragbench-v1-035-f2.

**Terminology examples:**

- Hamiltonian Monte Carlo: HMC, Hamiltonian MCMC
- no-U-turn sampler: NUTS, adaptive leapfrog-step selection

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-036

**Question:** What happens when HMC's step size is too large or too small, and what acceptance-rate tuning range is recommended for the stated L=1, identity-mass setup?

**Category / difficulty:** `conditional_claim` / `medium`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A too-large step size proposes moves that raise potential energy and are likely to be rejected; a too-small step size barely moves and makes sampling slow. With Σ=I and L=1, the cited heuristic varies η until acceptance is between 40% and 80%.

**Required facts:**

- `ragbench-v1-036-f1`: An overly large HMC step is likely to be rejected because it can raise potential energy too much. (evidence: ragbench-v1-036-e1)
- `ragbench-v1-036-f2`: An overly small step moves little and makes the algorithm slow. (evidence: ragbench-v1-036-e1)
- `ragbench-v1-036-f3`: For Σ=I and L=1, the cited target acceptance range is 40%–80%. (evidence: ragbench-v1-036-e2)

**Evidence:**

- `ragbench-v1-036-e1` — `Probabilistic Machine Learning.pdf`, PDF page 554 (printed label 520); supports ragbench-v1-036-f1, ragbench-v1-036-f2

> When Σ =I, the ideal step sizeη should be roughly equal to the width ofE(θ)in the most constrained
> direction of the local energy landscape. For a locally quadratic potential, this corresponds to the
> square root of the smallest marginal standard deviation of the local covariance matrix. (If we think
> of the energy surface as a valley, this corresponds to the direction with the steepest sides.) A step
> size much larger than this will cause moves that are likely to be rejected because they move to places
> which increase the potential energy too much. On the other hand, if the step size is too low, the
> proposal distribution will not move much from the starting position, and the algorithm will be very
> slow.

- `ragbench-v1-036-e2` — `Probabilistic Machine Learning.pdf`, PDF page 555 (printed label 521); supports ragbench-v1-036-f3

> In [BZ20, Sec 9.5.4] they recommend the following heuristic for pickingη: set Σ =Iand L = 1,
> and then varyη until the acceptance rates are in the range of 40%–80%.

**Required evidence groups:**

- `ragbench-v1-036-g1`: any one of [ragbench-v1-036-e1] supports ragbench-v1-036-f1.
- `ragbench-v1-036-g2`: any one of [ragbench-v1-036-e1] supports ragbench-v1-036-f2.
- `ragbench-v1-036-g3`: any one of [ragbench-v1-036-e2] supports ragbench-v1-036-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-037

**Question:** Which structural property lets a normalizing flow both sample and evaluate exact likelihood efficiently?

**Category / difficulty:** `direct_factual_lookup` / `medium`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A normalizing flow maps a sample from a simple base distribution through a nonlinear, invertible transformation. The forward transformation makes sampling straightforward, and invertibility enables efficient exact-density evaluation.

**Required facts:**

- `ragbench-v1-037-f1`: Normalizing flows are described as easy to sample from and efficient for exact-likelihood computation. (evidence: ragbench-v1-037-e1)
- `ragbench-v1-037-f2`: A normalizing flow passes a sample from a simple base distribution through a nonlinear, invertible transformation. (evidence: ragbench-v1-037-e2)
- `ragbench-v1-037-f3`: Sampling uses the forward transformation, while density computation relies on invertibility. (evidence: ragbench-v1-037-e3)

**Evidence:**

- `ragbench-v1-037-e1` — `Probabilistic Machine Learning.pdf`, PDF page 863 (printed label 829); supports ragbench-v1-037-f1

> In this chapter we discussnormalizing flows, a class of flexible density models that can be
> easily sampled from and whose exact likelihood function is efficient to compute. Such models
> can be used for many tasks, such as density modeling, inference and generative modeling.

- `ragbench-v1-037-e2` — `Probabilistic Machine Learning.pdf`, PDF page 863 (printed label 829); supports ragbench-v1-037-f2

> Normalizing flows create complex probability distributionsp(x)by passing random variablesu∈R D,
> drawn from a simplebase distributionp(u)through a nonlinear butinvertibletransformation
> f:R D→R D. That is,p(x)is defined by the following process:

- `ragbench-v1-037-e3` — `Probabilistic Machine Learning.pdf`, PDF page 863 (printed label 829); supports ragbench-v1-037-f3

> Sampling fromp(x)is straightforward: we first sampleu from p(u)and then computex =f(u).
> To compute the densityp(x), we rely on the fact thatf is invertible.

**Required evidence groups:**

- `ragbench-v1-037-g1`: any one of [ragbench-v1-037-e1] supports ragbench-v1-037-f1.
- `ragbench-v1-037-g2`: any one of [ragbench-v1-037-e2] supports ragbench-v1-037-f2.
- `ragbench-v1-037-g3`: any one of [ragbench-v1-037-e3] supports ragbench-v1-037-f3.

**Terminology examples:**

- normalizing flows: flow-based density model, invertible density model, change-of-variables model

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-038

**Question:** How do the tractability requirements for a normalizing flow differ between density estimation and variational inference?

**Category / difficulty:** `method_comparison` / `hard`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Density estimation requires efficient evaluation of the inverse flow and its Jacobian determinant; generating samples additionally requires a tractable forward map. Variational inference uses a flow to parameterize an approximate posterior, trains it by maximizing the ELBO, and uses reparameterization to optimize with stochastic gradients.

**Required facts:**

- `ragbench-v1-038-f1`: Density estimation requires efficient inverse-flow and Jacobian-determinant evaluation, while later generation requires a tractable forward map. (evidence: ragbench-v1-038-e1)
- `ragbench-v1-038-f2`: Variational inference parameterizes an approximate posterior with the flow and trains the variational parameters by maximizing the ELBO. (evidence: ragbench-v1-038-e2)
- `ragbench-v1-038-f3`: The reparameterization trick allows the flow parameters to be optimized with stochastic gradients. (evidence: ragbench-v1-038-e3)

**Evidence:**

- `ragbench-v1-038-e1` — `Probabilistic Machine Learning.pdf`, PDF page 865 (printed label 831); supports ragbench-v1-038-f1

> Density estimation requires maximizing the likelihood function in Equation (23.2). This requires that
> we can efficiently evaluate the inverse flowu =f−1(x)and its Jacobian determinant det J(f−1)(x)
> for any givenx. After optimizing the model, we can optionally use it to generate new data. To
> sample new points, we require that the forwards mappingfbe tractable.

- `ragbench-v1-038-e2` — `Probabilistic Machine Learning.pdf`, PDF page 865 (printed label 831); supports ragbench-v1-038-f2

> Normalizing flows are commonly used for variational inference to parameterize the approximate
> posterior distribution in latent variable models, as discussed in Section 10.4.3. Consider a latent
> variable model with continuous latent variablesz and observable variablesx. For simplicity, we
> consider the model parameters to be fixed as we are interested in approximating the true posterior
> p∗(z|x)with a normalizing flowqθ(z|x).1 As discussed in Section 10.1.1.2, the variational parameters
> are trained by maximizing the evidence lower bound (ELBO)

- `ragbench-v1-038-e3` — `Probabilistic Machine Learning.pdf`, PDF page 865 (printed label 831); supports ragbench-v1-038-f3

> Letqθ(z)denote a normalizing flow with base distributionq(u)and transformation z =fθ(u). Then
> the reparameterization trick (Section 6.3.5) allows us to optimize the parameters using stochastic
> gradients.

**Required evidence groups:**

- `ragbench-v1-038-g1`: any one of [ragbench-v1-038-e1] supports ragbench-v1-038-f1.
- `ragbench-v1-038-g2`: any one of [ragbench-v1-038-e2] supports ragbench-v1-038-f2.
- `ragbench-v1-038-g3`: any one of [ragbench-v1-038-e3] supports ragbench-v1-038-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-039

**Question:** For Gaussian-process time-series forecasting, how can inference cost change for suitable stationary kernels, and which kernel families permit exact versus approximate conversion?

**Category / difficulty:** `numerical_factual_lookup` / `medium`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Naive GP forecasting costs O(T^3). For certain stationary kernels it can be reformulated as a linear-Gaussian state-space model and solved with a Kalman smoother in O(T). The conversion is exact for Matérn kernels and approximate for Gaussian/RBF kernels.

**Required facts:**

- `ragbench-v1-039-f1`: Naive GP time-series forecasting costs O(T^3), while a state-space/Kalman formulation can cost O(T) for certain stationary kernels. (evidence: ragbench-v1-039-e1)
- `ragbench-v1-039-f2`: The state-space conversion is exact for Matérn kernels and approximate for Gaussian/RBF kernels. (evidence: ragbench-v1-039-e1)

**Evidence:**

- `ragbench-v1-039-e1` — `Probabilistic Machine Learning.pdf`, PDF page 766 (printed label 732); supports ragbench-v1-039-f1, ragbench-v1-039-f2

> It is possible to use Gaussian processes to perform time series forecasting (see e.g., [Rob+13]). The
> basic idea is to model the unknown output as a function of time,f(t), and to represent a prior about
> the form off as a GP; we then update this prior given the observed evidence, and forecast into the
> future. Naively this would takeO(T 3)time. However, for certain stationary kernels, it is possible to
> reformulate the problem as a linear-Gaussian state space model, and then use the Kalman smoother
> to perform inference inO(T )time, as explained in [SSH13; SS19; Ada+20]. This conversion can be
> done exactly for Matérn kernels and approximately for Gaussian (RBF) kernels

**Required evidence groups:**

- `ragbench-v1-039-g1`: any one of [ragbench-v1-039-e1] supports ragbench-v1-039-f1.
- `ragbench-v1-039-g2`: any one of [ragbench-v1-039-e1] supports ragbench-v1-039-f2.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-040

**Question:** What failure of raw likelihood is reported for unsupervised out-of-distribution detection, what replacement is proposed, and what invariance advantage does it have?

**Category / difficulty:** `limitations_and_exceptions` / `hard`

**Allowed sources:** Probabilistic Machine Learning.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** A deep density model can assign lower likelihood to samples from its source distribution than to samples from a novel target distribution. A log-likelihood ratio against a baseline density is proposed instead of raw likelihood, and the ratio is invariant to transformations of the data.

**Required facts:**

- `ragbench-v1-040-f1`: A deep density model can assign lower likelihood to source-distribution samples than to novel-target samples. (evidence: ragbench-v1-040-e1)
- `ragbench-v1-040-f2`: A log-likelihood ratio relative to a baseline density is proposed instead of raw likelihood. (evidence: ragbench-v1-040-e2)
- `ragbench-v1-040-f3`: The log-likelihood ratio is invariant to transformations of the data. (evidence: ragbench-v1-040-e3)

**Evidence:**

- `ragbench-v1-040-e1` — `Probabilistic Machine Learning.pdf`, PDF page 777 (printed label 743); supports ragbench-v1-040-f1

> If we don’t have labeled examples, a natural approach to OOD detection is to fit an unconditional
> density model (such as a VAE) to the ID samples, and then to evaluate the likelihoodp(x)and
> compare this to some threshold value. Unfortunately for many kinds of deep model and datasets, we
> sometimes find thatp(x)is lower for samples that are from the source distribution than from a novel
> target distribution.

- `ragbench-v1-040-e2` — `Probabilistic Machine Learning.pdf`, PDF page 777 (printed label 743); supports ragbench-v1-040-f2

> One solution to this is to use alog likelihood ratiorelative to a baseline density model,
> R(x) = logp (x)/q(x), as opposed to the raw log likelihood

- `ragbench-v1-040-e3` — `Probabilistic Machine Learning.pdf`, PDF page 777 (printed label 743); supports ragbench-v1-040-f3

> An important advantage of this is that the ratio is
> invariant to transformations of the data.

**Required evidence groups:**

- `ragbench-v1-040-g1`: any one of [ragbench-v1-040-e1] supports ragbench-v1-040-f1.
- `ragbench-v1-040-g2`: any one of [ragbench-v1-040-e2] supports ragbench-v1-040-f2.
- `ragbench-v1-040-g3`: any one of [ragbench-v1-040-e3] supports ragbench-v1-040-f3.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-041

**Question:** How does BPE training grow its vocabulary, and what is the stopping parameter described in the text?

**Category / difficulty:** `method_explanation` / `easy`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** BPE begins with individual characters, repeatedly finds the most frequent adjacent token pair, merges it into a new longer token, and stops after k merges. Thus k controls how many new symbols are added beyond the original character set.

**Required facts:**

- `ragbench-v1-041-f1`: BPE starts with individual characters and repeatedly merges the most frequent neighboring token pair. (evidence: ragbench-v1-041-e1)
- `ragbench-v1-041-f2`: The parameter k is the number of merges and therefore the number of newly created symbols. (evidence: ragbench-v1-041-e1)

**Evidence:**

- `ragbench-v1-041-e1` — `Speech and Language Processing.pdf`, PDF page 51 (printed label 43); supports ragbench-v1-041-f1, ragbench-v1-041-f2

> TheBPEtraining algorithm iteratively merges frequent neighboring tokens to create
> longer and longer tokens. The algorithm begins with a vocabulary that is just the
> set of all individual characters. It then examines the training corpus, and finds the
> two characters that are most frequently adjacent. Imagine our original corpus is 10
> characters long, using a vocabulary of 5 characters,{A,B,C,D,E}:
> A B D C A B E C A B
> The most frequent neighboring pair of characters is “A B” so we merge those,
> add a new merged token ‘AB’ to the vocabulary, and replace every adjacent ‘A’ ‘B’
> in the corpus with the new ‘AB’:
> AB D C AB E C AB
> Now we have a vocabulary of 6 possible tokens{A,B,C,D,E,AB}, and the
> corpus has length 7. And now the most frequent pair of tokens is “C AB”, so we
> merge those, leading to a vocabulary with 7 tokens{A,B,C,D,E,AB,CAB}, and the
> corpus has length 5.
> AB D CAB E CAB
> The algorithm continues to count and merge, creating new longer and longer
> character strings, untilkmerges have been done creatingknovel tokens;kis thus a
> parameter of the algorithm. The resulting vocabulary consists of the original set of
> characters plusknew symbols. That’s the core of the algorithm.

**Required evidence groups:**

- `ragbench-v1-041-g1`: any one of [ragbench-v1-041-e1] supports ragbench-v1-041-f1.
- `ragbench-v1-041-g2`: any one of [ragbench-v1-041-e1] supports ragbench-v1-041-f2.

**Terminology examples:**

- byte-pair encoding: BPE, byte pair encoding, iterative frequent-pair merging

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-042

**Question:** How should language-model perplexity be interpreted, and why is it unsafe to compare perplexities from models with very different tokenizers?

**Category / difficulty:** `multi_passage_synthesis` / `hard`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Perplexity is the inverse probability assigned to a test set, normalized by its token count; lower perplexity means higher test-set probability and a better predictive model on that data. Because the normalization depends on the number of tokens, different tokenization algorithms can change the value, so perplexity is best compared between models using the same tokenizer.

**Required facts:**

- `ragbench-v1-042-f1`: Perplexity is inverse test-set probability normalized by the number of words or tokens. (evidence: ragbench-v1-042-e1)
- `ragbench-v1-042-f2`: Lower perplexity corresponds to higher assigned sequence probability and a better model on the data. (evidence: ragbench-v1-042-e2)
- `ragbench-v1-042-f3`: Perplexity depends on token count, so models with very different tokenizers are hard to compare exactly and same-tokenizer comparisons are safest. (evidence: ragbench-v1-042-e3)

**Evidence:**

- `ragbench-v1-042-e1` — `Speech and Language Processing.pdf`, PDF page 84 (printed label 76); supports ragbench-v1-042-f1

> Theperplexity(sometimes abbreviated as PP or PPL) of a language model on aperplexity
> test set is the inverse probability of the test set (one over the probability of the test
> set), normalized by the number of words (or tokens). For this reason it’s sometimes
> called the per-word or per-token perplexity. We normalize by the number of words
> Nby taking theNth root.

- `ragbench-v1-042-e2` — `Speech and Language Processing.pdf`, PDF page 84 (printed label 76); supports ragbench-v1-042-f2

> Note that because of the inverse in Eq. 3.15, the higher the probability of the word
> sequence, the lower the perplexity. Thusthe lower the perplexity of a model on
> the data, the better the model.

- `ragbench-v1-042-e3` — `Speech and Language Processing.pdf`, PDF page 211 (printed label 203); supports ragbench-v1-042-f3

> One caveat: because perplexity depends on the number of tokensnin a text, it
> is very sensitive to differences in the tokenization algorithm. That means that it’s
> hard to exactly compare perplexities produced by two language models if they have
> very different tokenizers. For this reason perplexity is best used when comparing
> language models that use the same tokenizer.

**Required evidence groups:**

- `ragbench-v1-042-g1`: any one of [ragbench-v1-042-e1] supports ragbench-v1-042-f1.
- `ragbench-v1-042-g2`: any one of [ragbench-v1-042-e2] supports ragbench-v1-042-f2.
- `ragbench-v1-042-g3`: any one of [ragbench-v1-042-e3] supports ragbench-v1-042-f3.

**Terminology examples:**

- perplexity: PP, PPL, per-token inverse probability

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-043

**Question:** What role does self-attention play in building a token's contextual representation?

**Category / difficulty:** `direct_factual_lookup` / `easy`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Self-attention attends to and integrates information from surrounding tokens, moving information between token-position residual streams and enriching each token representation with long-range contextual relationships.

**Required facts:**

- `ragbench-v1-043-f1`: Self-attention integrates information from other token positions to build contextual token representations and capture long-range relationships. (evidence: ragbench-v1-043-e1)

**Evidence:**

- `ragbench-v1-043-e1` — `Speech and Language Processing.pdf`, PDF page 186 (printed label 178); supports ragbench-v1-043-f1

> The core intuition of the transformer, and the component that distinguishes it
> from the feedforward layers we saw in Chapter 6, is this multi-head attention layer,
> also called aself-attentionlayer. Attention can be thought of as a way to build
> contextual representations of a token’s meaning byattending toand integrating
> information from surrounding tokens, helping the model learn how tokens relate to
> each other over large spans. It can also be thought of as a way to move information
> from one residual stream to another, augmenting the stream at one token position
> with information from another token position.

**Required evidence groups:**

- `ragbench-v1-043-g1`: any one of [ragbench-v1-043-e1] supports ragbench-v1-043-f1.

**Terminology examples:**

- self-attention: multi-head attention, attention layer, context integration

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, exact quote, semantic support, fact links, evidence groups, source restrictions, and terminology were verified.

## ragbench-v1-044

**Question:** In a transformer attention head, what are the query, key, and value roles, and why is the query-key dot product scaled?

**Category / difficulty:** `technical_distinction` / `medium`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** The query represents the current element being compared, the key represents a preceding element used to determine similarity, and the value is the preceding element's content that is weighted and summed. The query-key dot product is divided by √dk because arbitrarily large dot products can cause numerical problems and gradient loss after exponentiation.

**Required facts:**

- `ragbench-v1-044-f1`: Query, key, and value respectively represent the current comparison element, a preceding comparison element, and the preceding content to weight and sum. (evidence: ragbench-v1-044-e1)
- `ragbench-v1-044-f2`: The query-key dot product is divided by the square root of key/query dimensionality to reduce numerical and gradient problems from large values. (evidence: ragbench-v1-044-e2)

**Evidence:**

- `ragbench-v1-044-e1` — `Speech and Language Processing.pdf`, PDF page 190 (printed label 182); supports ragbench-v1-044-f1

> The attention head allows us to
> distinctly represent three different roles that each input embedding plays during the
> course of the attention process:
> • Asthe current elementbeing compared to the preceding inputs. We’ll refer to
> this role as aquery.query
> • In its role asa preceding inputthat is being compared to the current element
> to determine a similarity weight. We’ll refer to this role as akey.key
> • And finally, as avalueof a preceding element that gets weighted and summedvalue
> up to compute the output for the current element.

- `ragbench-v1-044-e2` — `Speech and Language Processing.pdf`, PDF page 190 (printed label 182); supports ragbench-v1-044-f2

> Furthermore,
> the result of a dot product can be an arbitrarily large (positive or negative) value, and
> exponentiating large values can lead to numerical issues and loss of gradients during
> training. To avoid this, we scale the dot product by a factor related to the size of the
> embeddings, via dividing by the square root of the dimensionality of the query and
> key vectors (dk).

**Required evidence groups:**

- `ragbench-v1-044-g1`: any one of [ragbench-v1-044-e1] supports ragbench-v1-044-f1.
- `ragbench-v1-044-g2`: any one of [ragbench-v1-044-e2] supports ragbench-v1-044-f2.

**Terminology examples:**

- query, key, and value: Q/K/V, query-key-value projections, scaled dot-product attention

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-045

**Question:** How do sparse and dense retrieval represent queries and documents, and why do modern dense systems use approximate nearest-neighbor search such as Faiss?

**Category / difficulty:** `method_comparison` / `medium`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Sparse retrieval uses count vectors weighted by tf-idf or BM25, while dense retrieval uses neural vector representations. Dense ranking requires finding document vectors with the highest dot product to the query vector, a nearest-neighbor problem, so modern systems use approximate nearest-neighbor algorithms such as Faiss for efficiency.

**Required facts:**

- `ragbench-v1-045-f1`: Sparse retrieval represents queries and documents with count vectors weighted by tf-idf or BM25. (evidence: ragbench-v1-045-e1)
- `ragbench-v1-045-f2`: Dense retrieval represents queries and documents with neural vectors. (evidence: ragbench-v1-045-e2)
- `ragbench-v1-045-f3`: Dense top-dot-product search is nearest-neighbor search, for which modern systems use approximate algorithms such as Faiss. (evidence: ragbench-v1-045-e3)

**Evidence:**

- `ragbench-v1-045-e1` — `Speech and Language Processing.pdf`, PDF page 262 (printed label 254); supports ragbench-v1-045-f1

> In sparse retrieval, we represent documents and queries
> withcount vectors, weighted by tf-idf or BM25.

- `ragbench-v1-045-e2` — `Speech and Language Processing.pdf`, PDF page 263 (printed label 255); supports ragbench-v1-045-f2

> documents and queries withembeddings, computed from language models (either
> encoder or decoder models). We’ll discuss sparse retrieval in the rest of this section,
> and turn to dense retrieval in Section 11.3.

- `ragbench-v1-045-e3` — `Speech and Language Processing.pdf`, PDF page 275 (printed label 267); supports ragbench-v1-045-f3

> Efficiency is an important issue, since every possible document must be ranked
> for its similarity to the query. For sparse word-count vectors, the inverted index
> allows this very efficiently. For dense vector algorithms finding the set of dense
> document vectors that have the highest dot product with a dense query vector is
> an instance of the problem ofnearest neighbor search. Modern systems there-
> fore make use of approximate nearest neighbor vector search algorithms likeFaissFaiss

**Required evidence groups:**

- `ragbench-v1-045-g1`: any one of [ragbench-v1-045-e1] supports ragbench-v1-045-f1.
- `ragbench-v1-045-g2`: any one of [ragbench-v1-045-e2] supports ragbench-v1-045-f2.
- `ragbench-v1-045-g3`: any one of [ragbench-v1-045-e3] supports ragbench-v1-045-f3.

**Terminology examples:**

- sparse retrieval: BM25 retrieval, tf-idf retrieval, count-vector retrieval
- approximate nearest neighbor: ANN, vector nearest-neighbor search, Faiss search

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-046

**Question:** What are the two major stages of basic RAG, and which three knowledge problems does the text say retrieval can help address?

**Category / difficulty:** `multi_fact_lookup` / `medium`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** Basic RAG first retrieves useful documents from a specified collection and then uses a large language model to generate an answer conditioned on those documents and the original query. Retrieval can mitigate hallucination with trusted documents, provide factual access to proprietary data, and supply dynamic or time-sensitive knowledge newer than model training.

**Required facts:**

- `ragbench-v1-046-f1`: Basic RAG retrieves useful documents and then generates an answer conditioned on those documents and the original query. (evidence: ragbench-v1-046-e1)
- `ragbench-v1-046-f2`: Trusted retrieved documents can help mitigate hallucination. (evidence: ragbench-v1-046-e2)
- `ragbench-v1-046-f3`: RAG can help a language model generate factual text about proprietary data. (evidence: ragbench-v1-046-e2)
- `ragbench-v1-046-f4`: RAG can provide dynamic, time-sensitive knowledge from after model training. (evidence: ragbench-v1-046-e2)

**Evidence:**

- `ragbench-v1-046-e1` — `Speech and Language Processing.pdf`, PDF page 275 (printed label 267); supports ragbench-v1-046-f1

> The information retrieval techniques we introduced in the prior section can be inte-
> grated into language models via a method calledretrieval-augmented generation
> orRAG. In the basic RAG scenario that we will describe in this section, we use IR
> techniques to retrieve documents from some specified store of documents that are
> likely to have useful information. Then we use a large language model togenerate
> an answer conditioned on these documents in addition to the original query.

- `ragbench-v1-046-e2` — `Speech and Language Processing.pdf`, PDF page 275 (printed label 267); supports ragbench-v1-046-f2, ragbench-v1-046-f3, ragbench-v1-046-f4

> As we summarized in the introduction to the chapter, there are many goals of
> retrieval-augmented generation. RAG can help mitigate hallucination, by giving
> the model a set of trusted documents. RAG can also help language models gen-
> erate factual text about proprietary data, like personal email, or health records, or
> company-internal documents, or other legal documents. RAG can also help with
> the problem that knowledge is dynamic and time-sensitive, for example if we know
> the user’s information need references data from a time after a language model was
> trained.

**Required evidence groups:**

- `ragbench-v1-046-g1`: any one of [ragbench-v1-046-e1] supports ragbench-v1-046-f1.
- `ragbench-v1-046-g2`: any one of [ragbench-v1-046-e2] supports ragbench-v1-046-f2.
- `ragbench-v1-046-g3`: any one of [ragbench-v1-046-e2] supports ragbench-v1-046-f3.
- `ragbench-v1-046-g4`: any one of [ragbench-v1-046-e2] supports ragbench-v1-046-f4.

**Terminology examples:**

- retrieval-augmented generation: RAG, retrieve-then-generate, retriever-generator pipeline

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-047

**Question:** Which word-level edit operations underlie word error rate, and what range exception is noted because insertions are included?

**Category / difficulty:** `numerical_factual_lookup` / `easy`

**Allowed sources:** Speech and Language Processing.pdf

**Answerability / expected behavior:** `answerable` / `answer_using_only_allowed_sources`

**Reference answer:** WER uses the minimum number of word substitutions, insertions, and deletions needed to map the hypothesis to the correct string. Because insertions are included, WER can exceed 100%.

**Required facts:**

- `ragbench-v1-047-f1`: WER is based on the minimum word substitutions, insertions, and deletions needed to map between the hypothesized and correct strings. (evidence: ragbench-v1-047-e1)
- `ragbench-v1-047-f2`: WER can exceed 100% because insertions are included. (evidence: ragbench-v1-047-e1)

**Evidence:**

- `ragbench-v1-047-e1` — `Speech and Language Processing.pdf`, PDF page 386 (printed label 378); supports ragbench-v1-047-f1, ragbench-v1-047-f2

> words between the hypothesized and correct strings, giving us the minimum num-
> ber of wordsubstitutions, wordinsertions, and worddeletionsnecessary to map
> between the correct and hypothesized strings. The word error rate (WER) is then
> defined as follows (note that because the equation includes insertions, the error rate
> can be greater than 100%):

**Required evidence groups:**

- `ragbench-v1-047-g1`: any one of [ragbench-v1-047-e1] supports ragbench-v1-047-f1.
- `ragbench-v1-047-g2`: any one of [ragbench-v1-047-e1] supports ragbench-v1-047-f2.

**Terminology examples:**

- word error rate: WER, ASR edit-distance error rate, speech-recognition error rate

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read against the original PDF; source, one-based physical page, quote, semantic support, fact links, evidence groups, restrictions, and terminology were reverified after narrowing or correcting this record.

## ragbench-v1-048

**Question:** According to "Computer Vision: Algorithms and Applications.pdf", which word-level edit operations underlie word error rate, and what range exception is noted because insertions are included?

**Category / difficulty:** `controlled_unanswerable` / `medium`

**Allowed sources:** Computer Vision: Algorithms and Applications.pdf

**Answerability / expected behavior:** `unanswerable_within_allowed_sources` / `abstain_and_state_that_allowed_source_is_insufficient`

**Reference answer:** The requested fact is not supported by the allowed source, so the system should abstain.

**Required facts:**

- None; the required behavior is abstention within the allowed source restriction.

**Evidence:**

- No admissible positive evidence; see the allowed-source absence audit below.

**Verified distractors:**

- `ragbench-v1-048-d1` — `Speech and Language Processing.pdf`, PDF page 386 (printed label 378): This passage answers the question, but it is outside the explicitly allowed computer-vision PDF and must not be used.

> words between the hypothesized and correct strings, giving us the minimum num-
> ber of wordsubstitutions, wordinsertions, and worddeletionsnecessary to map
> between the correct and hypothesized strings. The word error rate (WER) is then
> defined as follows (note that because the equation includes insertions, the error rate
> can be greater than 100%):

**Allowed-source absence audit:**

- Source: `Computer Vision: Algorithms and Applications.pdf`; physical pages inspected: 1232
- Search terms: word error rate, WER, insertions substitutions deletions, speech recognition error rate
- Result: No passage supporting the requested fact was found in the allowed source.
- Near-hit review: Case-insensitive WER matched only the line-broken surname 'Wer-man' on PDF page 572; it is unrelated to word error rate.
- Caution: The complete extractable text of the allowed source was audited. The label passes this source audit, while retaining uncertainty because absence of every possible paraphrase cannot be guaranteed.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read the disallowed positive passage and audited the complete pypdf-extracted text of every physical page in the allowed source for the recorded terms and plausible terminology; no supporting allowed-source prose was found.

## ragbench-v1-049

**Question:** According to "Designing Data-Intensive Applications.pdf", how does byte-pair encoding training grow its token vocabulary?

**Category / difficulty:** `controlled_unanswerable` / `medium`

**Allowed sources:** Designing Data-Intensive Applications.pdf

**Answerability / expected behavior:** `unanswerable_within_allowed_sources` / `abstain_and_state_that_allowed_source_is_insufficient`

**Reference answer:** The requested fact is not supported by the allowed source, so the system should abstain.

**Required facts:**

- None; the required behavior is abstention within the allowed source restriction.

**Evidence:**

- No admissible positive evidence; see the allowed-source absence audit below.

**Verified distractors:**

- `ragbench-v1-049-d1` — `Speech and Language Processing.pdf`, PDF page 51 (printed label 43): This prose states how BPE grows longer tokens, but the explicit source restriction excludes it.

> TheBPEtraining algorithm iteratively merges frequent neighboring tokens to create
> longer and longer tokens. The algorithm begins with a vocabulary that is just the
> set of all individual characters. It then examines the training corpus, and finds the
> two characters that are most frequently adjacent.

**Allowed-source absence audit:**

- Source: `Designing Data-Intensive Applications.pdf`; physical pages inspected: 613
- Search terms: byte-pair encoding, byte pair encoding, BPE, subword tokenization, token vocabulary merge
- Result: No passage supporting the requested fact was found in the allowed source.
- Caution: The complete extractable text of the allowed source was audited. The label passes this source audit, while retaining uncertainty because absence of every possible paraphrase cannot be guaranteed.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read the disallowed positive passage and audited the complete pypdf-extracted text of every physical page in the allowed source for the recorded terms and plausible terminology; no supporting allowed-source prose was found.

## ragbench-v1-050

**Question:** According to "Grokking-the-system-design-interview-free.pdf", how do forward and reverse KL differ in mode-covering versus mode-seeking behavior?

**Category / difficulty:** `controlled_unanswerable` / `hard`

**Allowed sources:** Grokking-the-system-design-interview-free.pdf

**Answerability / expected behavior:** `unanswerable_within_allowed_sources` / `abstain_and_state_that_allowed_source_is_insufficient`

**Reference answer:** The requested fact is not supported by the allowed source, so the system should abstain.

**Required facts:**

- None; the required behavior is abstention within the allowed source restriction.

**Evidence:**

- No admissible positive evidence; see the allowed-source absence audit below.

**Verified distractors:**

- `ragbench-v1-050-d1` — `Probabilistic Machine Learning.pdf`, PDF page 259 (printed label 225): This disallowed-source passage states the forward-KL behavior.

> To preventDKL (p∥q) from becoming infinite, we must haveq > 0whenever p > 0(i.e., q
> must have support everywherep does), soq tends tocoverboth modes as it must be nonvanishing
> everywhere p is; this is calledmode-coveringorzero-avoidingbehavior

- `ragbench-v1-050-d2` — `Probabilistic Machine Learning.pdf`, PDF page 259 (printed label 225): This disallowed-source passage states the reverse-KL behavior.

> By
> contrast, to preventDKL (q∥p) from becoming infinite, we must haveq = 0whenever p = 0, which
> createsmode-seekingorzero-forcingbehavior

**Allowed-source absence audit:**

- Source: `Grokking-the-system-design-interview-free.pdf`; physical pages inspected: 196
- Search terms: Kullback-Leibler, KL divergence, forward KL, reverse KL, mode-covering, mode-seeking, zero-avoiding, zero-forcing
- Result: No passage supporting the requested fact was found in the allowed source.
- Caution: The complete extractable text of the allowed source was audited. The label passes this source audit, while retaining uncertainty because absence of every possible paraphrase cannot be guaranteed.

**Source audit:** `reviewed_and_verified` via `codex_source_audit` on 2026-09-08 using OpenAI Codex (GPT-5); evaluation eligibility = `eligible`; human approved = `false`.

Re-read the disallowed positive passage and audited the complete pypdf-extracted text of every physical page in the allowed source for the recorded terms and plausible terminology; no supporting allowed-source prose was found.
