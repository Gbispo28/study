# Research Note 0010: The 60-Minute Daily Allocation Policy & Cognitive Budgeting

- **Date**: 2026-09-08
- **Domain**: Instructional Design, Cognitive Budgeting, Habit Architecture
- **Primary Investigator**: Product Architect & Orchestrator
- **Epistemic Classification**: `STRONG EVIDENCE` (Cognitive Load & Time-Boxing) / `EXPERT CONSENSUS` (Deliberate Practice Scheduling)

---

## 1. Research Question

How should exactly 60 minutes of daily deliberate English study be operationally structured, time-boxed, and dynamically allocated across skill modalities to maximize communicative acquisition while preventing cognitive burnout, fake precision, and SRS saturation?

---

## 2. Core Operational Principles: Policy Before Mathematics

### 2.1 The Inviolable 60-Minute Daily Timebox
- **Human Reality**: The learner is a working professional dedicating exactly 60 focused minutes per day to language acquisition.
- **Cognitive Load & Deliberate Practice**: High-intensity deliberate practice exhibits steep diminishing returns beyond 50–60 minutes per day for working adults (Ericsson, 2006; Sweller, 2011). Exceeding 60 minutes risks cognitive fatigue, habit erosion, and abandonment.
- **Strict Prohibition of Fake Precision**: We reject pseudo-mathematical optimization formulas that pretend to calculate human learning down to decimal percentages. The system relies on **clear operational rules, priority hierarchies, and cognitive boundaries**.

### 2.2 Core Study vs. Ambient / Bonus Exposure
To preserve scientific validity, the system maintains a strict boundary between two classes of exposure:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       TOTAL DAILY ENGLISH EXPOSURE                      │
│                                                                         │
│   ┌───────────────────────────────────┐ ┌───────────────────────────┐   │
│   │        CORE STUDY (60 MIN)        │ │  AMBIENT / BONUS EXPOSURE │   │
│   │   • Inviolable daily commitment   │ │  • Strictly optional      │   │
│   │   • High deliberate attention     │ │  • Low cognitive demand  │   │
│   │   • Active retrieval & feedback   │ │  • Background podcasts    │   │
│   │   • Tracked by system metrics     │ │  • OS UI in English       │   │
│   │   • Governed by allocation engine │ │  • Entertainment / YouTube│   │
│   │   • Guaranteed habit core         │ │  • NOT counted toward 60m │   │
│   └───────────────────────────────────┘ └───────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

**The Core Invariant**: The English Learning OS must be completely viable and effective if ambient exposure is **exactly zero**. Ambient exposure serves as supplementary enrichment, never as an excuse for an ineffective core session.

---

## 3. The 3-Block Modular Allocation Policy

Rather than rigid daily fragmentation, the 60-minute session is divided into three functional blocks with strict time ceilings:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    60-MINUTE DAILY SESSION STRUCTURE                 │
├─────────────────────┬──────────────────────────┬─────────────────────┤
│ BLOCK 1: RETRIEVAL  │  BLOCK 2: FOCUSED INPUT  │ BLOCK 3: PRODUCTION │
│   & CONSOLIDATION   │       & DECODING         │    & EXPRESSION     │
│    (15–20 min)      │       (25–30 min)        │     (10–15 min)     │
├─────────────────────┼──────────────────────────┼─────────────────────┤
│ • Anki/FSRS review  │ • Reading-while-listening│ • Speaking w/ AI    │
│ • Due cards only    │ • Graded readers / VOA   │ • Sentence combining│
│ • 5–10 new cards    │ • Bottom-up decoding     │ • Pronunciation     │
│ • Hard stop at 20m  │ • Lexical noticing       │ • Micro-writing     │
└─────────────────────┴──────────────────────────┴─────────────────────┘
```

### 3.1 Block 1: Retrieval & Consolidation (15–20 minutes)
- **Cognitive Purpose**: Exploit early session alertness to perform high-effort active recall before working memory is depleted.
- **Activities**: Review all due FSRS flashcards in Anki/AnkiDroid; introduce 5 to 10 new cards maximum.
- **Hard Guardrail**: If reviews take longer than 20 minutes, review stops immediately. Unreviewed cards roll over to the next day, and new card introductions are automatically paused.

### 3.2 Block 2: Focused Comprehensible Input & Decoding (25–30 minutes)
- **Cognitive Purpose**: Expose the brain to high-volume language at $\ge 95\%$ comprehension ($i+1$), reinforcing recently primed vocabulary in rich syntactic context.
- **Activities**:
  - Bimodal input (reading-while-listening with synchronized audio/transcript).
  - Bottom-up acoustic decoding of connected speech clips (flapping, reductions).
  - Mining 2–3 new high-utility sentences for future card creation.

### 3.3 Block 3: Production, Articulation & Expression (10–15 minutes)
- **Cognitive Purpose**: Force the shift from semantic decoding to syntactic encoding (Swain's Output Hypothesis), practicing articulatory muscle memory and conversational agility.
- **Activities**:
  - 10-minute structured dialogue with AI conversational partner (Gemini Live).
  - Contrastive pronunciation micro-drills (epenthesis suppression, vowel minimal pairs).
  - Sentence-combining writing exercise (2–3 combined sentences).

---

## 4. The Routine Allocation Engine: Priority & Decision Rules

The daily assignment for Block 2 and Block 3 is governed by an explainable decision hierarchy:

```
                ┌──────────────────────────────────┐
                │ Daily Routine Allocation Engine  │
                └─────────────────┬────────────────┘
                                  │
                                  ▼
               Rule 1: Review Workload Protection
               • IF due reviews > 80: Cap Block 1 at 20 min, set new cards = 0.
               • IF due reviews <= 40: Normal Block 1 (15 min), introduce 8 new cards.
                                  │
                                  ▼
               Rule 2: Bottleneck Targeting
               (Derived from baseline diagnostic vector P):
               • IF Listening < Reading: Prioritize acoustic decoding and
                 connected speech in Block 2.
               • IF Pronunciation epenthesis is severe: Prioritize stop closure
                 micro-drills in Block 3.
               • IF Spoken fluency is zero: Prioritize controlled AI dialogue
                 scenarios in Block 3.
                                  │
                                  ▼
               Rule 3: Modality Interleaving Rotation
               • Mon: Reading-while-listening + AI Speaking Dialogue
               • Tue: Acoustic Decoding (Dictation) + Sentence Combining
               • Wed: Graded Reader Reading + Pronunciation Articulation
               • Thu: Bimodal Listening + AI Speaking Dialogue
               • Fri: Extensive Review + Functional Writing Composition
               • Sat: Diagnostic Check / Formative Micro-assessment (Optional)
               • Sun: Rest / Light Ambient Exposure (0 core minutes)
```

---

## 5. Single Continuous Session vs. Split-Block Schedule

The system supports two certified operational schedules depending on daily workflow:

| Schedule Mode | Daily Structure | Pedagogical Rationale | Target Persona Context |
| :--- | :--- | :--- | :--- |
| **Mode A: Continuous 60-Minute Block** | 60 continuous minutes (e.g., 07:00–08:00 or 20:00–21:00) on MacBook Air M4. | High immersion, zero context switching, complete daily closure in one sitting. | Optimal for deep-focus learners with an uninterrupted morning/evening window. |
| **Mode B: Split 20m + 40m Blocks** | Block 1 (20m AnkiDroid) during morning routine/transit + Block 2 & 3 (40m Mac) in evening. | Reduces single-session cognitive fatigue; spaces retrieval from input by several hours (spacing benefit). | Optimal for busy work schedules; leverages Galaxy S24 Ultra for morning mobile SRS. |

---

## 6. Architectural Implications for English Learning OS

1. **Session Timebox Enforcement**: The system must track session time and warn the user at 55 minutes to prompt a clean wrap-up at 60 minutes.
2. **Workload Throttling Policy**: If daily reviews exceed 15 minutes, new card introductions are set to 0.
3. **No Streak Shaming**: Consistency metrics must track 7-day rolling adherence rather than fragile, punitive daily streaks.

---

## 7. Authoritative References

1. Ericsson, K. A. (2006). The influence of experience and deliberate practice on the development of superior expert performance. *Cambridge Handbook of Expertise*, 685-705.
2. Sweller, J. (2011). Cognitive load theory. *Psychology of Learning and Motivation*, 55, 37-76. doi:10.1016/B978-0-12-387693-5.00002-8
3. Newport, C. (2016). *Deep work: Rules for focused success in a distracted world*. Grand Central Publishing.
4. Clear, J. (2018). *Atomic habits*. Penguin.
