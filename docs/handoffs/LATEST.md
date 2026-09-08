# Latest Session Handoff

> **Session**: Phase 02.1 — Scientific Validity & Diagnostic Hardening<br>
> **Timestamp**: 2026-09-08<br>
> **Branch**: `main`<br>
> **Gate 2 Status**: `GATE 2: BLOCKED ON LEARNER BASELINE`<br>
> **Phase 02 Status**: **OPEN / IN PROGRESS** (Pedagogical Specification Hardened — Baseline Administration Pending)<br>
> **Phase 03 Status**: **LOCKED** (Pending Learner Baseline Assessment)<br>
> **Foundation Baseline Commit**: `9737f2d`<br>
> **Phase 01 Hardening Commit**: `4b0e109`<br>
> **Current HEAD**: Resolve dynamically at runtime with `git rev-parse HEAD`

---

## 1. Accomplished in This Session
- Completed surgical remediation of Phase 02 based on independent external audit findings:
  1. **Separated Assessment Architecture**: Created `docs/assessment/learner/` ([learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md) and [learner/SUBMISSION_TEMPLATE.md](../assessment/learner/SUBMISSION_TEMPLATE.md)) with zero answer key or audio script leakage. Created administrative evaluation suite in `docs/assessment/admin/` ([admin/ADMINISTRATION_PROTOCOL.md](../assessment/admin/ADMINISTRATION_PROTOCOL.md), [admin/AUDIO_SCRIPT.md](../assessment/admin/AUDIO_SCRIPT.md), [admin/ITEM_KEY.md](../assessment/admin/ITEM_KEY.md), [admin/SCORING_GUIDE.md](../assessment/admin/SCORING_GUIDE.md)).
  2. **Explicit B2 Measurement Ceiling**: Established that the internal battery formatively profiles Pre-A1 to B2; scores approaching ceiling output `ABOVE CURRENT INSTRUMENT CEILING — EXTERNAL/EXTENDED ASSESSMENT REQUIRED`, rejecting false C1/C2 claims.
  3. **Elimination of Fake Vocabulary Extrapolation**: Removed `correct/3 * 1000 = 1600` formula; Part G now assesses categorical Lexical Band Familiarity (K1, K2, K3), deferring continuous size estimation.
  4. **Removal of Arbitrary Raw-Score Cutpoints**: Replaced arbitrary numerical conversion tables with qualitative descriptor profiling across multiple tasks.
  5. **Controlled for Domain Knowledge Contamination**: Balanced baseline with everyday, workplace, and technical English to prevent technical familiarity from masking general conversational deficits.
  6. **Dynamic Bottleneck Detection Engine**: Replaced rigid clinical hierarchy with data-driven 5-factor evaluation (severity, communicative impact, frequency, goal relevance, remediation leverage).
  7. **FSRS Temporal Accuracy**: Removed CMRR from operational guidance (noted removal in Anki 25.07); classified all scheduling parameters formally; softened quantitative claims into benchmark simulations.
  8. **Tool Ecosystem Audit**: Updated Claude Code to capability-based phrasing ("currently supported models under learner's plan", noting 3.7 retired in Feb 2026); updated NotebookLM to 300 sources for Pro; reclassified Project Gutenberg as a public-domain source corpus for selected/adapted texts.
  9. **Scientific Claims Hardened**: Corrected corrective feedback taxonomy in EVD-13 (prompts $\ne$ explicit correction); downgraded sentence combining in EVD-15 for adult L2; reframed 60m ceiling in EVD-16 as a confirmed product constraint; softened lexical coverage in EVD-04 into probabilistic targets.
  10. **Retest Protocol Hardened**: Reframed 150-200 learning hours as institutional planning heuristics; labeled 90-day retest as conservative operational default.

---

## 2. Active Decisions & Governance Status
- **Application Stack**: Strictly deferred to Phase 04 via ADR-0000. Zero production code written.
- **Pedagogical Contract**: Governed by [LEARNING_PRINCIPLES.md](../product/LEARNING_PRINCIPLES.md).
- **FSRS Configuration**: Native Anki FSRS, $R = 0.90$, steps `10m` or empty, max interval `36500d` default, 4-lapse leech policy.
- **Gate 2 Decision**: `GATE 2: BLOCKED ON LEARNER BASELINE`. Phase 02 remains open; Phase 03 is locked until baseline data is submitted.

---

## 3. Recommended Next Actions
1. The learner completes [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md) and records responses to [learner/BASELINE_FORM.md](../assessment/learner/BASELINE_FORM.md) using [learner/SUBMISSION_TEMPLATE.md](../assessment/learner/SUBMISSION_TEMPLATE.md).
2. Evaluator scores responses via [admin/SCORING_GUIDE.md](../assessment/admin/SCORING_GUIDE.md), computes vector $\vec{P}$, identifies primary cognitive bottleneck, formally closes Gate 2, and unlocks **Phase 03: Daily Journey & Card Architecture**.
