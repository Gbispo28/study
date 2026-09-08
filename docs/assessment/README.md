# Diagnostic & Assessment System: English Learning OS

> **Core Pedagogical Directive**: *Never assume a flat A0/A1 proficiency without deterministic measurement. Never collapse multi-dimensional linguistic skills into a single scalar score. Avoid false psychometrics, fake precision, and test item leakage.*

---

## 1. System Overview & Regulatory Disclaimers

The **English Learning OS Diagnostic System** provides an objective, scientifically grounded framework for establishing the learner's multi-dimensional baseline competence, identifying specific cognitive and phonological bottlenecks, and tracking measurable longitudinal acquisition over time.

### 1.1 Crucial Regulatory & Psychometric Disclaimers
1. **Formative Diagnostic Instrument**: The English Learning OS Diagnostic Pack is an **internal diagnostic profiling and curriculum-routing instrument**. It is **NOT an officially accredited, certified, or endorsed examination** by the Council of Europe, Cambridge Assessment, ETS, or any formal accreditation body. It provides formative profiling to optimize daily 60-minute study allocations, not legal or academic certification.
2. **Explicit Measurement Ceiling (Pre-A1 to B2)**: The custom battery reliably profiles performance from **Pre-A1 through B2**. When learner performance approaches ceiling across all tasks, the system reports `ABOVE CURRENT INSTRUMENT CEILING — EXTERNAL/EXTENDED ASSESSMENT REQUIRED`. High-level proficiency (C1/C2) is never inferred from single isolated extension items.
3. **Separated Learner & Admin Surfaces**: To prevent test contamination and preserve measurement integrity, all answer keys, audio scripts, and scoring criteria are strictly segregated into administrative files and are never visible to the test-taker during administration.
4. **Copyright & Original Item Protection**: References to the Council of Europe CEFR Companion Volume (2020), the English Profile (EVP/EGP), and Paul Nation's Vocabulary Levels Tests (VLT) represent scholarly methodological attribution. All specific test prompts, audio scenarios, reading passages, and items within this pack are custom-authored for the English Learning OS.

---

## 2. Assessment Architecture & Directory Structure

The assessment framework is organized into dedicated surfaces:

```text
docs/assessment/
├── README.md                           # System overview & directory guide (this file)
├── LEARNER_INTAKE.md                   # Pre-test questionnaire (lifestyle, hardware, history)
├── CEFR_RUBRIC.md                      # Qualitative rubrics across communicative modes
├── RETEST_PROTOCOL.md                  # Longitudinal monitoring & alternate-form rules
├── learner/                            # LEARNER-FACING SURFACES (Zero answer/script leakage)
│   ├── BASELINE_FORM.md                # Clean test form with prompts & instructions
│   └── SUBMISSION_TEMPLATE.md          # Response sheet for written answers & recording refs
└── admin/                              # ADMINISTRATIVE SURFACES (Confidential to evaluator)
    ├── ADMINISTRATION_PROTOCOL.md      # Audio delivery, speech rates, playback policies
    ├── AUDIO_SCRIPT.md                 # Full transcripts & IPA annotations of audio stimuli
    ├── ITEM_KEY.md                     # Definitive answer keys & acceptable variations
    └── SCORING_GUIDE.md                # Evaluation rules, ceiling logic, bottleneck engine
```

### 2.1 File Map & Functional Roles

| Surface | File | Role & Scope |
| :--- | :--- | :--- |
| **Intake** | [LEARNER_INTAKE.md](./LEARNER_INTAKE.md) | Captures lifestyle schedule, available devices, language history, and subjective comfort. |
| **Learner** | [learner/BASELINE_FORM.md](./learner/BASELINE_FORM.md) | Standardized test form containing questions, passages, and prompts (zero answers or scripts). |
| **Learner** | [learner/SUBMISSION_TEMPLATE.md](./learner/SUBMISSION_TEMPLATE.md) | Formatted response sheet for learner submissions and audio recording attachments. |
| **Admin** | [admin/ADMINISTRATION_PROTOCOL.md](./admin/ADMINISTRATION_PROTOCOL.md) | Audio standardization (TTS/human, wpm rates), playback count, environment rules. |
| **Admin** | [admin/AUDIO_SCRIPT.md](./admin/AUDIO_SCRIPT.md) | Complete transcripts, IPA phonetic transcriptions, and acoustic target notes. |
| **Admin** | [admin/ITEM_KEY.md](./admin/ITEM_KEY.md) | Definitive keys, acceptable response variations, and objective scoring keys. |
| **Admin** | [admin/SCORING_GUIDE.md](./admin/SCORING_GUIDE.md) | Qualitative descriptor scoring, B2 ceiling logic, non-parametric uncertainty, bottleneck engine. |
| **Rubric** | [CEFR_RUBRIC.md](./CEFR_RUBRIC.md) | Qualitative CEFR descriptors (Pre-A1 to C2) across 5 core communicative dimensions. |
| **Retest** | [RETEST_PROTOCOL.md](./RETEST_PROTOCOL.md) | 90-day operational retest cycle, alternate-form pool (Forms A/B/C), practice effect mitigation. |

---

## 3. The 9-Dimensional State Vector $\vec{P}$ (Pre-A1 to B2)

The system models competence as an asynchronous multi-dimensional vector:

$$\vec{P} = \langle L, R, SP, SI, W, PC, GC, VR, VP \rangle$$

- **$L$ (Acoustic Listening)**: Evaluated through speech reduction discrimination and micro-dictation.
- **$R$ (Text Reading)**: Evaluated through workplace narrative comprehension and inferencing.
- **$SP$ (Spoken Monologue)**: Evaluated via 60–90s recorded daily routine description.
- **$SI$ (Spoken Interaction)**: Evaluated via recorded workplace scenario explanation.
- **$W$ (Written Composition)**: Evaluated via sentence combining and workplace message synthesis.
- **$PC$ (Phonological Control)**: Evaluated via minimal pair perception and read-aloud production.
- **$GC$ (Operational Grammar)**: Evaluated via functional grammatical patterns in context.
- **$VR$ (Receptive Lexical Band Familiarity)**: Evaluates familiarity across K1, K2, K3 bands (no fake continuous size extrapolation).
- **$VP$ (Productive Lexical Recall)**: Evaluated through lexical precision in spoken/written tasks.

---

## 4. Administration Sequence

To prevent cognitive fatigue and maintain valid focus:
- **Session 1: Receptive & Lexical Baseline (~25 min)**:
  - Part A: Auditory Listening Comprehension (Tasks A1 & A2).
  - Part B: Reading Comprehension (Task B1).
  - Part G: Lexical Familiarity Probe (Sections 1–3).
- **Session 2: Productive & Articulatory Baseline (~25 min)**:
  - Part C: Spoken Monologue & Scenario (`spoken_c1.m4a`, `spoken_c2.m4a`).
  - Part D: Pronunciation Perception & Read-Aloud (`spoken_d2.m4a`).
  - Part E: Sentence Combining & Workplace Message.
  - Part F: Operational Grammar in Use.
