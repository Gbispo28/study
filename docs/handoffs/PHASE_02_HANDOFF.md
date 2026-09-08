# Session Handoff: Phase 02.1 — Scientific Validity & Diagnostic Hardening

> **Session**: Phase 02.1 Scientific Hardening & Diagnostic Separation<br>
> **Timestamp**: 2026-09-08<br>
> **Branch**: `main`<br>
> **Gate 2 Decision**: `GATE 2: BLOCKED ON LEARNER BASELINE`<br>
> **Phase 02 Status**: **OPEN / IN PROGRESS** (Pedagogical Specification Hardened — Awaiting Learner Baseline Data)<br>
> **Phase 03 Status**: **LOCKED** (Pending Learner Baseline Administration)<br>
> **Starting HEAD**: `734e374941ea9094e31bce5bfec9cef6325ec50e`<br>
> **Current HEAD**: Resolve dynamically at runtime with `git rev-parse HEAD`

---

## 1. Accomplished in This Remediation Session

1. **Separated Assessment Architecture & Zero-Leakage Surfaces**:
   - Segregated learner-facing materials into `docs/assessment/learner/` ([learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md) and [learner/SUBMISSION_TEMPLATE.md](../assessment/learner/SUBMISSION_TEMPLATE.md)) with zero exposure of answer keys, audio transcripts, scoring rubrics, or hidden routing logic.
   - Isolated administrative evaluation tools in `docs/assessment/admin/`:
     - [admin/ADMINISTRATION_PROTOCOL.md](../assessment/admin/ADMINISTRATION_PROTOCOL.md): Audio delivery standards (GAE accent, wpm speech rate policies, max 2 plays, continuous playback without mid-utterance scrubbing, headphone requirements, synthetic TTS limitation disclosure).
     - [admin/AUDIO_SCRIPT.md](../assessment/admin/AUDIO_SCRIPT.md): Full transcripts with IPA phonetic annotations.
     - [admin/ITEM_KEY.md](../assessment/admin/ITEM_KEY.md): Definitive answer keys and acceptable response variants.
     - [admin/SCORING_GUIDE.md](../assessment/admin/SCORING_GUIDE.md): Qualitative scoring rules, non-parametric uncertainty profiling, dynamic bottleneck engine.
2. **Explicit Diagnostic Measurement Ceiling (B2 Ceiling)**:
   - Established that the custom compact battery formatively profiles **Pre-A1 to B2**.
   - Performance exceeding this range returns `ABOVE CURRENT INSTRUMENT CEILING — EXTERNAL/EXTENDED ASSESSMENT REQUIRED`.
   - Never infers C1 or C2 from single isolated extension items.
3. **Elimination of Pseudo-Psychometrics & Fake Vocabulary Extrapolation**:
   - Completely removed the 3-item `correct/3 * 1000 = 1600 lemmas` formula.
   - Part G now assesses categorical **Lexical Band Familiarity** (K1, K2, K3 bands: High, Moderate, Emergent); quantitative vocabulary size estimation is deferred to longitudinal tracking or a dedicated 50+ item test.
   - Removed arbitrary raw-score-to-CEFR conversion cutpoint tables. Replaced with qualitative descriptor profiling across multiple tasks.
4. **Controlled for Domain Knowledge Contamination**:
   - Balanced baseline items with general everyday English, non-technical workplace communication, and technical English as a distinct contextual probe.
   - Evaluator is instructed to distinguish high technical conceptual schema from general English communicative decoding.
5. **Dynamic, Learner-Data-Driven Bottleneck Detection**:
   - Replaced the rigid fixed hierarchy (`epenthesis -> listening -> vocabulary -> speaking -> grammar`) with a 5-factor clinical evaluation (severity, communicative impact, frequency, goal relevance, remediation leverage).
6. **FSRS Temporal Accuracy & Parameter Hardening**:
   - Removed CMRR (Compute Minimum Recommended Retention) from current operational guidance; retained solely as historical context explaining its removal in Anki 25.07. Replaced with native Anki Simulator and Help Me Decide guidance.
   - Formally classified all scheduling parameters (`OFFICIAL DEFAULT`, `CURRENT OFFICIAL GUIDANCE`, `PROJECT OPERATIONAL DEFAULT`, `EXPERIMENTAL`).
   - Softened quantitative claims into benchmark observations and illustrative simulations.
7. **Tool Ecosystem Temporal Audit**:
   - Claude Code: Replaced retired models (Claude 3.7 retired Feb 2026) with capability-based phrasing ("currently supported models under the learner's plan", such as Sonnet 5, Fable 5, Opus 4.8 / 4.7, Sonnet 4.6). Noted Claude Pro includes Claude Code (API billing separate).
   - Google AI Pro & NotebookLM: Verified 300 sources per notebook in Pro tier (50 is base/free tier).
   - Project Gutenberg: Reclassified from "Graded Readers A2–B2" to "Public-domain source corpus for carefully selected/adapted texts".
8. **Scientific Findings & Evidence Matrix Hardening**:
   - *EVD-13 (Corrective Feedback)*: Corrected category error from Lyster & Saito (2010). Prompts (eliciting self-repair) $\ne$ explicit correction (supplying forms). Reclassified taxonomy.
   - *EVD-15 (Sentence Combining)*: Downgraded to `LIMITED TO MODERATE EVIDENCE (Adult L2)`; noted Saddler & Graham studied 4th-graders and Andrews review found limited adult L2 evidence; removed universal $d = 0.70$ transfer claim.
   - *EVD-16 (60-Minute Ceiling)*: Reclassified as `CONFIRMED PRODUCT CONSTRAINT` (learner commitment), removing biological cliff claims and controversial ego-depletion citations.
   - *EVD-04 (Lexical Coverage)*: Softened from biological cliff to probabilistic target (~95% scaffolded, ~98% extensive) conditioned on domain schema and visual aids.
   - *Retest Protocol*: Reclassified 150-200 guided learning hours as an institutional planning heuristic, not an invariant law; labeled 90-day retest as a conservative operational default.

---

## 2. Active Decisions & Governance Status

- **Stack Selection**: Strictly deferred to Phase 04 via ADR-0000. Zero production code written.
- **Pedagogical Invariants**: Fully operationalized in [LEARNING_PRINCIPLES.md](../product/LEARNING_PRINCIPLES.md).
- **FSRS Configuration**: Native Anki FSRS, $R = 0.90$, steps `10m` or empty, max interval `36500d` default or project cap, 4-lapse leech policy.
- **Gate 2 Verdict**: Maintained as `GATE 2: BLOCKED ON LEARNER BASELINE`. Phase 02 remains open; Phase 03 is locked until baseline data is submitted.

---

## 3. Required User Action to Unblock Gate 2

1. Fill out [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md).
2. Complete and record responses to [learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md) using [learner/SUBMISSION_TEMPLATE.md](../assessment/learner/SUBMISSION_TEMPLATE.md).
3. Once submitted, the system will score vector $\vec{P}$ via [admin/SCORING_GUIDE.md](../assessment/admin/SCORING_GUIDE.md), detect the primary cognitive bottleneck, close Gate 2, and unlock Phase 03.
