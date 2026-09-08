# System Architecture: English Learning OS

> **Architecture Status**: `Phase 01 — Deferred Stack Selection`

---

## 1. Architectural Philosophy

The architecture of English Learning OS is guided by five foundational tenets:

1. **Domain-Centric Design**: The business logic of language acquisition (spaced repetition intervals, CEFR level evaluations, study routine state machines, sentence mining models) must remain strictly decoupled from presentation frameworks, database engines, or cloud APIs.
2. **Local-First Reliability**: The learner must never be blocked from their daily 60-minute study session due to network latency, offline environments, or API outages. Core routines must function locally on macOS and Android.
3. **Multi-Agent Extensibility**: The system is designed to be inspected, evolved, and audited by autonomous AI agents with clear division of responsibilities.
4. **Frugality & Zero Tool Sprawl**: Do not introduce frameworks, microservices, or complex databases without a compelling, documented need approved in an ADR.
5. **Deterministic Testing**: Every architectural component must be verifiable via automated, reproducible test suites without reliance on network flakiness or timing hacks.

---

## 2. Conceptual System Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  (CLI / Web UI / Mobile Companion — Deferred to ADR-0001)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Application Services                     │
│   • Routine Coordinator (60-minute session orchestrator)    │
│   • Study Plan Dispatcher & Streak Engine                   │
│   • Export & Synchronization Managers                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     Core Domain Models                      │
│   • Learner Profile & CEFR State Machine                    │
│   • FSRS Spaced Repetition Scheduling Math                  │
│   • Sentence, Lexeme & Card Entities                        │
│   • Exercise & Feedback Evaluation Logic                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  Infrastructure & Adapters                  │
│   • Persistence Adapter (Storage Engine Deferred)           │
│   • Anki / AnkiDroid Exporter Adapter                       │
│   • Audio & Speech Synthesizer Adapter                      │
│   • AI Model Gateway (Gemini / Claude APIs)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack Evaluation Criteria (For Phase 04 ADRs)

When proposing the application runtime and storage engine in Phase 04, candidates will be evaluated against:

| Dimension | Critical Criteria |
| :--- | :--- |
| **Speed to Value** | Minimal boilerplate; quick startup for daily sessions. |
| **Cross-Device Interop** | Ease of moving cards/audio to Galaxy S24 Ultra (Android). |
| **Agent Maintainability** | High readability and clean tool support for AI agents. |
| **Longevity & Stability** | Low risk of ecosystem abandonment over multi-year horizon. |
| **Testing Simplicity** | Fast, zero-config deterministic test execution. |
