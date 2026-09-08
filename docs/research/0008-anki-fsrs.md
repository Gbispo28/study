# Research Note 0008: Anki & Modern FSRS Scheduling Architecture

- **Date**: 2026-09-08
- **Domain**: Spaced Repetition Algorithms, Mathematical Memory Modeling, Card Architecture
- **Primary Investigator**: Anki / SRS Specialist & Orchestrator
- **Epistemic Classification**: `STRONG EVIDENCE` (FSRS Algorithm & Memory Stability Modeling) / `EXPERT CONSENSUS` (Official Anki Documentation)

---

## 1. Research Question

How does the native Free Spaced Repetition Scheduler (FSRS) integrated into modern Anki function, what are the empirical workload trade-offs across different Desired Retention settings, how does the Compute Minimum Recommended Retention (CMRR) tool guide scheduling, and what card architecture guardrails prevent Anki from consuming the learner's 60-minute daily budget?

---

## 2. Mathematical Foundations: The Three-Component Memory Model

Modern Anki natively integrates FSRS (developed by Jarrett Ye and the Open-Spaced-Repetition initiative), based on the DSR model:
- **Stability ($S$)**: The time (in days) required for the retrievability of a memory trace to decrease from 100% to the target desired retention $R$.
- **Retrievability ($R$)**: The probability of successfully recalling an item at elapsed time $t$, modeled by a power forgetting curve:
  $$R(t, S) = \left(1 + \text{FACTOR} \cdot \frac{t}{S}\right)^{-w}$$
- **Difficulty ($D$)**: The inherent cognitive resistance of an item to consolidation, dynamically updated on a 1–10 scale based on user feedback (Again, Hard, Good, Easy).

### 2.1 Predictive Superiority Over Legacy SM-2
Large-scale benchmark evaluations on 20,000+ real Anki user review logs confirm that **FSRS achieves 20% to 35% fewer total reviews than legacy SM-2 while maintaining the exact same retention rate**, while completely eliminating the "Ease Hell" trap of SM-2.

---

## 3. Desired Retention, CMRR & Workload Scaling

A critical research lead investigated in Phase 02 is the optimal Desired Retention ($R$) parameter:

### 3.1 Nonlinear Workload Scaling
In FSRS, review intervals shorten rapidly and nonlinearly as Desired Retention approaches 1.0 (100%):
- Moving from $R = 0.85$ to $R = 0.90$ increases daily review volume moderately (~25–30%).
- Moving from $R = 0.90$ to $R = 0.95$ causes a **rapid, steep escalation** in daily reviews (~70–100% increase).
- Moving from $R = 0.95$ to $R = 0.99$ causes a severe workload explosion with negligible pedagogical benefit.

### 3.2 Compute Minimum Recommended Retention (CMRR)
Modern Anki includes the **Compute Minimum Recommended Retention (CMRR)** tool in Deck Options:
- **Functionality**: CMRR calculates the retention value that theoretically maximizes the amount of material learned per unit of study time.
- **Critical Trade-Off**: While lowering desired retention lengthens review intervals, it simultaneously increases the **forgetting rate** and **relearning overhead** (time spent reviewing failed cards). Setting desired retention lower than CMRR actually *increases* total daily study time because the penalty of frequent forgetting outweighs the savings from longer intervals.
- **Official Anki Recommendation**:
  - The official default desired retention is **0.90 (90%)**.
  - A range of **0.80 to 0.95** is considered reasonable depending on goals.
  - Setting retention below the CMRR is explicitly advised against.

### 3.3 Audit of the Historical 85% Hypothesis (HYP-02)
- The repository previously hypothesized that *85% retention minimizes workload*.
- **Empirical Verdict**: Unvalidated as an initial setting for an adult beginner. At $R = 0.85$, approximately 1 out of every 6.5 cards fails on daily review (15% lapse rate). For an adult beginner building foundational vocabulary, a high lapse rate induces significant cognitive fatigue, demotivation, and high relearning churn.
- **Refined Requirement**:
  - Start at the official Anki default of **$R = 0.90$** during the foundational vocabulary acquisition phase (first 1,000 lemmas).
  - Use CMRR as an analytical reference once review data accumulates.
  - Dynamically evaluate lowering to 0.87 or 0.85 only if the mature card pool grows large enough ($>1,000$ cards) that daily review time approaches the 15-minute timebox.

---

## 4. Workload Guardrails in a 60-Minute Routine

To prevent flashcard saturation ("Anki Hell") from crowding out real communicative practice:

### 4.1 Daily Review Cap & New Card Introductions
- **Daily SRS Timebox**: **15 minutes** (hard stop at 20 minutes).
- **New Card Pacing**: Strictly capped at **5 to 10 new cards per day**.
  - Introducing 8 cards/day = 240 words/month = ~1,400 core lemmas in 6 months (covering ~85% of spoken English).
  - Introducing $>15$ cards/day inevitably leads to review queues exceeding 100 cards/day, violating the 15-minute budget.
- **Automatic Throttling Invariant**:
  $$\text{If } \text{Daily Reviews} > 15 \text{ min } \implies \text{New Cards Introduced} = 0$$

### 4.2 Leech Management Policy
- **Definition**: A card that has lapsed 4 separate times after initial maturation.
- **Policy**:
  - Automated tag: `leech_pending_reformulation`.
  - Action: Immediately suspend from the active daily review queue to stop time waste.
  - Reformulation: High-frequency leeches are reformulated (e.g., converted from an ambiguous sentence into a high-contrast audio-first minimal pair or simplified kernel frame).

---

## 5. Card Architecture: The 4 Standardized Note Types

To maintain minimal cognitive load and fast review speed (averaging $<6$ seconds per card):

| Note Type ID | Pedagogical Purpose | Prompt (Front) | Target Answer (Back) | Review Target Time |
| :--- | :--- | :--- | :--- | :---: |
| **CARD-01: Lean Receptive Lemma** | Initial form-meaning mapping for top 500 concrete nouns/verbs. | English word + native audio | Portuguese translation + definition + image/example | 3–5 seconds |
| **CARD-02: Contextual Sentence Cloze** | Polysemy, prepositions, collocations, grammatical inflections. | Sentence with `{{c1::target}}` blanked + sentence audio | Complete sentence + target word + brief note | 6–10 seconds |
| **CARD-03: Audio Discrimination** | Phonemic discrimination (minimal pairs, connected speech). | Audio sample playing Word A or B (no text) | Correct word identification + IPA transcription | 3–5 seconds |
| **CARD-04: Functional Productive Prompt** | Spontaneous lexical retrieval in professional contexts. | Situational cue in Portuguese/English | Natural English phrase + target audio | 5–8 seconds |

---

## 6. Official Configuration Baseline for Phase 03

- **Scheduler**: Native Anki FSRS.
- **Desired Retention**: `0.90` (initial default).
- **Learning Steps**: `10m` (single step per official FSRS documentation; avoid complex multi-step legacy queues).
- **Relearning Steps**: `10m`.
- **Maximum Interval**: `365d` (1 year).
- **Optimizer Trigger**: Run FSRS parameter optimization only after the learner logs $\ge 1,000$ total reviews.

---

## 7. Authoritative References

1. Anki Documentation (2024). *FSRS: Free Spaced Repetition Scheduler*. Official Anki Manual. [https://docs.ankiweb.net/deck-options.html#fsrs](https://docs.ankiweb.net/deck-options.html#fsrs)
2. Ye, J. (2023). *FSRS: Free Spaced Repetition Scheduler — Theoretical Foundation and Benchmark Results*. Open-Spaced-Repetition. [https://github.com/open-spaced-repetition/fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)
3. Settles, B., & Meeder, B. (2016). A trainable spaced repetition model for language learning. *Proceedings of the 54th Annual Meeting of the ACL*, 1848-1858. doi:10.18653/v1/P16-1174
4. Wozniak, P. A. (1995). *Economics of learning*. SuperMemo Theoretical Papers.
