# Retesting & Longitudinal Tracking Protocol: English Learning OS

> **Core Tenet**: *Never mistake test familiarity for language acquisition. Derive retesting frequency from psycholinguistic evidence, measurement noise limits, and conservative operational judgment.*

---

## 1. Empirical Foundations of Retest Scheduling

### 1.1 The Threat of Practice Effects & Item Memorization
In psycholinguistic assessment, administering test items at close intervals (e.g., weekly or bi-weekly) severely corrupts measurement validity (Alderson, 2005; Hausknecht et al., 2007):
- **Episodic Recall**: Learners recall specific test sentences, audio scenarios, and multiple-choice options rather than demonstrating generalized communicative gains.
- **Score Inflation**: Test-retest score gains in short intervals largely reflect test-wiseness and reduced anxiety, not authentic second language development.
- **Measurement Noise**: Daily or weekly language fluctuations (sleep, work stress, emotional state) produce noise that overwhelms true linguistic growth.

### 1.2 Rate of L2 Acquisition in Working Adults: Heuristics vs. Universal Invariants
Institutional estimates (such as Cambridge English Language Assessment, 2018; North, 2014) frequently cite approximately **150 to 200 guided learning hours** to progress between major CEFR bands:
- **Planning Heuristic, Not Invariant Law**: These figures represent broad institutional planning averages derived from classroom contexts, not universal cognitive invariants. Individual trajectory speed is heavily modulated by prior language exposure, L1-L2 typological proximity, cognitive aptitude, and practice intensity.
- **Short-Term Measurement Noise**: Because authentic linguistic acquisition involves complex neural consolidation, testing formal CEFR competencies at very short intervals (e.g., bi-weekly) primarily captures measurement noise and transient state fluctuations (sleep, fatigue, anxiety) rather than durable competence gains.

### 1.3 Operational Consensus vs. Scientific Bounds
Where empirical literature does not dictate an exact calendar frequency, the English Learning OS adopts **conservative operational defaults**:

| Assessment Layer | Derived Frequency | Operational & Scientific Rationale | Evaluation Modality |
| :--- | :--- | :--- | :--- |
| **Daily Activity Tracking** | Continuous (Daily) | Zero testing overhead; tracks habit adherence and retrieval success without test fatigue. | Leading Indicators: FSRS review clearance, true retention, audio minutes heard, sentences spoken. |
| **Weekly Formative Micro-Check** | Weekly (Day 6, ~10 min) | Sensitive to short-term instructional uptake without testing broad CEFR bands. | 3-item sentence combining check, 4-item micro-dictation drawn from the week's study content. |
| **Monthly Lexical Check** | Every 30 Days (~10 min) | Tracks emerging receptive lemma recognition, which develops faster than complex communicative grammar. | Sampled probe from unseen frequency bands to check emerging recognition. |
| **Quarterly Formal Reassessment** | **Every 90 Days (~60 min)** | *Conservative Operational Default*: Provides an extended consolidation window to observe genuine skill shifts while minimizing practice effects. | Full alternate-form battery ([learner/BASELINE_FORM.md](./learner/BASELINE_FORM.md) Form B / Form C). |

---

## 2. Leading vs. Lagging Indicators

To prevent confusing activity streaks with language mastery:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MEASUREMENT ARCHITECTURE                        │
├───────────────────────────────────┬────────────────────────────────────┤
│        LEADING INDICATORS         │          LAGGING OUTCOMES          │
│    (Daily Study Behaviors)        │     (Periodic Measured Mastery)    │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Study Adherence (Days/week = 60m)│ • CEFR Profile Vector Shift (P)   │
│ • SRS Reviews Completed Daily     │ • Receptive Lexical Familiarity    │
│ • FSRS True Retention Rate (%)    │ • Spoken Retrieval Latency (sec)   │
│ • Minutes of Bimodal Input Heard  │ • Articulatory Intelligibility     │
│ • Sentences Vocalized Aloud Daily │ • Sentence Combining Accuracy (%)  │
│ • Written Words Composed          │ • Unassisted Acoustic Comprehension│
└───────────────────────────────────┴────────────────────────────────────┘
```

### 2.1 Daily & Weekly Leading Indicators (Operational Starting Targets)
The following numbers serve as **operational starting targets** to monitor consistency, not biological mandates:
1. **Adherence Rate**: Percentage of days achieving the full 60-minute session (*Starting Target*: $\ge 85\%$, or ~6 out of 7 days).
2. **Review Clearance**: Clearing all due FSRS reviews within the 15-minute timebox.
3. **True Retention**: Percentage of mature reviews rated "Good" or "Easy" on first pass (*Operational Target*: $88\% - 92\%$).
4. **Bimodal Input Volume**: Running word count of bimodal text read and listened to (*Operational Target*: $\approx 2,000$ words/week).
5. **Vocal Output Count**: Number of complete sentences spoken aloud in Block 3 (*Operational Target*: $\approx 15$ sentences/day).

### 2.2 Quarterly Lagging Outcomes (Hypotheses to Validate)
Evaluated solely through standardized alternate-form retests:
1. **CEFR Vector Progression**: Upward shift in individual dimensions (e.g., $L: \text{A1} \rightarrow \text{A2}$).
2. **Confirmed Lexical Growth**: Expanding familiarity into K2 and K3 frequency bands (*Planning Hypothesis*: $+200$ to $+300$ active/receptive lemmas per quarter).
3. **Acoustic Parsing Speed**: Ability to comprehend connected speech at natural speed (1.0x) without text scaffolding.
4. **Articulatory Accuracy**: Absence of epenthetic vowels on word-final consonant clusters in unscripted speech.

---

## 3. Alternate-Form Pool Architecture

To guarantee that 90-day milestone retests measure genuine acquisition:
1. **Item Pool Triplication**:
   - **Form A**: Initial Baseline Test (administered Day 0).
   - **Form B**: Milestone 1 Retest (administered Day 90).
   - **Form C**: Milestone 2 Retest (administered Day 180).
2. **Isomorphism Rules**:
   - Audio passages maintain identical word count ($\pm 5\%$), speech rate (wpm), and frequency band distribution.
   - Minimal pair drills test identical phonemic contrasts using different lexical carriers (e.g., Form A: *ship/sheep*; Form B: *fit/feet*; Form C: *chip/cheap*).
   - Sentence combining tasks utilize identical grammatical conjunctions (*because, although, after*) with novel situational prompts.

---

## 4. Retest Failure & Stagnation Protocol

If a 90-day milestone retest shows zero progression in a specific dimension (e.g., Spoken Production remains Pre-A1 after 3 months):

```
┌───────────────────────────────────────────────────────────┐
│               STAGNATION DIAGNOSTIC PROTOCOL              │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
        Step 1: Inspect Leading Indicator Logs for Last 90 Days
        • Were SRS reviews cleared consistently?
        • Was Block 3 (Production) skipped or truncated?
                              │
                              ▼
        Step 2: Check Cognitive Bottleneck Flag
        • What primary bottleneck is identified in SCORING_GUIDE.md?
          (e.g., acoustic decoding, K1 vocabulary deficit, or articulatory barrier)
        • Is working memory overwhelmed by task cognitive overload?
                              │
                              ▼
        Step 3: Dynamic Routine Adjustment (Routine Engine)
        • Double time allocated to the stagnant skill (e.g., shift 10 min
          from passive reading to active speaking drills).
        • Reduce new vocabulary intake to decrease cognitive load.
```
