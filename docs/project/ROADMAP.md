# Project Roadmap: English Learning OS

> **Governance Principle**: Phases represent logical gates, not arbitrary calendar dates. A phase is unlocked only when the preceding phase meets its Definition of Done.

```
Phase 01: Foundation & Governance (COMPLETE — Gate 1 Passed)
   ↓
Phase 02: Product Discovery & SLA Specification (IN PROGRESS — Gate 2: Blocked on Learner Baseline)
   ↓
Phase 03: Daily Journey & Card Architecture (LOCKED — Pending Learner Baseline)
   ↓
Phase 04: Architecture & Stack Decision (ADRs)
   ↓
Phase 05: Core MVP Implementation
   ↓
Phase 06: Measurement & Progress Analytics
   ↓
Phase 07: Adaptive Learning Engine
   ↓
Phase 08: Multi-Device Automation & Hardening
```

---

## Phase 01: Foundation & Governance (Status: COMPLETE | Gate 1: PASSED)
- [x] Canonical governance contract ([AGENTS.md](../../AGENTS.md)) and Claude pairing guide ([CLAUDE.md](../../CLAUDE.md)).
- [x] Workspace rules configured with native Antigravity frontmatter.
- [x] Custom agent hierarchy (Orchestrator + 8 Specialists).
- [x] Standardized skills for planning, research, implementation, verification, and Git delivery.
- [x] Zero-dependency repository validator and automated quality gate.
- [x] Living documentation and handoff infrastructure.
- [x] Foundation hardening, Git hygiene gate, and Gate 1 closure.

---

## Phase 02: Product Discovery & SLA Specification (Status: IN PROGRESS | Gate 2: BLOCKED ON LEARNER BASELINE)
- [x] Standardized 7-part diagnostic test battery and scoring model ([docs/assessment/](../assessment/README.md)).
- [x] Master evidence matrix with 16 graded candidate claims and 4 hypothesis audits ([docs/research/EVIDENCE_MATRIX.md](../research/EVIDENCE_MATRIX.md)).
- [x] 10 peer-reviewed research notes covering SLA, memory, vocabulary, input, output, phonetics, grammar, and 2026 tools ([docs/research/](../research/README.md)).
- [x] Candidate contrastive phonological priority matrix: Brazilian Portuguese to General American English.
- [x] Operational 60-minute routine allocation policy (3-block modular architecture + priority engine).
- [x] Native Anki FSRS configuration and card taxonomy (4 note types).
- [x] Canonical pedagogical invariants ([LEARNING_PRINCIPLES.md](../product/LEARNING_PRINCIPLES.md)).
- [x] Master system specification ([LEARNING_SYSTEM_SPEC.md](../product/LEARNING_SYSTEM_SPEC.md)).
- [ ] **Gating Dependency**: Ingest completed learner baseline intake and diagnostic performance to compute vector $\vec{P}$ and close Gate 2.

---

## Phase 03: Daily Journey & Card Architecture (Status: LOCKED — Pending Learner Baseline)
- [ ] Unlocked only upon formal closure of Gate 2 with real learner baseline data.
- [ ] Detailed daily protocol and device transitions (Galaxy S24 Ultra morning $\rightarrow$ MacBook Air evening).
- [ ] Implementation of Anki note type templates (fields, CSS, mobile touch targets, cloze styling).
- [ ] FSRS configuration profile setup in Anki Desktop.
- [ ] Initial seed batch of 100 core foundational cards (K1 Band + BP phonetics).

---

## Phase 04: Architecture & Technology Stack Decision (Status: Planned)
- [ ] Formal ADR: Application delivery interface (CLI, Web, Local App).
- [ ] Formal ADR: Programming language and framework selection.
- [ ] Formal ADR: Persistence layer (SQLite, Flat Files, or Embedded DB).
- [ ] Formal ADR: AI API integration and TTS/STT provider strategy.

---

## Phase 05: Core MVP Implementation (Status: Planned)
- [ ] Implementation of study session engine adhering to Phase 04 ADRs.
- [ ] Automated sentence mining pipeline and card export format.
- [ ] Basic pronunciation drill validator.
- [ ] 100% deterministic test coverage of domain logic.

---

## Phase 06: Measurement & Progress Analytics (Status: Planned)
- [ ] Vocabulary accumulation metrics (lemma count, frequency bands).
- [ ] Consistency tracking and streak protection mechanisms.
- [ ] CEFR milestone progression indicators.

---

## Phase 07: Adaptive Learning Engine (Status: Planned)
- [ ] Dynamic difficulty adjustment based on error patterns.
- [ ] Automated identification of leeches and confusing grammar structures.
- [ ] AI conversation partner specialized in targeted role-playing.

---

## Phase 08: Multi-Device Automation & Hardening (Status: Planned)
- [ ] Mobile sync automation between MacBook and Galaxy S24 Ultra.
- [ ] Security audit, backup automation, and disaster recovery.
- [ ] Performance optimization and latency tuning.
