# Research Note 0010: The 60-Minute Daily Allocation Policy & Cognitive Budgeting

- **Date**: 2026-09-08
- **Domain**: Instructional Design, Cognitive Budgeting, Habit Architecture
- **Primary Investigator**: Product Architect & Orchestrator
- **Epistemic Classification**: `STRONG EVIDENCE` (Cognitive Load & Time-Boxing) / `EXPERT CONSENSUS` (Deliberate Practice Schedulers)

---

## 1. Research Question

How should exactly 60 minutes of daily deliberate English study be mathematically structured, time-boxed, and dynamically allocated across skill modalities to maximize communicative acquisition while preventing cognitive burnout and SRS saturation?

---

## 2. Core Operational Constraints & Distinctions

### 2.1 The Inviolable 60-Minute Time Ceiling
- **Human Constraint**: The learner is a working software/data professional dedicating exactly 60 focused minutes per day to English acquisition.
- **Cognitive Science Constraint (CLT & Deliberate Practice)**: High-intensity deliberate practice exhibits steep diminishing returns beyond 50–60 minutes per day for working adults (Ericsson, 2006; Sweller, 2011). Exceeding 60 minutes creates chronic fatigue, habit erosion, and eventual abandonment.
- **Strict Prohibition of Fake Precision**: We do NOT assign fixed, rigid percentages (e.g., "exactly 25% listening, 25% reading, 25% speaking, 25% writing" every single day). Fixed schedules ignore individual skill bottlenecks, due SRS fluctuations, and natural learning phases.

### 2.2 Core Study vs. Ambient / Bonus Exposure
To preserve scientific validity and accountability, we establish a strict boundary between two classes of exposure:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       TOTAL DAILY ENGLISH EXPOSURE                      │
│                                                                         │
│   ┌───────────────────────────────────┐ ┌───────────────────────────┐   │
│   │        CORE STUDY (60 MIN)        │ │  AMBIENT / BONUS EXPOSURE │   │
│   │   • Inviolable daily commitment   │ │  • Optional / Variable    │   │
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
- **Cognitive Purpose**: Exploit morning cognitive alertness to perform high-effort active recall before working memory is depleted by other tasks.
- **Activities**:
  - Review all due FSRS flashcards in Anki/AnkiDroid.
  - Introduce 5 to 10 new cards maximum.
- **Hard Guardrail**: If reviews take longer than 20 minutes, the session stops immediately. Unreviewed cards roll over to the next day, and the system triggers an automatic throttle on new card introductions.

### 3.2 Block 2: Focused Comprehensible Input & Decoding (25–30 minutes)
- **Cognitive Purpose**: Expose the brain to high-volume authentic/graded language at $\ge 95\%$ comprehension ($i+1$), reinforcing recently primed vocabulary in rich syntactic context.
- **Activities**:
  - Bimodal input (reading-while-listening with synchronized transcript).
  - Bottom-up acoustic decoding of connected speech clips (flapping, reductions).
  - Mining 2–3 new high-utility sentences for future card creation.

### 3.3 Block 3: Production, Articulation & Expression (10–15 minutes)
- **Cognitive Purpose**: Force the shift from semantic decoding to syntactic encoding (Swain's Output Hypothesis), practicing articulatory muscle memory and conversational agility.
- **Activities**:
  - 10-minute structured dialogue with AI conversational partner (Gemini Live).
  - Contrastive pronunciation micro-drill (epenthesis suppression, vowel minimal pair).
  - Sentence-combining writing exercise (2–3 combined sentences).

---

## 4. The Routine Allocation Engine: Dynamic Scheduling Policy

How does the future system decide what to assign for Block 2 and Block 3 each day? The decision model is governed by a deterministic priority hierarchy:

```
                ┌──────────────────────────────────┐
                │ Daily Routine Allocation Engine  │
                └─────────────────┬────────────────┘
                                  │
                                  ▼
               Step 1: Check Due SRS Review Volume
               • If due reviews > 80: Cap Block 1 at 20m, 0 new cards.
               • If due reviews <= 40: Normal Block 1 (15m), +8 new cards.
                                  │
                                  ▼
               Step 2: Identify Primary Skill Bottleneck
               (From baseline diagnostic vector P):
               • If Listening < Reading - 1 band: Weight Block 2 toward
                 acoustic decoding & connected speech.
               • If Pronunciation/Intelligibility is critical: Weight Block 3
                 toward epenthesis suppression & stress drills.
               • If Speaking Spontaneity is zero: Weight Block 3 toward
                 controlled AI dialogue frames.
                                  │
                                  ▼
               Step 3: Enforce Interleaving Schedule
               (Rotate secondary emphasis across 5-day cycle):
               • Day 1 (Mon): Reading-while-listening + AI Speaking Dialogue
               • Day 2 (Tue): Acoustic Decoding (Dictation) + Sentence Combining
               • Day 3 (Wed): Graded Reader Reading + Pronunciation Articulation
               • Day 4 (Thu): Bimodal Listening + AI Speaking Dialogue
               • Day 5 (Fri): Extensive Review + Functional Writing Composition
               • Day 6 (Sat): Diagnostic Check / Milestone Check (Optional)
               • Day 7 (Sun): Rest / Light Ambient Exposure (0 core minutes)
```

---

## 5. Single Continuous Session vs. Split-Block Schedule

The system supports two certified operational schedules depending on learner lifestyle:

| Mode | Configuration | Advantages | Target Persona Context |
| :--- | :--- | :--- | :--- |
| **Mode A: Single 60-Minute Block** | 60 continuous minutes (e.g., 07:00–08:00 or 20:00–21:00) on MacBook Air M4. | High immersion, zero context switching, complete daily closure in one sitting. | Preferred for deep-focus learners with an uninterrupted morning/evening window. |
| **Mode B: Split 20m + 40m Blocks** | Block 1 (20m AnkiDroid) during morning transit/routine + Block 2 & 3 (40m Mac) in evening. | Reduces single-session cognitive fatigue; spaces retrieval from input by several hours (spacing benefit). | Preferred for busy work schedules; leverages Galaxy S24 Ultra for morning SRS. |

Both modes are pedagogically equivalent and fully supported by the system architecture.

---

## 6. Architectural Implications for English Learning OS

1. **Strict 60-Minute Timer**: The software engine must track session time and warn the user when approaching 55 minutes, prompting a clean wrap-up at 60 minutes.
2. **Workload Throttling Logic**:
   $$\text{If } \text{Daily Reviews} > 15 \text{ minutes } \implies \text{New Cards Introduced} = 0$$
3. **No Streak Shaming**: Consistency metrics must track 7-day rolling adherence rather than fragile, punitive daily streaks that induce demotivation after a single missed day.

---

## 7. Authoritative References

1. Ericsson, K. A. (2006). The influence of experience and deliberate practice on the development of superior expert performance. *The Cambridge Handbook of Expertise and Expert Performance*, 38, 685-705.
2. Sweller, J. (2011). Cognitive load theory. *Psychology of Learning and Motivation*, 55, 37-76. doi:10.1016/B978-0-12-387693-5.00002-8
3. Newport, C. (2016). *Deep work: Rules for focused success in a distracted world*. Grand Central Publishing.
4. Clear, J. (2018). *Atomic habits: An easy & proven way to build good habits & break bad ones*. Penguin.
