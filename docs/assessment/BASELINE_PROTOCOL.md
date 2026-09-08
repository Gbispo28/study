# Baseline Assessment Protocol: English Learning OS

- **Purpose**: A standardized, reproducible diagnostic test battery designed to establish the multi-dimensional baseline proficiency profile of an adult Brazilian Portuguese native speaker entering the system.
- **Estimated Completion Time**: ~60 minutes total (administered across two separate sessions).
- **Evaluation Range**: **Pre-A1 through C2** (with adaptive routing and early stopping).
- **Required Equipment**: MacBook Air M4 or Galaxy S24 Ultra, standard headphones with microphone.
- **Copyright & Attribution Notice**: Test methodologies are informed by the Council of Europe CEFR Companion Volume (2020), the English Profile, and Paul Nation's Vocabulary Levels Test (VLT) framework. All specific test prompts, reading passages, and items below are original custom diagnostic items created for the English Learning OS and do NOT constitute a standardized psychometric exam.

---

## Part A: Listening Comprehension Battery (15 minutes)

### Task A1: Acoustic Speed & Reduction Discrimination (3 core items)
*Instructions: Listen to each audio clip twice at normal native speech rate (1.0x). Answer the comprehension question without written text.*

1. **Audio Clip 1 (Connected Speech - Reductions & Flapping)**:
   - *Spoken Audio*: *"I was gonna get a cup of water, but the machine is out of order."*
   - *Question (Multiple Choice)*: What did the speaker try to do?
     - [a] Fix the broken machine.
     - [b] Drink some water.
     - [c] Order a new cup online.
     - [d] Wash the dishes.
   - *Target Key*: [b]. (Tests parsing of *gonna*, flapping in *water*, and reduction in *out of*).
2. **Audio Clip 2 (Technical Workplace Discourse)**:
   - *Spoken Audio*: *"The deployment failed because the database credentials expired at midnight."*
   - *Question*: Why did the deployment fail?
     - [a] The server ran out of disk space.
     - [b] The database password/key stopped working at 12:00 AM.
     - [c] Someone cancelled the script.
     - [d] The network connection was too slow.
   - *Target Key*: [b].
3. **Audio Clip 3 (Prepositional & Temporal Markers)**:
   - *Spoken Audio*: *"We’re meeting on Tuesday morning at ten, not Thursday."*
   - *Question*: When is the meeting?
     - [a] Thursday at 10:00 AM.
     - [b] Tuesday at 10:00 AM.
     - [c] Tuesday at 2:00 PM.
     - [d] Thursday afternoon.
   - *Target Key*: [b].

### Task A2: Micro-Dictation / Bottom-Up Decoding (4 items)
*Instructions: Listen to each short sentence spoken at conversational speed and type the exact words heard. Tests acoustic segmentation.*
1. Item 1: *"Can you send me the file?"* [Audio: /kən jə sɛnd miː ðə faɪl/]
2. Item 2: *"What did you do yesterday?"* [Audio: /wʌdʒə duː jɛstɚdeɪ/]
3. Item 3: *"I've been working on this bug."* [Audio: /aɪv bɪn wɜːrkɪŋ ɑːn ðɪs bʌɡ/]
4. Item 4: *"There’s a problem with the server."* [Audio: /ðɛrz ə prɑːbləm wɪð ðə sɜːrvɚ/]

### Optional Extension Task A3: Advanced Acoustic Parsing (C1/C2 Routing)
*(Administered only if learner scores 100% on Task A1 and A2)*
- *Spoken Audio (Fast, Multi-speaker, Idiomatic)*: *"Look, had we known the upstream broker was throttling the event stream, we wouldn't have spun up redundant consumer instances in the first place."*
- *Question*: What is the speaker's core realization regarding the system architecture?
  - *Target Response*: Explaining that redundant consumer instances were created unnecessarily due to lack of visibility into upstream broker throttling.

---

## Part B: Reading Comprehension Battery (10 minutes)

### Task B1: General Syntax & Inferencing (Core A2/B1 Passage)
*Read the following short passage and answer the questions:*

> "Alex arrived at the office at 8:30 AM. His team had planned to release the new software update before noon. However, when Alex checked the monitoring dashboard, he noticed that CPU usage was unusually high. Instead of pushing the update immediately, he decided to investigate the memory logs with Maria. By 11:00 AM, they discovered a memory leak in the data ingestion pipeline, fixed the bug, and safely deployed the update at 1:30 PM."

1. **Item 1 (Detail Recall)**: At what time was the update originally supposed to be released?
   - [a] 8:30 AM | [b] Before 12:00 PM (noon) | [c] 11:00 AM | [d] 1:30 PM
2. **Item 2 (Lexical & Syntactic Inferencing)**: What does the phrase *"Instead of pushing the update immediately"* mean?
   - [a] Alex pushed the update right away.
   - [b] Alex chose not to deploy the update immediately so he could check the logs first.
   - [c] Alex cancelled the update permanently.
   - [d] Maria deployed the update without telling Alex.
3. **Item 3 (Temporal Logic)**: When was the bug actually fixed?
   - [a] At 8:30 AM | [b] Around 11:00 AM | [c] At 1:30 PM | [d] After midnight

### Optional Extension Task B2: Complex Architecture Reasoning (C1/C2 Routing)
*(Administered only if learner scores 3/3 on Task B1)*
> "While eventual consistency models offer significant throughput advantages in globally distributed partitions, they inevitably introduce non-trivial reconciliation overhead during network split-brain scenarios, forcing data engineers to implement idempotent deduplication logic at the application layer."

- *Question*: According to the passage, why must data engineers write idempotent deduplication logic?
  - *Target Evaluation*: Identifies that network partitions under eventual consistency create reconciliation overhead, requiring application-layer safeguards.

---

## Part C: Spoken Production & Interaction Battery (10 minutes)

### Task C1: Sustained Monologue (Describing Professional Routine)
- **Prompt**: *"Describe what you do on a typical working day as a software/data professional. Talk for 60 to 90 seconds. Include: 1) What time you start working, 2) What tools or languages you use, and 3) What kind of problems you solve."*
- **Scoring Rubric**: Evaluated on Intelligibility, Lexical Range, Grammatical Accuracy, Fluency, and Hesitation/Repair via [CEFR_RUBRIC.md](./CEFR_RUBRIC.md) across bands Pre-A1 through C2.

### Task C2: Elicited Communicative Interaction (Scenario Simulation)
- **Prompt**: *"Imagine your deployment script failed right before a critical demo. Explain the situation to your team leader in 2–3 sentences, tell them why it happened, and state when you expect it to be resolved."*

---

## Part D: Pronunciation & Articulatory Mechanics (10 minutes)

### Task D1: Phonemic Perception (Minimal Pair Discrimination)
*Instructions: Listen to each pair of spoken words and indicate whether the two words are IDENTICAL or DIFFERENT.*
1. `/ʃɪp/` vs `/ʃiːp/` (*ship* vs *sheep*) $\rightarrow$ [DIFFERENT]
2. `/bæd/` vs `/bɛd/` (*bad* vs *bed*) $\rightarrow$ [DIFFERENT]
3. `/lɪv/` vs `/lɪv/` (*live* vs *live*) $\rightarrow$ [IDENTICAL]
4. `/pʊl/` vs `/puːl/` (*pull* vs *pool*) $\rightarrow$ [DIFFERENT]
5. `/kʌp/` vs `/kɑːp/` (*cup* vs *cop*) $\rightarrow$ [DIFFERENT]

### Task D2: Articulatory Production (Candidate BP Interference Targets)
*Instructions: Record yourself reading the following sentences aloud. Evaluated for candidate difficulties (epenthesis, nasal closure, vowel quality, and word stress).*
1. Target 1 (Stop Epenthesis Candidate): *"I need to **stop** and check my **laptop** before the **big** meeting."*
2. Target 2 (/i/ vs /ɪ/ Candidate): *"He wants to **live** in this city and **eat** good food."*
3. Target 3 (Word Stress & Tonic Syllable): *"Our **development** team solved the **database** problem."*
4. Target 4 (Coda Nasal Closure): *"Can you **come** and see my **plan** this **afternoon**?"*

---

## Part E: Written Composition & Sentence Combining (10 minutes)

### Task E1: Sentence Combining (Syntactic Synthesis)
*Combine each pair of simple kernel sentences into ONE grammatically correct English sentence without changing the meaning:*

1. Kernel: *The database was very slow.* / *We optimized the query index.*
   - *Target Combined Frame*: (e.g., *"Because the database was very slow, we optimized the query index."*)
2. Kernel: *Alex pushed the code to GitHub.* / *The automated tests passed successfully.*
   - *Target Combined Frame*: (e.g., *"Alex pushed the code to GitHub after the automated tests passed successfully."*)
3. Kernel: *I wanted to attend the conference.* / *I had too many production deadlines.*
   - *Target Combined Frame*: (e.g., *"Although I wanted to attend the conference, I had too many production deadlines."*)

### Task E2: Short Functional Workplace Communication
- **Prompt**: *"Write a short Slack message (3 to 4 sentences) to a colleague telling them: 1) You are working on the reporting dashboard today, 2) You found an error in the sales calculation, and 3) Asking them if they have 10 minutes to discuss it this afternoon."*

---

## Part F: Operational Grammar in Use (5 minutes)

1. *Verb Aspect*: "Right now, Maria ____________ (debug) the API, but she usually ____________ (write) data pipelines."
2. *Simple Past*: "Yesterday, we ____________ (find) the root cause and ____________ (bring) the server back online."
3. *Modal / Ability*: "I ____________ (not can / cannot) access the staging server without VPN credentials."
4. *Prepositions of Time*: "The sprint planning starts ____________ 9:00 AM ____________ Monday."

---

## Part G: Lexical Size & Depth Sampling (5 minutes)

*Match each numbered word on the left with its closest definition on the right:*

### K1 Band (Top 1,000 Lemmas)
1. **agree** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [a] to have the same opinion
2. **happen** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [b] to occur or take place
3. **protect** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [c] to keep something safe from danger

### K2 Band (1,001–2,000 Lemmas)
1. **maintain** &nbsp;&nbsp; [a] to make something continue in good condition
2. **predict** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [b] to say what will happen in the future
3. **reduce** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [c] to make something smaller in size or amount

### K3 Band (2,001–3,000 Lemmas)
1. **accurate** &nbsp;&nbsp; [a] correct and exact without errors
2. **crucial** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [b] extremely important or necessary
3. **efficient** &nbsp;&nbsp;&nbsp; [c] working well without wasting time or energy

---

## Execution Protocol & Storage

- Learner answers and audio recordings are stored in:
  `docs/assessment/results/baseline_YYYYMMDD/`
- Evaluation follows [SCORING_MODEL.md](./SCORING_MODEL.md) and [CEFR_RUBRIC.md](./CEFR_RUBRIC.md).
