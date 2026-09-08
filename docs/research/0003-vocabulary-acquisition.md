# Research Note 0003: Vocabulary Acquisition, Lexical Frequency & Coverage

- **Date**: 2026-09-08
- **Domain**: Lexicology, Corpus Linguistics, Second Language Acquisition (SLA)
- **Primary Investigator**: Learning Science Researcher & Orchestrator
- **Epistemic Classification**: `ESTABLISHED` (Frequency Distributions & Lexical Coverage) / `STRONG EVIDENCE` (Intentional vs Incidental Learning)

---

## 1. Research Question

What quantitative principles govern the selection, sequencing, and acquisition of English vocabulary for an adult beginner in data/software, and how do intentional study (SRS) and incidental acquisition (reading/listening) interact?

---

## 2. Theoretical & Corpus Foundations

### 2.1 Lexical Units: Definitions & Distinctions
In corpus linguistics and SLA research, precise units of counting must be maintained:
- **Token**: Every individual word occurrence in a text (e.g., *"to be or not to be"* = 6 tokens).
- **Word / Inflected Form**: Specific morphological realizations (e.g., *write*, *writes*, *wrote*, *writing*, *written*).
- **Lemma**: A base headword plus its inflections within the same grammatical word class (e.g., *walk*, *walks*, *walked*, *walking* = 1 lemma; *walk* as a noun is technically a separate lemma in strict lexicography).
- **Word Family**: A base headword, its inflections, and its transparent derivational affixes (e.g., *nation*, *national*, *international*, *nationalize*, *nationalism*).
  - *SLA Caution*: Nation (2001, 2013) historically counted vocabulary by word families. However, recent empirical research (Brezina & Gablasova, 2015; Brown et al., 2020) demonstrates that **for beginner L2 learners, word family counting dangerously inflates presumed knowledge**. A beginner who knows *nation* does NOT automatically know or understand *nationalize*.
  - **English Learning OS Standard**: At levels Pre-A1 to B1, vocabulary must be measured in **lemmas and high-frequency multiword expressions (MWEs)**, not broad word families.
- **Multiword Expressions (MWEs) & Collocations**: Fixed or semi-fixed sequences of two or more words functioning as a single semantic unit (e.g., *look forward to*, *at first glance*, *take advantage of*, *pull request*).

### 2.2 Corpus Frequency Distributions (Zipf's Law & BNC/COCA)
Natural language adheres to Zipf's law: word frequency is inversely proportional to its rank in the frequency table.
- **Corpus of Contemporary American English (COCA)** (Davies, 2008–present; 1+ billion words) and the **British National Corpus (BNC)** establish the canonical frequency bands:
  - **Top 1,000 Lemmas (K1)**: Covers ~70–75% of running tokens in general fiction, television, and conversation.
  - **Top 2,000 Lemmas (K2)**: Covers ~80–85% of general spoken English running tokens.
  - **Top 3,000 Lemmas (K3)**: Covers ~88–92% of running tokens.
  - **Beyond K3**: Diminishing returns accelerate. Moving from 3,000 to 9,000 lemmas yields only an additional 5–7% text coverage.

### 2.3 Paul Nation's Lexical Coverage Thresholds
Paul Nation's seminal research (2001, 2006, 2013) establishes the cognitive thresholds of lexical coverage for text comprehension:
- **95% Lexical Coverage**: The absolute minimal threshold for minimally acceptable comprehension with scaffolding (dictionary lookup, teacher assistance, glosses). Approximately 1 unknown word in every 20 words (5 words per 100).
- **98% Lexical Coverage**: The threshold required for unassisted, pleasurable, fluent extensive reading and high-accuracy incidental guessing from context. Approximately 1 unknown word in every 50 words (2 words per 100).
- *Implication for Beginners*: Authentic native novels or technical whitepapers require a vocabulary of 8,000–9,000 word families for 98% coverage. Handing authentic, unsimplified text to an A0/A1 learner (lexical coverage < 70%) causes immediate cognitive overload and complete comprehension breakdown.

---

## 3. Intentional vs. Incidental Acquisition

A long-standing debate in SLA pits explicit study (flashcards, word lists) against implicit learning (natural reading/listening). The empirical literature provides a definitive resolution:

| Dimension | Intentional Learning (SRS / Decontextualized Retrieval) | Incidental Learning (Extensive Reading / Listening) |
| :--- | :--- | :--- |
| **Primary Strength** | Rapid initial form-meaning link establishment (Laufer, 2003). | Development of deep collocational depth, register, syntax, and polysemy (Hulstijn, 2001). |
| **Efficiency (Words/Hour)** | Very high (~10–30 new receptive associations established per hour). | Very low (~1–5 new words acquired per hour of extensive reading without glosses; Nation, 2013). |
| **Repetitions Required** | 4 to 7 spaced retrieval events (FSRS). | 10 to 20 contextual encounters across multiple texts (Webb, 2007; Waring & Takaki, 2003). |
| **Danger / Limitation** | Shallow knowledge; inability to use word fluently in spontaneous speech if unpracticed. | Inefficient for beginners; cannot encounter unknown words often enough when text coverage is too low. |

**The Complementary Synthesis**:
- Intentional learning via SRS acts as a **supercharger**: it rapidly introduces the core 1,000 to 2,000 high-frequency lemmas.
- Scaffolded comprehensible input provides the **ecological validation**: the learner repeatedly encounters these newly primed words in rich grammatical sentences, transforming shallow recognition into deep, automatic communicative competence.

---

## 4. Receptive vs. Productive Vocabulary Knowledge

Vocabulary knowledge is a multi-dimensional continuum, not a binary switch (Schmitt, 2010):
1. **Spoken Form**: Recognizing the word when heard; pronouncing it correctly.
2. **Written Form**: Recognizing the spelling; spelling it correctly.
3. **Form-Meaning Connection**: Knowing what concept the word signals.
4. **Collocations**: Knowing what words typically co-occur with it (e.g., *make a decision*, not *do a decision*).
5. **Grammatical Constraints**: Transitivity, prepositional government (e.g., *depend on*, not *depend of*).

**Receptive Vocabulary Size is Always 2x–3x Larger than Productive Vocabulary**:
An A2 learner may receptively recognize 2,000 lemmas in text, but actively produce only 600–800 lemmas in spontaneous speech. The curriculum must not attempt to force all 2,000 receptive lemmas into productive speaking cards immediately; productive vocabulary must prioritize high-utility communicative and domain-specific verbs, connectors, and nouns.

---

## 5. Domain Personalization: General English vs. Tech/Data Lexis

For a software and data professional:
1. **Core High-Frequency Layer (K1–K2)**: Mandatory non-negotiable prerequisite (e.g., *think, give, need, because, however, although, usually*). English grammar and discourse cohesion depend entirely on this layer.
2. **General Professional English (B1–B2)**: Workplace communication (e.g., *schedule, deadline, clarify, ensure, prioritize, feedback, trade-off*).
3. **Data & Software Specialized Lexis**: High familiarity in passive written form (e.g., *database, query, cluster, schema, latency, pipeline, async*), but often completely unpracticed in spoken articulatory production.
   - *Strategy*: Introduce technical vocabulary into speaking and listening drills early to leverage the learner's existing conceptual schema, but never allow technical jargon to substitute for foundational general English functional vocabulary.

---

## 6. Architectural Implications for English Learning OS

1. **Vocabulary Prioritization Algorithm**:
   $$Priority = FrequencyRank (COCA/BNC) \times CommunicativeUtility \times CEFRBand \times DomainRelevance$$
2. **Lemma-Based Progress Tracking**: Track learner vocabulary in unique lemmas and validated MWEs, strictly partitioned into:
   - `Receptive_Recognized` (receptive recall in $\le 3$ seconds)
   - `Productive_Active` (spontaneous production in speaking/writing)
3. **Input Lexical Filtering**: All reading and listening texts assigned to the learner must have their lexical profile programmatically inspected against the learner's known lemma registry, guaranteeing $\ge 95\%$ coverage (with automatic glossing of the remaining 5%).

---

## 7. Authoritative References

1. Nation, I. S. P. (2001). *Learning vocabulary in another language*. Cambridge University Press.
2. Nation, I. S. P. (2006). How large a vocabulary is needed for reading and listening?. *Canadian Modern Language Review*, 63(1), 59-82. doi:10.3138/cmlr.63.1.59
3. Davies, M. (2008). *The Corpus of Contemporary American English (COCA)*. Available online at [https://www.english-corpora.org/coca/](https://www.english-corpora.org/coca/).
4. Brezina, V., & Gablasova, D. (2015). Is there a core general vocabulary? Introducing the New General Service List. *Applied Linguistics*, 36(1), 1-22. doi:10.1073/applin/amt018
5. Laufer, B. (2003). The incidental acquisition of foreign language vocabulary through reading: Does it happen? Does it work?. *Canadian Modern Language Review*, 59(4), 567-587. doi:10.3138/cmlr.59.4.567
6. Schmitt, N. (2010). *Researching and analyzing vocabulary*. Cambridge University Press.
7. Webb, S. (2007). The effects of repetition on vocabulary knowledge. *Studies in Second Language Acquisition*, 29(1), 49-65. doi:10.1017/S0272263107070030
