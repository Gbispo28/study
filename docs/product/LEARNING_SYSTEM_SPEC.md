# Learning System Specification: English Learning OS

> **Document Status**: Canonical Pedagogical Specification Artifact (Phase 02 Synthesis — Refined)
> **Target Release**: Foundation for Phase 03 (Daily Journey & Card Architecture)
> **Engineering Invariant**: This document specifies *how the learning system operates scientifically and operationally*. It does NOT select software frameworks, backend databases, or cloud infrastructure (strictly deferred to Phase 04 per ADR-0000).

---

## 1. Learner Model

- **Persona**: Single adult learner, native Brazilian Portuguese speaker, professional software engineer and data processing specialist.
- **Cognitive Profile**:
  - High analytical capability, abstract reasoning, and familiarity with technical syntax, logic, and data schemas.
  - Perceived memory/retention difficulty with isolated rote memorization; high vulnerability to cognitive overload if routines lack explicit structure.
  - Asymmetric exposure: Extensive passive exposure to written English code, error logs, and technical documentation; minimal real-time conversational practice; significant foreign language speaking anxiety (FLA).
- **Time Commitment**: Exactly **60 focused minutes per day**, 6 to 7 days per week.
- **Hardware Ecosystem**: MacBook Air M4 (macOS workstation) + Samsung Galaxy S24 Ultra (Android mobile companion).

---

## 2. Multi-Dimensional Proficiency Model (Pre-A1 to C2)

The learner's proficiency is modeled as an asynchronous 9-dimensional state vector $\vec{P}$ spanning **Pre-A1 through C2**:

$$\vec{P} = \begin{bmatrix}
L & \text{(Acoustic Listening Comprehension)} \\
R & \text{(Text Reading Comprehension)} \\
SP & \text{(Spoken Monologue Production)} \\
SI & \text{(Spoken Interactive Turn-Taking)} \\
W & \text{(Written Composition & Synthesis)} \\
PC & \text{(Phonological Control & Intelligibility)} \\
GC & \text{(Operational Grammatical Competence)} \\
VR & \text{(Receptive Vocabulary Breadth - Lemmas)} \\
VP & \text{(Productive Vocabulary Recall - Lemmas)}
\end{bmatrix}$$

- **Distinction of Dimensions**: Official CEFR scales (Listening, Reading, Spoken Production, Spoken Interaction, Written Production, Phonological Control) are strictly distinguished from internal diagnostic dimensions (Operational Grammar, Receptive Vocabulary Breadth, Productive Vocabulary Recall).
- **Non-Parametric Uncertainty Modeling**: Each dimension is reported with qualitative `Confidence Ratings` (`High`, `Medium`, `Low`), `Evidence Sufficiency`, and `Boundary Bands` (`A2-high / B1-low`). Fake statistical confidence intervals are rejected.

---

## 3. Epistemic Evidence Model

All curricular decisions trace directly to [EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md):
- All working hypotheses and instructional assumptions are treated as `CANDIDATE CLAIMS / RESEARCH LEADS` until audited against empirical literature.
- Claims are graded across the 8-tier epistemic hierarchy (`ESTABLISHED`, `STRONG EVIDENCE`, `MODERATE EVIDENCE`, `LIMITED EVIDENCE`, `EXPERT CONSENSUS`, `PLAUSIBLE / HYPOTHESIS`, `UNSUPPORTED`, `CONFLICTING EVIDENCE`).

---

## 4. Assessment & Diagnostic Model

- **Diagnostic Nature & Scope**: Internal formative profiling tool informed by CEFR descriptors. **Not an accredited or certified Council of Europe examination**.
- **Item Copyright Protection**: Cites original frameworks (CEFR 2020, Cambridge EVP/EGP, Nation's VLT). All test items in [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md) are original custom diagnostic items.
- **Adaptive Routing & Early Stopping**: Core A1/A2 routing with optional extension up to C1/C2 if performance warrants. Early stopping halts testing when accuracy drops $<40\%$ to prevent fatigue.
- **Longitudinal Schedule**: Derived from psycholinguistic research on practice effects and adult L2 acquisition rates; operationalized as weekly formative micro-checks, monthly vocabulary checks, and 90-day alternate-form milestone retests.

---

## 5. Vocabulary Acquisition Model

- **Counting Unit**: **Lemmas** and validated **Multiword Expressions (MWEs)**. Word family counting is avoided at A0–B1 stages to prevent inflating presumed morphological knowledge.
- **Corpus Frequency Prioritization**: Derived from BNC/COCA frequency bands:
  - *Tier 1*: K1 Band (Top 1,000 general lemmas).
  - *Tier 2*: K2 Band (1,001–2,000 general lemmas).
  - *Tier 3*: K3 Band + High-Frequency Workplace/Data Lexis.
- **Intentional + Incidental Hybrid**: Intentional SRS (Anki) rapidly primes receptive form-meaning recognition; scaffolded comprehensible input provides ecological consolidation and collocational depth.
- **Coverage Filtering**: Materials assigned to the learner must maintain $\ge 95\%$ lexical coverage.

---

## 6. Grammar Model

- **Pedagogical Standard**: **Focus on Form (FonF)**. Rote grammar parsing worksheets and abstract grammatical terminology are banned.
- **Progression**: Grounded in the Cambridge English Grammar Profile (EGP) from A1 basic SVO through B1/B2 complex subordination.
- **Instructional Practice**: Practiced through functional sentence combining, cloze retrieval frames, and communicative micro-prompts.

---

## 7. Listening Comprehension Model

- **Bimodal Primacy**: Reading-While-Listening (audio + synchronized text) serves as the acoustic bridge for A0–A2 stages.
- **Acoustic Decoding Curriculum**: Explicit bottom-up training on connected speech in General American English (alveolar flapping, schwa reduction of unstressed function words, consonant elision, linking).
- **Lexical Threshold**: Listening material must maintain $\ge 95\%$ lexical coverage to prevent cognitive overload.

---

## 8. Reading Comprehension Model

- **Extensive Reading (ER)**: Utilizing Graded Readers calibrated to $\ge 98\%$ coverage to foster reading fluency and sight-word automatization.
- **Intensive Reading (IR)**: Short workplace-relevant technical passages (100–250 words) analyzed for new collocations, syntax frames, and sentence mining.

---

## 9. Spoken Production & Interaction Model

- **Early Production**: Oral output commences in Week 1 via scaffolded sentence frames.
- **CAF Triad Decoupling**: Fluency practice (speed, 4/3/2 drills) is strictly decoupled from accuracy drills (explicit correction).
- **AI Voice Dialogue (Gemini Live)**: Low-stakes, zero-anxiety interactive speaking practice enacting specific professional scenarios.
- **Explicit Feedback Protocol**: AI provides explicit, metalinguistic correction (not ambiguous recasts), limited to a maximum of 2 errors per turn.

---

## 10. Pronunciation & Articulatory Mechanics Model

- **Target Standard**: **General American English (GAE)**, targeting comfortable international intelligibility and functional comprehensibility rather than native accent mimicry.
- **Candidate Contrastive Priorities (Modulated by Regional BP Dialect)**:
  1. *Epenthesis Suppression*: Eliminating added [i] on final consonant stops (*stop*, *big*, *laptop*).
  2. *Word Stress & Tonic Syllables*: Lengthening stressed syllables and reducing unstressed syllables.
  3. *Core Vowel Contrasts*: Minimal pair training on /i/ vs /ɪ/ (*ship/sheep*), /æ/ vs /ɛ/ (*bad/bed*).
  4. *Coda Nasal Closure*: Closing lips on /m/ and tongue on /n/ to stop vowel nasalization.
- **Continuous Acoustic Rhythm**: Rhythm is trained as a continuous acoustic contrast (stress lengthening and schwa reduction via nPVI principles) rather than a rigid binary syllable/stress switch.

---

## 11. Writing & Composition Model

- **Core Instructional Tool**: **Sentence Combining** (Saddler & Graham, 2005). Combining kernel sentences into complex, cohesive sentences using conjunctions and relative clauses.
- **Functional Workplace Writing**: Short Slack messages, bug reports, and pull request descriptions.
- **AI Feedback Guardrails**: 4-step scaffolding protocol: 1) Validate meaning $\rightarrow$ 2) Highlight max 2 errors $\rightarrow$ 3) Elicit learner self-correction $\rightarrow$ 4) Provide target model. Silent AI ghostwriting is prohibited.

---

## 12. Memory & Cognitive Load Model

- **Working Memory Protection**: Eliminate extraneous cognitive load (visual clutter, complex interfaces).
- **The Testing Effect**: Every review event requires active retrieval before answer reveal.
- **Interleaving Rule**: The 60-minute daily session must interleave Retrieval $\rightarrow$ Input $\rightarrow$ Production.
- **Cognitive Budget**: Deliberate cognitive effort peaks at 45–50 minutes; daily session must cleanly conclude at 60 minutes.

---

## 13. Spaced Repetition (SRS) & Card Architecture

- **Scheduler Engine**: Native Anki **FSRS**.
- **Desired Retention**: Initial default set to **0.90 (90%)** for core foundational vocabulary. Evaluated down to 0.87 or 0.85 only if mature review volume threatens the daily 15-minute timebox. Compute Minimum Recommended Retention (CMRR) used as analytical reference.
- **Nonlinear Workload**: Acknowledges that workload scaling is rapid and nonlinear as retention approaches 1.0.
- **Card Schemas (4 Note Types)**:
  1. `CARD-01`: Lean Receptive Lemma (Top 500 concrete nouns/verbs).
  2. `CARD-02`: Contextual Sentence Cloze (Polysemy, collocations, grammar frames).
  3. `CARD-03`: Audio Discrimination (Minimal pairs, connected speech).
  4. `CARD-04`: Functional Productive Prompt (Scenario-based vocalized retrieval).
- **Leech Policy**: Cards failing 4 times are tagged `leech_pending_reformulation`, suspended, and queued for reformulation.

---

## 14. The 60-Minute Routine Allocation Policy

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DAILY 60-MINUTE SESSION STRUCTURE                    │
├───────────────────────┬────────────────────────┬───────────────────────┤
│  BLOCK 1: RETRIEVAL   │ BLOCK 2: FOCUSED INPUT │  BLOCK 3: PRODUCTION  │
│      (15–20 min)      │      (25–30 min)       │      (10–15 min)      │
├───────────────────────┼────────────────────────┼───────────────────────┤
│ • Anki/FSRS review    │ • Bimodal input        │ • Spoken AI dialogue  │
│ • Due cards only      │ • Graded reading       │ • Sentence combining  │
│ • 5–10 new cards      │ • Acoustic decoding    │ • Articulatory drills │
│ • Hard stop at 20 min │ • Sentence mining      │ • Micro-writing       │
└───────────────────────┴────────────────────────┴───────────────────────┘
```

- **Policy Before Mathematics**: Governed by operational priority rules and cognitive timeboxes rather than fake mathematical formulas.
- **Workload Throttling Invariant**:
  $$\text{If } \text{Daily Reviews} > 15 \text{ min } \implies \text{New Cards Introduced} = 0$$
- **Core vs. Ambient Separation**: Core study is guaranteed and independent of ambient exposure. Ambient exposure is tracked separately as optional bonus.
- **Execution Modes**: Mode A (continuous 60m on MacBook Air) and Mode B (split 20m morning AnkiDroid on S24 + 40m evening on MacBook Air).

---

## 15. Metrics & Measurement Framework

- **Leading Indicators (Daily/Weekly Behavior)**: Adherence rate ($\ge 85\%$), review queue clearance, true retention ($88\% - 92\%$), bimodal input volume ($\ge 2,000$ words/week), sentences vocalized ($\ge 15$/day).
- **Lagging Outcomes (Periodic Mastery)**: Measured shift in the multi-dimensional vector $\vec{P}$, growth in validated receptive lemmas, unassisted connected speech comprehension, epenthesis suppression in spontaneous speech.

---

## 16. Tool & Ecosystem Leverage (Verified September 2026)

- **Google AI Pro (R$ 96,99/mês in Brazil)**: Access to Gemini 3.1 Pro, Antigravity rate limits, Workspace integration, Deep Research, 5TB storage. Gemini Live on Galaxy S24 Ultra serves as primary voice speaking partner; NotebookLM Audio Overview generates calibrated podcasts from user texts.
- **Claude Code Pro**: Agentic engineering CLI for text frequency profiling, sentence mining extraction, deterministic validation, and card compilation. (Not a voice tutor).
- **MacBook Air M4**: Deep workstation for 40-minute input/production blocks, Anki desktop management, local whisper transcription.
- **Galaxy S24 Ultra**: Mobile companion for 15-minute AnkiDroid reviews, Gemini Live spoken practice, ambient audio listening, S-Pen handwriting.
- **Curated Free Resources**: Cambridge Learner's Dictionary, YouGlish, Forvo, COCA, VOA Learning English, Project Gutenberg.

---

## 17. Tracked Open Questions & Dependencies

- **[DEP-01] Learner Diagnostic Execution**: Calibration of vector $\vec{P}$ and dynamic routine weights depends on the learner completing [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md) and [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md).
- **[DEP-02] Anki Sync Strategy**: Selection between AnkiWeb cloud sync or local AnkiConnect desktop automation (deferred to Phase 03).
- **[DEP-03] Audio Generation Provider**: Evaluation of local vs cloud TTS for card audio (deferred to Phase 04 ADR).

---

## 18. Phase 03 Input Contract & Gate Status

Phase 03 (**Daily Journey & Card Architecture**) requires as its mandatory starting input:
1. The learner's completed diagnostic test data and computed vector $\vec{P}$.
2. The 4 standardized card taxonomies defined in Section 13.
3. The FSRS configuration parameters ($R = 0.90$, steps = `10m`, max interval = `365d`, 4-lapse leech policy).
4. The 3-block modular timebox (15m SRS / 30m Input / 15m Output).
5. The 4-step AI corrective feedback scaffolding protocol.

**Gate Status**: Phase 03 remains **LOCKED** until the user executes the diagnostic protocol and submits intake responses. All application stack decisions remain strictly deferred to Phase 04 per ADR-0000.
