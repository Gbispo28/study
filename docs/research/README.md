# Learning Science & Cognitive Research Repository

This directory contains empirical research notes, literature reviews, and cognitive science analyses supporting pedagogical decisions in the **English Learning OS**.

---

## 1. Master Evidence Matrix

The central empirical registry for all architectural decisions is located in:
- [EVIDENCE_MATRIX.md](./EVIDENCE_MATRIX.md): Comprehensive 8-tier epistemic grading of all pedagogical claims, empirical sources, conflicting evidence, practical implications, and audited product hypotheses.

---

## 2. Scientific Evidence Grading Standard

Every research document stored here grades its conclusions against the project's canonical 8-tier epistemic hierarchy:

| Level | Evidence Category | Definition & Criteria |
| :--- | :--- | :--- |
| **Level 1: ESTABLISHED** | Meta-Analyses & Systematic Reviews | Multiple randomized controlled trials or large-scale cohort studies published in peer-reviewed cognitive/SLA journals with robust replication. |
| **Level 2: STRONG EVIDENCE** | Primary Empirical Studies | Controlled trials, longitudinal case studies, or published laboratory experiments with clear methodology and consistent findings. |
| **Level 3: MODERATE EVIDENCE** | Well-Designed Primary Studies | Controlled investigations with moderate sample sizes or specific boundary conditions. |
| **Level 4: LIMITED EVIDENCE** | Preliminary Laboratory Findings | Small-scale exploratory trials, laboratory data, or pilot studies requiring further replication. |
| **Level 5: EXPERT CONSENSUS** | Authoritative Frameworks | Institutional standards and frameworks from official bodies (e.g., Council of Europe CEFR, Cambridge English). |
| **Level 6: PLAUSIBLE / HYPOTHESIS** | Theoretical Models | Conceptually sound pedagogical models or working hypotheses awaiting empirical validation. |
| **Level 7: UNSUPPORTED** | Disproven Myths / Unsubstantiated | Popular language learning claims lacking empirical support or contradicted by modern cognitive science. |
| **Level 8: CONFLICTING EVIDENCE** | Divergent Literature | Findings with contradictory results under different experimental or pedagogical conditions. |

---

## 3. Phase 02 Research Notes

The following peer-reviewed research syntheses govern the system's pedagogical specification:

| Note ID | Research Topic | Primary Scientific Focus | Canonical References |
| :--- | :--- | :--- | :--- |
| [0001](./0001-assessment-cefr.md) | **Assessment & CEFR Framework Alignment** | CEFR Companion Volume (2020), English Profile (EVP/EGP), Multi-dimensional diagnostic vectors. | Council of Europe (2020), Alderson (2005), North (2014) |
| [0002](./0002-memory-retrieval-spacing.md) | **Memory Architecture & Retrieval Practice** | Testing effect, distributed spacing, interleaving, desirable difficulties, cognitive load theory. | Roediger & Karpicke (2006), Cepeda et al. (2006, 2008), Sweller (2011) |
| [0003](./0003-vocabulary-acquisition.md) | **Vocabulary Acquisition & Lexical Coverage** | COCA/BNC frequency bands, lemmas vs word families, Nation's 95%/98% coverage, intentional vs incidental. | Nation (2001, 2006), Davies (2008), Laufer (2003), Schmitt (2010) |
| [0004](./0004-listening-reading-input.md) | **Receptive Skills: Listening & Reading Input** | Comprehensible input ($i+1$), bottom-up acoustic decoding, connected speech, bimodal reading-while-listening. | Field (2008), Vandergrift & Goh (2012), Chang (2011), VanPatten (2004) |
| [0005](./0005-speaking-feedback.md) | **Spoken Production & Corrective Feedback** | Pushed output hypothesis, CAF triad, AI conversational safety, explicit correction vs recasts. | Swain (1995), Skehan (1998), Lyster & Saito (2010), Kim et al. (2019) |
| [0006](./0006-pronunciation-brazilian-portuguese.md) | **Contrastive Phonetics: BP to General American** | Intelligibility principle, epenthesis suppression, vowel collapses (/i/-/ɪ/, /æ/-/ɛ/), stress priority matrix. | Derwing & Munro (2015), Levis (2018), Major (2001), Celce-Murcia (2010) |
| [0007](./0007-writing-grammar.md) | **Written Production & Grammar Acquisition** | Focus on Form (FonF), English Grammar Profile, sentence combining, AI feedback guardrails. | Long (1991), Norris & Ortega (2000), Saddler & Graham (2005), Ferris (2011) |
| [0008](./0008-anki-fsrs.md) | **Anki & Modern FSRS Scheduling Architecture** | FSRS mathematics, Desired Retention workload curve (80% vs 85% vs 90%), leech policies, card taxonomy. | Ye (2023), Anki Official Docs (2024), Settles & Meeder (2016), Wozniak (1995) |
| [0009](./0009-ai-tools-and-free-resources.md) | **Tool Ecosystem & Curated Resource Audit** | Google AI Pro (Gemini Live), Claude Code Pro, MacBook M4, S24 Ultra, curated zero-cost linguistic tools. | Official Tech Reports (Google DeepMind, Anthropic), Cambridge Learner Corpus |
| [0010](./0010-sixty-minute-allocation-model.md) | **60-Minute Daily Allocation & Cognitive Budget** | Modular 3-block session, dynamic routine allocation engine, workload throttling, core vs ambient exposure. | Ericsson (2006), Sweller (2011), Newport (2016) |

---

## 4. Research Note Template

When authoring future study notes, adhere strictly to this template:

```markdown
# [Research Topic Title]

- **Date**: YYYY-MM-DD
- **Domain**: [SLA / Phonetics / Cognitive Psychology / etc.]
- **Primary Investigator**: [Agent Name]
- **Epistemic Classification**: [ESTABLISHED | STRONG EVIDENCE | MODERATE EVIDENCE | etc.]

## 1. Research Question
What specific pedagogical or cognitive question was investigated?

## 2. Methodology & Key Sources
List citations, DOIs, sample sizes, and study parameters.

## 3. Core Findings
Synthesize findings with quantitative metrics where available.

## 4. Conflicting Evidence & Boundary Conditions
Where does this theory break down or show diminished returns?

## 5. Architectural Implications for English Learning OS
Concrete takeaways for study planning, card scheduling, or session structure.

## 6. Authoritative References
Numbered list with complete academic citations and DOIs.
```
