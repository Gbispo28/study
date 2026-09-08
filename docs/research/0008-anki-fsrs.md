# Research Note 0008: Anki & Modern FSRS Scheduling Architecture

- **Date**: 2026-09-08 (Audited & Aligned with Anki 25.07+ Documentation — September 2026)
- **Domain**: Spaced Repetition Algorithms, Mathematical Memory Modeling, Card Architecture
- **Primary Investigator**: Anki / SRS Specialist & Orchestrator
- **Epistemic Classification**: `STRONG EVIDENCE` (FSRS Algorithm & DSR Modeling) / `EXPERT CONSENSUS` (Official Anki Manual Guidance)

---

## 1. Research Question

How does the native Free Spaced Repetition Scheduler (FSRS) integrated into modern Anki function, what are the empirical workload trade-offs across different Desired Retention settings, how should the native Anki Simulator and current official guidance replace retired legacy tools, and what card architecture guardrails prevent Anki from consuming the learner's 60-minute daily budget?

---

## 2. Mathematical Foundations: The Three-Component DSR Model

Modern Anki natively integrates FSRS (developed by Jarrett Ye and the Open-Spaced-Repetition initiative), replacing the heuristic SM-2 algorithm with a mathematically grounded model:
- **Stability ($S$)**: The time (in days) required for the retrievability of a memory trace to decrease from 100% to the target desired retention $R$.
- **Retrievability ($R$)**: The probability of successfully recalling an item at elapsed time $t$, modeled by a power forgetting curve:
  $$R(t, S) = \left(1 + \text{FACTOR} \cdot \frac{t}{S}\right)^{-w}$$
- **Difficulty ($D$)**: The inherent cognitive resistance of an item to consolidation, dynamically updated on a 1–10 scale based on user grading (Again, Hard, Good, Easy).

### 2.1 Predictive Superiority Over Legacy SM-2
Large-scale benchmark evaluations across open review log datasets (Open-Spaced-Repetition benchmark on 20,000+ user collections) indicate that **FSRS models memory decay with substantially lower log-loss and root-mean-squared error compared to SM-2**. In simulation benchmarks, FSRS achieves equivalent retention with fewer total reviews than SM-2 while eliminating the structural "Ease Hell" trap of SM-2. However, exact review savings vary by user review consistency and card type and should be treated as benchmark simulation findings rather than universal guarantees for every learner.

---

## 3. Desired Retention, Simulator Guidance & Workload Trade-offs

### 3.1 Workload Trade-offs and Retention Dynamics
In FSRS, review intervals shorten as Desired Retention ($R$) approaches 1.0 (100%):
- *Higher Retention ($R \ge 0.90$)*: Generates shorter intervals and higher daily review counts, but delivers high recall stability and a lower lapse rate (~10% or less).
- *Lower Retention ($R \le 0.85$)*: Lengthens intervals and reduces short-term scheduling volume, but increases the lapse rate (~15% or higher), resulting in more frequent failed reviews and relearning cycles.
- *Extreme Retention ($R \ge 0.95$)*: Causes an aggressive workload escalation as intervals become extremely compressed, yielding minimal pedagogical benefit for exponential daily reviews.

### 3.2 Historical Context: Removal of CMRR (Anki 25.07)
> [!NOTE]
> **Historical Retrospective**: Early FSRS implementations in Anki included an experimental feature called *Compute Minimum Recommended Retention (CMRR)*. In official Anki documentation beginning with version 25.07, CMRR was **explicitly marked as a Removed Feature**. It was removed because the mathematical optimization frequently produced unhelpful, static baseline values (e.g., recommending 70% retention regardless of context) that failed to reflect authentic learner experience or communicative needs.

### 3.3 Current Official Decision Mechanisms: Simulator & Help Me Decide
In modern Anki (25.07+), workload and retention trade-offs are evaluated using:
1. **The Built-in FSRS Simulator**: Models projected daily review volume based on target retention, daily new card count, and historical deck parameters.
2. **Help Me Decide / Retention Hints**: Evaluates the learner's historical review log to guide retention selection based on available daily study time.

---

## 4. Parameter Classification Matrix for English Learning OS

To avoid transforming software defaults into pedagogical dogmas, every scheduling parameter is formally classified:

| Parameter | Current Value | Canonical Classification | Technical & Pedagogical Rationale |
| :--- | :---: | :--- | :--- |
| **Desired Retention** | `0.90` (90%) | `OFFICIAL DEFAULT` & `PROJECT OPERATIONAL DEFAULT` | Official Anki starting default. Provides high initial recognition stability for foundational vocabulary (top 1,000 lemmas) where high lapse rates cause frustration. Dynamic adjustment evaluated later via Simulator. |
| **Maximum Interval** | `36500d` (~100y) | `OFFICIAL DEFAULT` | Anki's official default is 36500 days. Artificially restricting the maximum interval (e.g., to 365 days) artificially forces mature cards to be reviewed repeatedly, unnecessarily inflating daily workload. |
| **Learning Steps** | Empty or `10m` | `CURRENT OFFICIAL GUIDANCE` / `EXPERIMENTAL` | Official documentation advises keeping learning steps shorter than one day and keeping their count low. Leaving steps empty allows FSRS to govern short-term scheduling experimentally. Project default uses `10m` or empty based on Anki version. |
| **Relearning Steps** | Empty or `10m` | `CURRENT OFFICIAL GUIDANCE` / `EXPERIMENTAL` | Aligns with learning steps. Single short step or empty for native FSRS control. |
| **Optimization Trigger** | After review history exists | `CURRENT OFFICIAL GUIDANCE` | Official health guidance warns against optimizing on fewer than a few hundred reviews. The previously cited universal "1,000 reviews" threshold is an illustrative benchmark, not an absolute software lock. |
| **Leech Threshold** | `4 lapses` | `PROJECT OPERATIONAL DEFAULT` | Official default is 8 lapses. The English Learning OS lowers this to 4 lapses specifically to prevent difficult cards from consuming the strict 15-minute daily SRS budget. |
| **New Card Pacing** | `5–10 cards/day` | `PROJECT OPERATIONAL DEFAULT` | Derived strictly from the 15-minute daily timebox constraint, ensuring total review volume remains sustainable. |

---

## 5. Workload Guardrails in a 60-Minute Daily Routine

To prevent flashcards from crowding out essential communicative listening, speaking, and reading:

### 5.1 Daily Review Cap & Throttling Invariant
- **Daily SRS Timebox**: **15 minutes** (absolute hard stop at 20 minutes).
- **New Card Introductions**: Capped at **5 to 10 new cards per day**.
- **Automatic Throttling Invariant**:
  $$\text{If } \text{Daily Reviews} > 15 \text{ min } \implies \text{New Cards Introduced} = 0$$

### 5.2 Leech Management Policy
- **Definition**: A card that has lapsed 4 separate times after initial learning.
- **Action**: Tagged `leech_pending_reformulation` and automatically suspended from the active daily queue.
- **Pedagogical Remedy**: High-utility leeches are reformulated (e.g., converted from ambiguous text clozes into high-contrast audio-first minimal pairs or simplified functional frames).

---

## 6. Card Architecture: 4 Standardized Note Types

Card designs must minimize cognitive friction and maintain rapid, focused retrieval:

| Note Type ID | Pedagogical Focus | Prompt (Front) | Target Answer (Back) | Pacing Target |
| :--- | :--- | :--- | :--- | :---: |
| **CARD-01: Lean Receptive Lemma** | Initial form-meaning mapping for top 500 concrete lemmas. | English word + native audio | Portuguese translation + definition + example | ~3–5 sec |
| **CARD-02: Contextual Sentence Cloze** | Polysemy, prepositions, collocations, grammatical frames. | Sentence with `{{c1::target}}` blanked + sentence audio | Complete sentence + target word + brief note | ~6–10 sec |
| **CARD-03: Audio Discrimination** | Phonemic discrimination (minimal pairs, connected speech). | Audio sample playing Word A or B (no text) | Correct word identification + IPA transcription | ~3–5 sec |
| **CARD-04: Functional Productive Prompt** | Spontaneous lexical retrieval in professional scenarios. | Situational cue in Portuguese/English | Natural English phrase + target audio | ~5–8 sec |

---

## 7. Authoritative References

1. Anki Documentation (2026). *Deck Options — FSRS*. Official Anki Manual. [https://docs.ankiweb.net/deck-options.html#fsrs](https://docs.ankiweb.net/deck-options.html#fsrs) (Verified September 2026).
2. Ye, J. (2023). *FSRS: Free Spaced Repetition Scheduler — Theoretical Foundation and Benchmark Results*. Open-Spaced-Repetition. [https://github.com/open-spaced-repetition/fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)
3. Settles, B., & Meeder, B. (2016). A trainable spaced repetition model for language learning. *Proceedings of the 54th Annual Meeting of the ACL*, 1848-1858. doi:10.18653/v1/P16-1174
4. Wozniak, P. A. (1995). *Economics of learning*. SuperMemo Theoretical Papers.
