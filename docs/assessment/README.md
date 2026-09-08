# Diagnostic & Assessment System: English Learning OS

> **Core Pedagogical Directive**: *Never assume a flat A0/A1 proficiency without deterministic measurement. Never collapse multi-dimensional linguistic skills into a single scalar score. Avoid false psychometrics.*

---

## 1. System Overview & Regulatory Disclaimers

The **English Learning OS Diagnostic System** provides an objective, scientifically grounded framework for establishing the learner's multi-dimensional baseline competence, identifying specific cognitive and phonological bottlenecks, and tracking measurable longitudinal acquisition over time.

### 1.1 Crucial Regulatory & Legal Disclaimers
1. **Not a Certified CEFR Examination**: The English Learning OS Diagnostic Pack is an **internal diagnostic and curriculum-routing instrument**. It is **NOT an officially accredited, certified, or endorsed examination** by the Council of Europe, Cambridge Assessment, ETS, or any formal accreditation body. It provides formative profiling to optimize daily 60-minute study allocations, not legal or academic certification.
2. **Copyright & Original Item Protection**: References to the Council of Europe CEFR Companion Volume (2020), the English Profile (EVP/EGP), and Paul Nation's Vocabulary Levels Tests (VLT) represent scholarly methodological attribution. All specific test prompts, audio scenarios, reading passages, and items within this pack are custom-authored for the English Learning OS and labeled as unstandardized diagnostic items.

---

## 2. Diagnostic Pack Architecture

The assessment framework comprises six dedicated specifications:

| Document | Purpose & Scope | Target Modalities |
| :--- | :--- | :--- |
| [BASELINE_PROTOCOL.md](./BASELINE_PROTOCOL.md) | Standardized multi-dimensional test battery administered at Day 0 (Pre-A1 to C2 adaptive routing). | Listening, Reading, Speaking, Pronunciation, Writing, Grammar, Vocabulary (7 battery parts). |
| [CEFR_RUBRIC.md](./CEFR_RUBRIC.md) | Qualitative rubrics grounded in the Council of Europe CEFR Companion Volume (2020) spanning Pre-A1 through C2. | Pre-A1 to C2 descriptors for Reception, Production, Interaction, and Phonological Control. |
| [LEARNER_INTAKE.md](./LEARNER_INTAKE.md) | High-information questionnaire capturing operational lifestyle, device, and environmental variables. | Study schedules, auditory equipment, prior exposure, affective comfort, daily SRS tolerance. |
| [SCORING_MODEL.md](./SCORING_MODEL.md) | Deterministic scoring algorithms producing the 9-dimensional state vector $\vec{P}$ and identifying the primary bottleneck. | Algorithmic scoring rules, confidence ratings, boundary bands (`A2-high / B1-low`), bottleneck detection. |
| [RETEST_PROTOCOL.md](./RETEST_PROTOCOL.md) | Research-derived longitudinal tracking schedule designed to mitigate practice effects and measurement noise. | Weekly leading indicators vs. periodic lagging outcome retests. |

---

## 3. The 9-Dimensional State Vector $\vec{P}$ Across Pre-A1 to C2

```
                        ┌─────────────────────────────────────┐
                        │ Multi-Dimensional Baseline Profile  │
                        │    Vector P: Pre-A1 through C2      │
                        └──────────────────┬──────────────────┘
                                           │
         ┌───────────────────┬─────────────┼─────────────┬───────────────────┐
         ▼                   ▼             ▼             ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────┴─────┐ ┌─────────────────┐ ┌─────────────────┐
│ 1. Auditory     │ │ 2. Text         │ │ 3. Oral   │ │ 4. Articulatory │ │ 5. Written      │
│    Listening    │ │    Reading      │ │    Speech │ │    Phonetics    │ │    Composition  │
│ (Connected      │ │ (Lexical &      │ │ (Fluency &│ │ (Minimal pairs, │ │ (Sentence       │
│  speech, rate)  │ │  inferencing)   │ │  repair)  │ │  epenthesis)    │ │  combining)     │
└─────────────────┘ └─────────────────┘ └───────────┘ └─────────────────┘ └─────────────────┘
                                           │
                            ┌──────────────┴──────────────┐
                            ▼                             ▼
                   ┌─────────────────┐           ┌─────────────────┐
                   │ 6. Functional   │           │ 7. Lexical Size │
                   │    Grammar      │           │    & Depth      │
                   │ (Sentence       │           │ (VLT K1–K5+     │
                   │  frames)        │           │  receptive/prod)│
                   └─────────────────┘           └─────────────────┘
```

---

## 4. Administration & Adaptive Routing Sequence

To prevent fatigue and eliminate ceiling or floor bias:
- **Session 1: Receptive & Lexical Baseline (~35 min)**:
  - Step 1: Complete [LEARNER_INTAKE.md](./LEARNER_INTAKE.md) (10 min).
  - Step 2: Part G — Vocabulary Levels Sampling (10 min).
  - Step 3: Part A — Auditory Listening Comprehension (15 min).
- **Session 2: Productive & Articulatory Baseline (~30 min)**:
  - Step 4: Part B — Reading Comprehension (10 min).
  - Step 5: Part D — Pronunciation & Minimal Pair Perception/Production (10 min).
  - Step 6: Part C & E — Spoken Interaction & Written Sentence Combining (10 min).

**Adaptive Early Stopping**: If accuracy drops below 40% on an initial core tier, testing in that dimension stops immediately to avoid invalid guessing and frustration. If accuracy exceeds 85%, optional extension items advance toward higher bands (up to C1/C2).

---

## 5. Epistemic Principles Governing Assessment

1. **Deterministic Scoring**: Evaluators must adhere to explicit rubric criteria in [CEFR_RUBRIC.md](./CEFR_RUBRIC.md); intuitive guessing is forbidden.
2. **Non-Parametric Uncertainty Modeling**: Rejects fictitious statistical "confidence intervals". Employs transparent `Confidence Rating` (`High`, `Medium`, `Low`), `Uncertainty Category`, `Evidence Sufficiency`, and `Boundary Band` classifications (`A2-high / B1-low`).
3. **Decoupled Competencies**: Receptive skills (reading/listening) are decoupled from productive skills (speaking/writing) to reflect the learner's true asymmetric competence.
