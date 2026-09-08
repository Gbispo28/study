# Retesting & Longitudinal Tracking Protocol: English Learning OS

> **Core Principle**: *Never mistake test familiarity for language acquisition. Separate daily leading indicators from periodic lagging outcomes.*

---

## 1. Practice Effects & Retest Intervals

### 1.1 The Threat of Test-Retest Practice Effects
In SLA and psychometrics, administering identical assessment instruments at close intervals (e.g., weekly or bi-weekly) severely corrupts measurement validity (Alderson, 2005):
- Learners memorize specific test prompts, question options, and sentence answers.
- Score inflation reflects test-wiseness and episodic memory rather than generalized linguistic proficiency.
- Practice effects create a dangerous illusion of accelerated progress.

### 1.2 Scientifically Defensible Retest Schedule

| Assessment Type | Frequency / Interval | Purpose | Evaluation Items |
| :--- | :--- | :--- | :--- |
| **Micro-Diagnostic Check** | Weekly (End of Week) | Formative check on target skills learned during the week. | Alternate-form sentence combining (3 items), 4-item acoustic dictation. |
| **Vocabulary Progress Check** | Monthly (Every 30 Days) | Measure receptive lemma expansion and retention stability. | 30-item sampled Vocabulary Levels Test (VLT K1–K3) drawn from unseen item bank. |
| **Major Milestone Retest** | **Quarterly (Every 90 Days)** | Comprehensive re-evaluation of the full multi-dimensional vector $\vec{P}$. | Complete alternate form of [BASELINE_PROTOCOL.md](./BASELINE_PROTOCOL.md) (Form B / Form C). |

---

## 2. Leading vs. Lagging Indicators

A fatal flaw in commercial language apps is tracking trivial activity metrics (e.g., daily streaks, XP points, badges) and presenting them as proxies for fluency. The English Learning OS explicitly separates **Leading Indicators** from **Lagging Outcomes**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MEASUREMENT ARCHITECTURE                        │
├───────────────────────────────────┬────────────────────────────────────┤
│        LEADING INDICATORS         │          LAGGING OUTCOMES          │
│    (What the learner controls)    │      (What the system measures)    │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Study Adherence (Days/week = 60m)│ • CEFR Multi-Dimensional Bands    │
│ • SRS Reviews Completed Daily     │ • Receptive Lexical Breadth (Lemmas│
│ • FSRS True Retention Rate (%)    │ • Spoken Retrieval Latency (sec)   │
│ • Minutes of Bimodal Input Heard  │ • Epenthesis Suppression Rate (%)  │
│ • Sentences Vocalized Aloud Daily │ • Sentence Combining Accuracy (%)  │
│ • Written Words Composed          │ • Unassisted Acoustic Comprehension│
└───────────────────────────────────┴────────────────────────────────────┘
```

### 2.1 Daily & Weekly Leading Indicators
Tracked automatically during daily sessions:
1. **Adherence Rate**: Percentage of days achieving the full 60-minute session (Target: $\ge 85\%$, or 6 out of 7 days).
2. **Review Clearance**: Clearing all due FSRS reviews within the 15-minute timebox.
3. **True Retention**: Percentage of mature reviews rated "Good" or "Easy" on first pass (Target: $88\% - 92\%$).
4. **Input Volume**: Running word count of bimodal text read and listened to (Target: $\ge 1,500$ words/week at A1; $\ge 4,000$ words/week at A2).
5. **Vocal Output Count**: Number of complete sentences spoken aloud in Block 3 (Target: $\ge 15$ sentences/day).

### 2.2 Monthly & Quarterly Lagging Outcomes
Evaluated solely through standardized retests:
1. **CEFR Vector Progression**: Upward shift in individual dimensions (e.g., $L: \text{A1} \rightarrow \text{A2}$).
2. **Measured Lemma Growth**: Expansion in confirmed receptive lemmas (e.g., $+250$ lemmas/month).
3. **Acoustic Parsing Speed**: Ability to comprehend connected speech at natural speed (1.0x) without text scaffolding.
4. **Articulatory Accuracy**: Absence of epenthesis on word-final consonant clusters in unscripted speech.

---

## 3. Alternate-Form Pool Architecture

To guarantee that 90-day milestone retests measure genuine acquisition:
1. **Item Pool Triplication**: The system maintains three structurally isomorphic but lexically distinct test batteries:
   - **Form A**: Initial Baseline Test (administered Day 0).
   - **Form B**: Milestone 1 Retest (administered Day 90).
   - **Form C**: Milestone 2 Retest (administered Day 180).
2. **Isomorphism Rules**:
   - Audio passages maintain identical word count ($\pm 5\%$), speech rate (wpm), and frequency band distribution.
   - Minimal pair perception drills test identical phonemic contrasts using different lexical carriers (e.g., Form A: *ship/sheep*; Form B: *fit/feet*; Form C: *chip/cheap*).
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
        • Is severe pronunciation epenthesis blocking speaking output?
        • Is working memory overwhelmed by cognitive overload?
                              │
                              ▼
        Step 3: Dynamic Routine Adjustment (Phase 03 Engine)
        • Double time allocated to the stagnant skill (e.g., shift 10 min
          from passive reading to active speaking drills).
        • Reduce new vocabulary intake to decrease cognitive load.
```
