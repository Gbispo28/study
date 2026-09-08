# Product Requirements: English Learning OS

> **Governance Note**: Every item in this document is categorized strictly by certainty level. Hypotheses and candidate claims must never be treated as confirmed requirements until empirical validation or explicit user diagnostic confirmation occurs.

---

## 1. Confirmed Requirements

- [REQ-01] **Single Learner Focus**: Optimized specifically for the primary user (Brazilian native Portuguese speaker, tech/data background).
- [REQ-02] **Multi-Dimensional Baseline Diagnosis**: Curriculum and routines must NOT assume a flat A0/A1 proficiency across all skills; the learner's baseline must be diagnosed as an asynchronous 9-dimensional vector $\vec{P}$ spanning Pre-A1 through C2 via [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md) and [SCORING_MODEL.md](../assessment/SCORING_MODEL.md).
- [REQ-03] **Strict 60-Minute Daily Budget**: Daily learning workflows must fit inside exactly 60 total minutes without spilling over into cognitive burnout, structured across three modular blocks (Retrieval, Input, Production) governed by operational priority rules.
- [REQ-04] **Memory Science Integration**: The learning methodology must prioritize active recall, native spaced repetition (FSRS), retrieval practice, and comprehensible input ($\ge 95\%$ coverage).
- [REQ-05] **Hardware Compatibility**: Must support zero-friction workflows across MacBook Air M4 (macOS desktop workstation) and Galaxy S24 Ultra (Android mobile companion).
- [REQ-06] **Anki / AnkiDroid Alignment**: Must integrate with or produce compatible assets for Anki desktop and AnkiDroid mobile, adhering strictly to the 4 standardized note schemas.
- [REQ-07] **Holistic Language Competencies**: Must address all core competencies: Speaking, Listening, Reading, Writing, Pronunciation (articulatory mechanics), and Grammar (Focus on Form).
- [REQ-08] **Progress Traceability**: The system must provide measurable metrics of mastery, vocabulary accumulation, and study consistency, strictly separating daily leading indicators from periodic lagging outcomes.
- [REQ-09] **Agent-First Foundation**: The repository must support multi-agent development with Google Antigravity 2.0, Gemini, and Claude Code Pro without vendor lock-in.
- [REQ-10] **Inviolable Pedagogical Invariants**: All system interactions, prompts, and routine generators must strictly adhere to [LEARNING_PRINCIPLES.md](./LEARNING_PRINCIPLES.md).
- [REQ-11] **Modern FSRS Engine**: Spaced repetition must use the native Anki FSRS scheduler with an initial desired retention of 90% ($R = 0.90$) and an automated 4-lapse leech reformulation policy.
- [REQ-12] **Contrastive Phonetic Priority**: Pronunciation instruction must prioritize Brazilian Portuguese candidate transfer breakdowns (final epenthesis suppression, word stress, /i/ vs /ɪ/ vowel contrast) to maximize international intelligibility.

---

## 2. Hypotheses Audit & Evolutionary Status (Phase 02 Audit)

The four initial repository hypotheses have undergone formal adversarial scientific audit against peer-reviewed SLA and cognitive literature (see [EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md)):

| Hypothesis ID | Original Formulation | Audit Verdict | Empirical Findings & Rationale | Transitioned Requirement / Operational Form |
| :--- | :--- | :--- | :--- | :--- |
| **HYP-01** | *Sentence Mining vs Word Lists*: Contextual sentence cards will produce 2x higher retention than isolated word translation cards. | **REVISED (Claim of 2x unsupported)** | Peer-reviewed vocabulary research (Webb, 2007; Waring, 2004) confirms sentence contexts aid syntax and collocation depth, but isolated word pairs allow faster initial receptive acquisition. A literal "2x retention multiplier" lacks empirical evidence. Reviewing sentence cards takes 2–3x longer per card. | **REQ-HYP-01 (Revised)**: Use lean bilingual cards (`CARD-01`) for initial form-meaning acquisition of the top 500 concrete lemmas; use contextual cloze cards (`CARD-02`) for polysemy, prepositions, collocations, and grammatical patterns. |
| **HYP-02** | *FSRS Algorithm Efficiency*: FSRS with an 85% retention target will minimize daily Anki review load compared to default Anki SM-2. | **REVISED (Target parameter unvalidated)** | FSRS reduces reviews by ~20–30% vs SM-2, but 85% desired retention increases card lapses to 15% (vs 10% at 90%). Anki's CMRR demonstrates that setting retention too low increases total study time due to high relearning overhead. For beginners, high lapse rates cause frustration and relearning churn. | **REQ-HYP-02 (Revised)**: Adopt FSRS scheduling. Set initial desired retention to **90%** for the core foundational vocabulary (first 1,000 words) to guarantee high recognition stability. Dynamically evaluate downscaling to 85–87% only after the learner accumulates $>500$ mature cards and reviews exceed 20 min/day. |
| **HYP-03** | *Phonemic Training Precedence*: Prioritizing phoneme discrimination in weeks 1–4 will prevent fossilized pronunciation errors common among Portuguese speakers. | **REVISED (Absolute prevention unsupported)** | High-Variability Phonetic Training (HVPT) significantly improves adult phonemic discrimination and production (Logan et al., 1991), but SLA literature (Han, 2004) confirms fossilization cannot be completely or permanently prevented by an initial 4-week drill block. | **REQ-HYP-03 (Revised)**: Implement dedicated contrastive phonological training targeting Brazilian Portuguese candidate interference (vowel contrasts, final epenthesis, rhythm) starting in Week 1, maintaining micro-drills integrated into daily listening/speaking. |
| **HYP-04** | *AI Conversational Scaffolding*: Controlled AI dialogue drills with real-time speech-to-text and grammar feedback will reduce anxiety compared to open-ended conversational apps. | **SUPPORTED (With pedagogical boundaries)** | Empirical research on computer-assisted language learning (CALL) and LLM dialogue systems (Kim et al., 2019; Kohnke et al., 2023) strongly validates that low-stakes, non-judgmental AI conversational practice reduces foreign language anxiety and promotes willingness to communicate. | **REQ-HYP-04 (Validated Requirement)**: Use structured, task-based AI conversational scenarios with explicit scaffolding and immediate corrective feedback as the primary speaking environment during A0–B1 stages to build productive fluency before live human interaction. |

---

## 3. Open Questions & Dependencies

- [OQ-01] **Actual Learner Baseline Vector**: What is the learner's measured performance across the 7 parts of [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md)? *(Status: Blocked on user test administration)*.
- [OQ-02] **Routine Schedule Mode**: Does the user prefer Mode A (Single 60-minute block on Mac) or Mode B (Split 20m mobile AnkiDroid + 40m Mac deep session)? *(Status: Addressed in [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md); awaiting user submission)*.
- [OQ-03] **Audio Input Gear**: What primary audio capture hardware will be used (wireless earbuds with microphone vs MacBook array)? *(Status: Addressed in [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md); awaiting user submission)*.
- [OQ-04] **Anki Synchronization Architecture**: Will card database synchronization between MacBook and Galaxy S24 Ultra use AnkiWeb cloud sync or local AnkiConnect desktop automation? *(Status: Active dependency for Phase 03)*.

---

## 4. Deferred Decisions

- [DEF-01] **Application Delivery Stack**: Web vs Desktop vs CLI application framework (strictly deferred to Phase 04 ADRs).
- [DEF-02] **Persistence Layer**: SQLite, JSON flat-files, PostgreSQL, or Git-based markdown storage (deferred to Phase 04 ADR).
- [DEF-03] **Speech & Audio Engines**: Choice of TTS/STT providers (deferred to Phase 04 ADR).
- [DEF-04] **Deployment Target**: Local-only, self-hosted container, or cloud deployment (deferred to Phase 04 ADR).

---

## 5. Non-Goals for Current & Upcoming Phase 03

- Implementing frontend UI screens, web apps, or mobile apps (deferred to Phase 05).
- Arbitrarily picking backend frameworks, databases, or cloud infrastructure (deferred to Phase 04).
- Creating automated production pipelines before card architecture is mathematically finalized.
