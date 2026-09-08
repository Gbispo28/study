# Product Requirements: English Learning OS

> **Governance Note**: Every item in this document is categorized strictly by certainty level. Hypotheses must never be treated as confirmed requirements until empirical validation or explicit user confirmation occurs.

---

## 1. Confirmed Requirements

- [REQ-01] **Single Learner Focus**: Optimized specifically for the primary user (Brazilian native Portuguese speaker, tech/data background).
- [REQ-02] **Beginner Starting Point**: Curriculum and routines must assume near-zero foundational English (CEFR A0/A1).
- [REQ-03] **Strict 60-Minute Daily Budget**: Daily learning workflows must fit inside 60 total minutes without spilling over into cognitive burnout.
- [REQ-04] **Memory Science Integration**: The learning methodology must prioritize active recall, spaced repetition, retrieval practice, and comprehensible input.
- [REQ-05] **Hardware Compatibility**: Must support workflows across MacBook Air M4 (macOS) and Galaxy S24 Ultra (Android).
- [REQ-06] **Anki / AnkiDroid Alignment**: Must integrate with or produce compatible assets for Anki desktop and AnkiDroid mobile.
- [REQ-07] **Holistic Language Competencies**: Must address all core competencies: Speaking, Listening, Reading, Writing, Pronunciation, and Grammar.
- [REQ-08] **Progress Traceability**: The system must provide measurable metrics of mastery, vocabulary accumulation, and study consistency.
- [REQ-09] **Agent-First Foundation**: The repository must support multi-agent development with Google Antigravity 2.0, Gemini, and Claude Code Pro without vendor lock-in.

---

## 2. Working Hypotheses

- [HYP-01] *Sentence Mining vs Word Lists*: Contextual sentence cards (cloze deletions with audio) will produce 2x higher retention than isolated word translation cards for this user.
- [HYP-02] *FSRS Algorithm Efficiency*: FSRS with an 85% retention target will minimize daily Anki review load compared to default Anki SM-2.
- [HYP-03] *Phonemic Training Precedence*: Prioritizing phoneme discrimination (minimal pairs) in weeks 1-4 will prevent fossilized pronunciation errors common among Portuguese speakers.
- [HYP-04] *AI Conversational Scaffolding*: Controlled AI dialogue drills with real-time speech-to-text and grammar feedback will reduce anxiety compared to open-ended conversational apps.

---

## 3. Open Questions

- [OQ-01] What is the exact baseline vocabulary size (e.g., via a diagnostic 500-word test) of the user today?
- [OQ-02] Does the user prefer the 60 minutes in a single continuous morning/evening block or split into two 30-minute sessions (e.g., 20m AnkiDroid mobile + 40m MacBook deep practice)?
- [OQ-03] What is the user's primary medium of audio capture on the Galaxy S24 Ultra and Mac (built-in mics, wireless earbuds)?
- [OQ-04] Will Anki synchronization be handled via AnkiWeb or local file/AnkiConnect automation?

---

## 4. Deferred Decisions

- [DEF-01] **Application Stack**: Web vs Desktop vs CLI application framework (deferred to ADR-0001).
- [DEF-02] **Database & Storage**: SQLite, JSON flat-files, PostgreSQL, or Git-based markdown storage (deferred to Phase 2 ADR).
- [DEF-03] **Speech & Audio Engines**: Choice of TTS/STT providers (e.g., Gemini Multimodal Live API, ElevenLabs, OpenAI Whisper, or native Web Speech API).
- [DEF-04] **Deployment Target**: Local-only, self-hosted container, or cloud deployment.

---

## 5. Non-Goals for Current Phase

- Implementing frontend UI screens, web apps, or mobile apps.
- Building full-blown automated flashcard generation pipelines before card schema is validated.
- Creating an interactive chat application or live audio streaming service.
- Arbitrarily picking backend frameworks, databases, or cloud infrastructure.
