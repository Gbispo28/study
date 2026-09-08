# Diagnostic & Assessment System: English Learning OS

> **Core Pedagogical Directive**: *Never assume a flat A0/A1 proficiency without deterministic measurement. Never collapse multi-dimensional linguistic skills into a single scalar score.*

---

## 1. System Overview

The **English Learning OS Diagnostic System** provides an objective, scientifically validated framework for establishing the learner's true baseline competence, identifying specific cognitive and phonological bottlenecks, and tracking measurable longitudinal acquisition over time.

Commercial language platforms frequently commit two critical diagnostic errors:
1. **The Homogeneous Beginner Fallacy**: Assuming that an adult Portuguese-speaking data engineer who starts learning English is uniformly "A0/A1" across all skills. In reality, such learners often possess high passive technical reading comprehension (A2/B1) alongside severe auditory parsing limitations (A1) and near-zero spontaneous oral retrieval (Pre-A1).
2. **The Collapsed Scalar Fallacy**: Condensing complex communicative abilities into a single arbitrary number (e.g., "Duolingo score: 65" or "CEFR: 2.3"). This masks critical skill imbalances and leads to misallocated study routines.

---

## 2. Diagnostic Pack Architecture

The assessment framework is structured across six dedicated specifications:

| Document | Purpose & Scope | Target Modalities |
| :--- | :--- | :--- |
| [BASELINE_PROTOCOL.md](./BASELINE_PROTOCOL.md) | Standardized multi-dimensional test battery administered at Day 0. | Listening, Reading, Speaking, Pronunciation, Writing, Grammar, Vocabulary (7 battery parts). |
| [CEFR_RUBRIC.md](./CEFR_RUBRIC.md) | Explicit qualitative and performance rubrics grounded in the Council of Europe CEFR Companion Volume (2020). | Pre-A1 through B2 descriptors for Reception, Production, Interaction, and Phonological Control. |
| [LEARNER_INTAKE.md](./LEARNER_INTAKE.md) | High-information learner questionnaire capturing operational lifestyle and environmental variables. | Study schedules, auditory equipment, prior exposure, affective comfort, daily SRS tolerance. |
| [SCORING_MODEL.md](./SCORING_MODEL.md) | Deterministic and explainable scoring algorithms. Converts raw task performance into a multi-dimensional proficiency vector. | Algorithmic scoring rules, confidence intervals, borderline band handling (`A2-high / B1-low`). |
| [RETEST_PROTOCOL.md](./RETEST_PROTOCOL.md) | Scientifically defensible retesting schedule designed to prevent practice effects and item memorization. | Weekly leading indicators vs. 90-day lagging CEFR benchmark evaluations. |

---

## 3. The 7 Diagnostic Assessment Dimensions

```
                        ┌─────────────────────────────────────┐
                        │ Multi-Dimensional Baseline Profile  │
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
                   │ (Sentence       │           │ (VLT K1–K5      │
                   │  frames)        │           │  receptive/prod)│
                   └─────────────────┘           └─────────────────┘
```

---

## 4. Administration Sequence

To prevent cognitive fatigue from invalidating test results, the baseline battery is administered across two distinct sessions:

- **Session 1: Receptive & Lexical Baseline (~35 min)**:
  - Step 1: Complete [LEARNER_INTAKE.md](./LEARNER_INTAKE.md) (10 min).
  - Step 2: Part G — Vocabulary Levels Test (VLT K1–K3) (10 min).
  - Step 3: Part A — Auditory Listening Comprehension (15 min).
- **Session 2: Productive & Articulatory Baseline (~30 min)**:
  - Step 4: Part B — Reading Comprehension (10 min).
  - Step 5: Part D — Pronunciation & Minimal Pair Perception/Production (10 min).
  - Step 6: Part C & E — Spoken Interaction & Written Sentence Combining (10 min).

---

## 5. Epistemic Principles Governing Assessment

1. **Deterministic Scoring**: Human/AI evaluators must follow explicit rubric matrices in [CEFR_RUBRIC.md](./CEFR_RUBRIC.md); no intuitive "gut-feel" scoring is permitted.
2. **Explicit Uncertainty**: Where performance spans two bands or test evidence is limited, the score must be reported as a borderline classification with confidence ratings (e.g., `Listening: A1-high / A2-low [Confidence: High]`).
3. **No Fake Precision**: Reporting unsupported fractional CEFR levels (e.g., `Speaking = 1.43`) is strictly prohibited.
