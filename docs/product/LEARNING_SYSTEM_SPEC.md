# Learning System Specification: English Learning OS

> **Document Status**: Canonical Pedagogical Specification Artifact (Phase 02 Synthesis)
> **Target Release**: Foundation for Phase 03 (Daily Journey & Card Architecture)
> **Engineering Invariant**: This document specifies *how the learning system operates scientifically and mathematically*. It does NOT select software frameworks, backend databases, or cloud infrastructure (deferred to Phase 04 per ADR-0000).

---

## 1. Learner Model

- **Persona**: Single adult learner, native Brazilian Portuguese speaker, professional software engineer and data processing specialist.
- **Cognitive Profile**:
  - High analytical capability, abstract reasoning, and familiarity with technical syntax, logic, and data schemas.
  - Perceived memory/retention difficulty with isolated rote memorization; high vulnerability to cognitive overload if routines lack explicit structure.
  - Asymmetric exposure: Extensive passive exposure to written English code, error logs, and technical documentation; minimal real-time conversational practice; significant foreign language speaking anxiety (FLA).
- **Time Commitment**: Exactly **60 focused minutes per day**, 6 to 7 days per week.
- **Hardware Ecosystem**: MacBook Air M4 (macOS) + Samsung Galaxy S24 Ultra (Android).

---

## 2. Multi-Dimensional Proficiency Model

The learner's proficiency is mathematically defined as a 9-dimensional vector:

$$\vec{P} = \langle L, R, SP, SI, W, PC, GC, VR, VP \rangle$$

- $L \in [\text{Pre-A1}, \text{C2}]$: Acoustic Listening Comprehension (connected speech & reduction parsing).
- $R \in [\text{Pre-A1}, \text{C2}]$: Text Reading Comprehension (syntax, inferencing, lexical coverage).
- $SP \in [\text{Pre-A1}, \text{C2}]$: Spoken Monologue Production (fluency, coherence, sustained utterance).
- $SI \in [\text{Pre-A1}, \text{C2}]$: Spoken Interactive Turn-Taking (conversational agility, latency, repair).
- $W \in [\text{Pre-A1}, \text{C2}]$: Written Composition (sentence combining, cohesive workplace messaging).
- $PC \in [\text{Pre-A1}, \text{C2}]$: Phonological Control & Intelligibility (prosody, stress, epenthesis suppression).
- $GC \in [\text{Pre-A1}, \text{C2}]$: Operational Grammatical Competence (functional sentence frames in use).
- $VR \in \mathbb{N}$: Receptive Vocabulary Breadth (number of recognized lemmas, sampled via VLT).
- $VP \in \mathbb{N}$: Productive Vocabulary Recall (number of spontaneously retrievable lemmas).

Each dimension is independently evaluated and tagged with an explicit confidence score (`Low`, `Medium`, `High`).

---

## 3. Epistemic Evidence Model

All curriculum choices, scheduling parameters, and feedback mechanisms adhere to the 8-tier epistemic grading standard defined in [EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md):
- `ESTABLISHED`: Replicated meta-analyses and cognitive laws (Retrieval Practice, Spacing Effect, Zipf's Law, Intelligibility Principle).
- `STRONG EVIDENCE`: Peer-reviewed controlled trials (Lexical Coverage $\ge 95\%$, Focus on Form, Sentence Combining, Bimodal Input, FSRS efficiency).
- `MODERATE EVIDENCE`: Validated primary studies with boundary conditions (High-Variability Phonetic Training, AI speaking scaffolding).
- `EXPERT CONSENSUS`: Authoritative institutional frameworks (CEFR Companion Volume 2020, English Profile EVP/EGP).
- `PLAUSIBLE / HYPOTHESIS`: Theoretical models awaiting empirical validation.
- `UNSUPPORTED`: Disproven myths (isolated word lists produce 2x retention; 4-week drills permanently prevent fossilization; unassisted 70% coverage input works for beginners).

---

## 4. Assessment & Diagnostic Model

- **Initial Baseline Battery**: Administered via [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md) and scored via [SCORING_MODEL.md](../assessment/SCORING_MODEL.md). Never assumes a flat A0/A1 starting point.
- **Intake Questionnaire**: Administered via [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md) to calibrate daily energy windows, auditory gear, and communicative urgency.
- **Retest Schedule**: Administered via [RETEST_PROTOCOL.md](../assessment/RETEST_PROTOCOL.md) using a 3-form alternate item pool (Forms A, B, C) at 90-day intervals to eliminate test-retest practice effects.
- **Bottleneck Identification**: The system applies the Weakest Link Theorem to continuously detect the specific dimension constraining communicative output and automatically tilts daily study allocation toward it.

---

## 5. Vocabulary Acquisition Model

- **Counting Unit**: **Lemmas** and validated **Multiword Expressions (MWEs)**. Word family counting is prohibited for A0–B1 stages.
- **Selection Algorithm**: Prioritized by frequency bands derived from COCA/BNC:
  $$\text{Priority} = \text{Rank}_{\text{COCA}} \times \text{CommunicativeUtility} \times \text{CEFRBand}_{\text{EVP}} \times \text{DomainRelevance}$$
  - *Tier 1*: K1 Band (Top 1,000 general lemmas) — non-negotiable prerequisite.
  - *Tier 2*: K2 Band (1,001–2,000 general lemmas) — covers ~85% of spoken discourse.
  - *Tier 3*: K3 Band + High-Frequency Workplace/Data Lexis.
- **Intentional + Incidental Hybrid**:
  - Intentional SRS (Anki) rapidly establishes initial receptive form-meaning recognition (10–30 words/hour).
  - Scaffolded input (Graded readers, bimodal listening) deepens collocational and syntactic maturity.
- **Receptive vs. Productive Division**: Receptive vocabulary target is maintained at $2.5\text{x} - 3.0\text{x}$ the productive target. Only high-utility communicative verbs, connectors, and nouns enter productive recall cards.

---

## 6. Grammar Model

- **Pedagogical Strategy**: **Focus on Form (FonF)**. Traditional isolated grammar parsing worksheets and abstract grammatical terminology are prohibited.
- **Syntactic Progression**: Grounded in the Cambridge English Grammar Profile (EGP):
  - *Phase A (A1)*: SVO word order, present simple (habitual), present continuous (action in progress), modal *can*, basic prepositions of place/time (*in, on, at*).
  - *Phase B (A2)*: Past simple regular/irregular, basic modals of necessity (*must, have to, should*), comparative adjectives, future with *going to*, basic coordinators (*because, but, so*).
  - *Phase C (B1)*: Present perfect (unfinished time/experience), first conditional, simple passives, relative clauses (*which, that, who*).
- **Instructional Vehicle**: Functional sentence frames embedded directly in input texts and practiced through sentence combining and cloze retrieval cards.

---

## 7. Listening Comprehension Model

- **Primary Input Mode**: **Bimodal Input (Reading-While-Listening)** during A0–A2 stages. Natural native audio accompanied by synchronized text to anchor phoneme-grapheme correspondences.
- **Acoustic Decoding Curriculum**: Dedicated bottom-up training on connected speech phenomena in General American English:
  1. Alveolar flapping ([ɾ] in *water, get it*).
  2. Vowel reduction to schwa (/ə/ in *to, for, can, of*).
  3. Consonant cluster elisions (*last night* $\rightarrow$ [læs naɪt]).
  4. Linking and liaison across word boundaries.
- **Lexical Threshold**: Listening material must strictly guarantee $\ge 95\%$ lexical coverage. Unsimplified native podcasts are prohibited for core study until B1+ proficiency.

---

## 8. Reading Comprehension Model

- **Extensive Reading (ER)**: Utilizing Graded Readers calibrated to the learner's vocabulary level at $\ge 98\%$ coverage to foster automatic sight-word recognition and reading fluency.
- **Intensive Reading (IR)**: Short workplace-relevant technical passages (100–250 words) analyzed for new collocations, syntax frames, and sentence mining.
- **Tooling Support**: Clean text display, integrated Cambridge Learner dictionary lookups, and one-click sentence mining into Anki card drafts.

---

## 9. Spoken Production & Interaction Model

- **Early Production**: Oral output commences in Week 1 via controlled sentence frames and vocalized retrieval.
- **Cognitive Decoupling (CAF Triad)**:
  - *Fluency Sessions*: Timed 4/3/2 speech routines, AI dialogues focused on communicative speed where linguistic errors are ignored.
  - *Accuracy Sessions*: Structured articulatory drills and sentence frame completions with explicit immediate corrective feedback.
- **AI Conversational Partner (Gemini Live)**: Low-stakes, zero-anxiety interactive speaking practice enacting specific professional and daily scenarios (daily standups, ordering, status updates).
- **Corrective Feedback Protocol**: AI must provide explicit, metalinguistic correction (not ambiguous recasts), limited to a maximum of 2 errors per turn.

---

## 10. Pronunciation & Articulatory Mechanics Model

- **Target Accent**: **General American English (GAE)**, evaluated on international intelligibility and articulatory comprehensibility, never native-speaker mimicry.
- **Contrastive Intervention for Brazilian Portuguese (BP) Interference**:
  1. **Suppressing Final Epenthesis**: Articulatory stop closure drills preventing added [i] on final stops (*stop*, *job*, *big*, *internet*). (Priority Rank 1).
  2. **Word Stress & Tonic Syllable**: Visual bolding of primary stress on polysyllabic words to entrain stress-timed English rhythm. (Priority Rank 2).
  3. **High-Frequency Vowel Contrasts**: Minimal pair discrimination and production for /i/ vs /ɪ/ (*ship/sheep*), /æ/ vs /ɛ/ (*bad/bed*), /u/ vs /ʊ/ (*pool/pull*).
  4. **Coda Nasal Closure**: Physical closure of lips on /m/ and tongue on /n/ to stop vowel nasalization transfer.

---

## 11. Writing & Composition Model

- **Core Instructional Tool**: **Sentence Combining** (Saddler & Graham, 2005). Combining two or three simple kernel sentences into complex, cohesive sentences using conjunctions and relative clauses.
- **Functional Workplace Writing**: Drafting short asynchronous technical updates, bug reports, and polite professional Slack messages.
- **AI Feedback Guardrails**: The 4-step scaffolding protocol is mandatory: 1) Validate message meaning $\rightarrow$ 2) Identify up to 2 specific syntactic/lexical errors $\rightarrow$ 3) Elicit learner self-correction $\rightarrow$ 4) Provide target model. Full AI ghostwriting/rewriting is strictly forbidden.

---

## 12. Memory & Cognitive Load Model

- **Working Memory Protection**: Eliminate all extraneous cognitive load (visual clutter, complex interfaces, confusing instructions).
- **The Testing Effect**: Every card and review event requires active retrieval from memory before revealing answers.
- **Interleaving Rule**: The 60-minute daily session must interleave Retrieval $\rightarrow$ Input $\rightarrow$ Production. Full-day blocking (e.g., 60 minutes of flashcards) is prohibited.
- **Fatigue Guardrail**: Deliberate cognitive effort peaks at 45–50 minutes; daily session must cleanly conclude at 60 minutes.

---

## 13. Spaced Repetition (SRS) & Card Architecture

- **Scheduler Engine**: Native Anki **FSRS-5**.
- **Desired Retention Parameter**:
  - Initial default: **$R = 0.90$** (minimizes frustrating card lapses during K1 core vocabulary acquisition).
  - Dynamic scaling: Evaluated down to $R = 0.87$ or $0.85$ only if review time approaches the 15-minute daily ceiling as mature card volume exceeds 1,000 cards.
- **Card Schema Standardization (4 Note Types)**:
  1. `CARD-01`: Lean Receptive Lemma (Top 500 concrete nouns/verbs).
  2. `CARD-02`: Contextual Sentence Cloze (Polysemy, collocations, grammar frames).
  3. `CARD-03`: Audio Discrimination (Minimal pairs, connected speech decoding).
  4. `CARD-04`: Functional Productive Prompt (Scenario-based vocalized retrieval).
- **Leech Policy**: Cards failing 4 times are tagged `leech_pending_reformulation`, suspended from the daily review queue to prevent review bloat, and queued for instructional reformulation.

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

- **Execution Modes**:
  - *Mode A (Continuous)*: 60 minutes uninterrupted on MacBook Air M4.
  - *Mode B (Split Schedule)*: 20 minutes mobile SRS (AnkiDroid on Galaxy S24) in morning + 40 minutes deep input/production (MacBook Air) in evening.
- **Workload Throttling Invariant**:
  $$\text{If } \text{Daily Reviews} > 15 \text{ min} \implies \text{New Cards Introduced} = 0$$

---

## 15. Metrics & Measurement Framework

- **Leading Indicators (Daily/Weekly Behavior)**:
  - Session adherence rate ($\ge 85\%$).
  - Review queue clearance within timebox.
  - True retention rate ($88\% - 92\%$).
  - Bimodal words heard/read ($\ge 2,000$ words/week).
  - Sentences vocalized aloud ($\ge 15$ sentences/day).
- **Lagging Outcomes (Quarterly Mastery)**:
  - Measured shift in the multi-dimensional CEFR vector $\vec{P}$.
  - Growth in validated receptive lemmas (VLT).
  - Epenthesis suppression rate in spontaneous speech.
  - Acoustic connected speech comprehension score at 1.0x speed.

---

## 16. Tool & Hardware Ecosystem Leverage

- **Google AI Pro (Gemini Advanced)**: Primary real-time spoken conversational partner (Gemini Live), multimodal pronunciation feedback, and NotebookLM podcast/audio generation.
- **Claude Code Pro**: Automation engine for text frequency filtering, sentence mining extraction, deterministic repository validation, and card syntax compilation.
- **MacBook Air M4**: Deep workstation for 40-minute input/production blocks, Anki desktop management, local whisper transcription, and writing composition.
- **Galaxy S24 Ultra**: Mobile workstation for 15-minute AnkiDroid review micro-sessions and on-the-go Gemini Live spoken dialogues.
- **Curated Free Resources**: Cambridge Learner's Dictionary (CEFR lexis), YouGlish (authentic video context), Forvo (native audio pronunciation), COCA (frequency validation), Voice of America (scaffolded bimodal input).

---

## 17. Tracked Open Questions & Dependencies

- **[DEP-01] Learner Diagnostic Execution**: The exact initialization of $\vec{P}$ and dynamic routine weights depends on the learner completing [BASELINE_PROTOCOL.md](../assessment/BASELINE_PROTOCOL.md) and [LEARNER_INTAKE.md](../assessment/LEARNER_INTAKE.md).
- **[DEP-02] Anki Sync Strategy**: Selection between AnkiWeb cloud sync or local AnkiConnect desktop automation (deferred to Phase 03).
- **[DEP-03] Audio Generation Provider**: Evaluation of high-quality local vs cloud TTS for custom sentence card audio generation (deferred to Phase 04 ADR).

---

## 18. Phase 03 Input Contract (Preconditions for Next Phase)

Phase 03 (**Daily Journey & Card Architecture**) may strictly consume the following validated specifications from Phase 02:
1. The 4 standardized card taxonomies defined in Section 13.
2. The FSRS-5 configuration parameters ($R = 0.90$, steps = `10m`, max interval = `365d`, 4-lapse leech policy).
3. The 3-block modular timebox (15m SRS / 30m Input / 15m Output).
4. The BP-contrastive pronunciation priority matrix from [0006-pronunciation-brazilian-portuguese.md](../research/0006-pronunciation-brazilian-portuguese.md).
5. The 4-step AI corrective feedback scaffolding protocol.
6. The diagnostic scoring algorithms and vector profile structure from [SCORING_MODEL.md](../assessment/SCORING_MODEL.md).

**Phase 03 Boundary**: Phase 03 must NOT select web/backend application frameworks or database storage technologies; all application architecture remains deferred to Phase 04.
