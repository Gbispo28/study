# Diagnostic Scoring Guide & Profiling Engine: English Learning OS

> **Audience**: Test Administrator / Evaluator / Context Curator.
> **Core Tenet**: *Scoring must be reproducible, qualitative-evidence-based, explainable, and free of pseudo-psychometrics, fake precision, or unjustified certainty.*
> **Confidentiality Notice**: This file contains evaluation rules and bottleneck diagnostics. **NOT FOR LEARNER DISTRIBUTION.**

---

## 1. Methodological & Psychometric Foundations

### 1.1 Formative Diagnostic Profiling vs. Standardized Certification
The English Learning OS Diagnostic Battery is an **internal formative profiling instrument**, designed to identify baseline bottlenecks and calibrate dynamic study allocations in a 60-minute daily routine.
- It is **NOT** a certified or accredited Council of Europe standardized examination (such as IELTS, TOEFL, or Cambridge English).
- It does not possess large normative calibration cohorts ($N > 1,000$) or item-response-theory (IRT) parameter calibration.
- Consequently, constructing statistical "confidence intervals" (e.g., $95\% \text{ CI} = [1.32, 1.68]$) or calculating fractional CEFR decimals (e.g., "Level 2.41") is strictly unscientific and prohibited.

### 1.2 Instrument Measurement Ceiling (Pre-A1 to B2)
The custom diagnostic battery is calibrated to discriminate between **Pre-A1, A1, A2, and B2** proficiency levels.
- **Explicit Ceiling Rule**: If a learner achieves near-perfect performance across all core and extension tasks, the system must report:
  $$\text{Classification: } \mathbf{ABOVE\ CURRENT\ INSTRUMENT\ CEILING\ —\ EXTERNAL/EXTENDED\ ASSESSMENT\ REQUIRED}$$
- Under no circumstances may a C1 or C2 level be diagnosed from single isolated advanced extension items. Determining C1/C2 requires extensive multi-task sampling and certified external assessment.

### 1.3 Non-Parametric Uncertainty Modeling
Uncertainty is evaluated using transparent qualitative indicators:
- **Confidence Rating**:
  - `High`: Consistent performance across items, clear alignment with qualitative descriptors, reliable audio recordings, and low reported test fatigue/anxiety.
  - `Medium`: Borderline performance straddling descriptors, minor item inconsistency (e.g., missed an everyday item but parsed a workplace item), or moderate reported fatigue.
  - `Low`: Highly erratic response patterns, premature test termination, poor audio quality, severe reported test anxiety, or significant contradictory evidence.
- **Boundary Bands**: Explicit reporting of transitional stages (e.g., `A1-high / A2-low`, `A2-high / B1-low`).
- **Evidence Sufficiency**: Tagged as `Sufficient` (all battery parts completed) or `Partial` (one or more parts incomplete or unrecorded).

---

## 2. The 9-Dimensional State Vector $\vec{P}$

The learner's proficiency is modeled as an asynchronous multi-dimensional vector:

$$\vec{P} = \begin{bmatrix}
L & \text{(Acoustic Listening Comprehension)} \\
R & \text{(Text Reading Comprehension)} \\
SP & \text{(Spoken Monologue Production)} \\
SI & \text{(Spoken Interactive Turn-Taking)} \\
W & \text{(Written Composition & Synthesis)} \\
PC & \text{(Phonological Control & Intelligibility)} \\
GC & \text{(Operational Grammatical Competence)} \\
VR & \text{(Receptive Lexical Band Familiarity)} \\
VP & \text{(Productive Lexical Recall)}
\end{bmatrix}$$

Each dimension is assigned a qualitative CEFR descriptor band from [CEFR_RUBRIC.md](../CEFR_RUBRIC.md) (Pre-A1 through B2, or `> B2 Ceiling`), accompanied by a Confidence Rating.

---

## 3. Dimension-Specific Evaluation & Scoring Guidelines

### 3.1 Listening Comprehension ($L$)
- **Core Tasks**:
  - Task A1 (3 items): General conversation reduction (Clip 1), workplace schedule (Clip 2), technical context probe (Clip 3).
  - Task A2 (4 items): Bottom-up micro-dictation of connected speech sentences.
- **Optional Extension**: Task A3 (Fast spoken technical discourse).
- **Domain Contamination Safeguard**:
  - If the learner parses Clip 3 and Task A3 (technical schema) but fails Clip 1 and Task A2 (everyday reductions like *gonna get a cup of water* and *what did you do yesterday*), the learner MUST NOT be classified above A2 in general listening. Their listening bottleneck is bottom-up acoustic decoding of natural connected speech.
- **Heuristic Routing Guidelines** *(Unvalidated preliminary routing only; cross-reference with CEFR descriptors)*:
  - 0–2 items correct in core tasks $\rightarrow$ `Pre-A1` (Severe acoustic segmentation barrier).
  - 3–4 items correct in core tasks $\rightarrow$ `A1` (Recognizes isolated content words; misses functional words and connected reductions).
  - 5–6 items correct in core tasks $\rightarrow$ `A2` (Parses standard speech; emerging tolerance of connected reductions).
  - 7 items correct in core tasks + partial extension $\rightarrow$ `B1` to `B2` (Robust bottom-up parsing of connected speech).
  - Complete mastery of core + advanced extension $\rightarrow$ `B2` (Flag as approaching or exceeding instrument ceiling).

### 3.2 Reading Comprehension ($R$)
- **Core Task B1**: Workplace narrative passage (3 items: detail recall, meaning in context, chronological reasoning).
- **Optional Extension Task B2**: Distributed systems reasoning passage.
- **Domain Contamination Safeguard**: Technical vocabulary and software conceptual familiarity can inflate reading scores. If performance on Task B1 is strong but general functional grammar (Part F) is weak, the reading score reflects domain schema support.
- **Heuristic Routing Guidelines**:
  - 0–1 items on Task B1 $\rightarrow$ `Pre-A1 / A1`
  - 2 items on Task B1 $\rightarrow$ `A1-high / A2-low`
  - 3 items on Task B1 $\rightarrow$ `A2 / B1`
  - 3 items on Task B1 + correct comprehension on Task B2 $\rightarrow$ `B2` (Approaching instrument ceiling; do not diagnose C1/C2).

### 3.3 Spoken Production ($SP$) & Interaction ($SI$)
Evaluated from recordings `spoken_c1` (monologue) and `spoken_c2` (workplace scenario) against [CEFR_RUBRIC.md](../CEFR_RUBRIC.md):
1. **Intelligibility & Articulatory Clarity** (Does accent impede comprehension?)
2. **Grammatical Complexity & Accuracy** (Simple isolated SVO phrases vs. coordinated clauses)
3. **Lexical Precision** (Reliance on basic gestures/words vs. accurate workplace terms)
4. **Fluency & Retrieval Latency** (Long pauses $>5$s vs. continuous delivery)
- **Descriptor Mapping**:
  - `Pre-A1`: Single-word fragments, retrieval pauses $>5$s, no connected syntax.
  - `A1`: 1–2 simple memorized phrases, heavy hesitation.
  - `A2`: 3–5 linked sentences, pauses for grammatical planning, message understandable.
  - `B1`: Spontaneous narrative, handles routine standup scenario with comprehensible fluency.
  - `B2`: High fluency, coherent technical explanation, rare communicative breakdown.

### 3.4 Phonological Control ($PC$)
- **Task D1 (Perception)**: Minimal pair discrimination (5 items).
- **Task D2 (Production Read-Aloud)**: Evaluates candidate interference features:
  1. *Epenthesis*: High-front vowel [i] added after final consonant stops (*stop-i*, *laptop-i*, *big-ui*).
  2. *Vowel Contrasts*: /i/ vs /ɪ/ (*live/eat*); /æ/ vs /ɛ/ (*bad/bed*).
  3. *Word Stress & Reduction*: Preservation of tonic syllables (*development*, *database*); schwa reduction.
  4. *Nasal Closure*: Oral closure on coda nasals (*come*, *plan*, *afternoon*).
- **Regional Dialect Awareness**: Check intake dialect background. If the learner does not show affrication or retroflex transfer, do not diagnose problems that do not exist.

### 3.5 Written Composition ($W$) & Operational Grammar ($GC$)
- **Task E1 (Sentence Combining)**: Evaluates ability to synthesize clauses using connectors (*because, after, although*).
- **Task E2 (Workplace Message)**: Evaluates functional written composition across 3 criteria (task status, problem description, meeting request).
- **Part F (Grammar in Use)**: Verb aspect (*is debugging / writes*), past simple (*found / brought*), modals (*cannot*), prepositions (*at / on*).

### 3.6 Receptive Lexical Band Familiarity ($VR$) — NO FAKE EXTRAPOLATION
- **Part G**: 9 items sampled across K1 (top 1,000), K2 (1,001–2,000), and K3 (2,001–3,000).
- **Prohibition**: DO NOT multiply correct items by 1,000 to compute a "vocabulary size" (e.g., "1,600 lemmas"). 9 items cannot support a continuous numeric estimate.
- **Reporting Standard**:
  - *K1 Familiarity*: High (3/3) | Moderate (2/3) | Emergent (0–1/3)
  - *K2 Familiarity*: High (3/3) | Moderate (2/3) | Emergent (0–1/3)
  - *K3 Familiarity*: High (3/3) | Moderate (2/3) | Emergent (0–1/3)
  - *Overall Lexical Profile*: Tagged qualitatively as `Foundational (K1-focused)`, `Expanding (K2-emergent)`, or `Intermediate (K3-emergent)`. Quantitative size estimation is deferred to longitudinal tracking.

---

## 4. Multi-Factor Bottleneck Evaluation Engine

Rather than an arbitrary fixed hierarchy where phonology always outranks listening or vocabulary, the system evaluates bottlenecks dynamically based on **five clinical criteria**:

1. **Severity of Communicative Breakdown**: Does the issue cause a complete communicative failure?
2. **Frequency in Target Communication**: How often does this feature occur in daily professional and general English?
3. **Learner-Specific Goals & Priorities**: What immediate communication tasks does the learner need to perform?
4. **Remediation Leverage**: Does resolving this issue unlock rapid progress in other dimensions? (e.g., bottom-up acoustic decoding unlocks listening comprehension; K1 vocabulary unlocks sentence construction).
5. **Measurement Confidence**: Is the diagnostic evidence for this weakness strong and consistent?

```python
def evaluate_primary_bottleneck(profile):
    """
    Evaluates primary bottleneck based on empirical evidence,
    avoiding rigid predetermined hierarchies.
    """
    evidence = []

    # 1. Phonological Intelligibility Check
    if profile["PC"]["epenthesis_severe"] and profile["PC"]["intelligibility_threat"]:
        evidence.append({
            "type": "BOTTLENECK_PHONOLOGICAL_EPENTHESIS",
            "leverage": "High (intelligibility barrier blocks spoken interaction)",
            "priority_weight": 85
        })

    # 2. Acoustic Listening vs Reading Gap (Decoding Barrier)
    if profile["L"]["band"] in ["Pre-A1", "A1"] and profile["R"]["band"] >= "A2":
        evidence.append({
            "type": "BOTTLENECK_ACOUSTIC_DECODING",
            "leverage": "High (reading knowledge not recognized in speech due to connected speech)",
            "priority_weight": 90
        })

    # 3. Foundational Lexicon Deficit
    if profile["VR"]["K1"] in ["Emergent", "Moderate"]:
        evidence.append({
            "type": "BOTTLENECK_FOUNDATIONAL_LEXICON_K1",
            "leverage": "Maximum (without K1 lemmas, syntax and decoding cannot function)",
            "priority_weight": 95
        })

    # 4. Spoken Retrieval Latency / Production Block
    if profile["SP"]["band"] == "Pre-A1" and profile["R"]["band"] >= "A2":
        evidence.append({
            "type": "BOTTLENECK_SPOKEN_RETRIEVAL_LATENCY",
            "leverage": "Moderate-High (asymmetry between receptive and productive competence)",
            "priority_weight": 80
        })

    if not evidence:
        return {"primary": "BALANCED_PROGRESSION", "rationale": "No single catastrophic bottleneck detected."}

    # Sort dynamically by priority weight and empirical evidence quality
    evidence.sort(key=lambda x: x["priority_weight"], reverse=True)
    return evidence[0]
```

---

## 5. Standardized Diagnostic Profile Card Output

Every diagnostic administration outputs a structured profile card:

```markdown
### Baseline Diagnostic Assessment Profile
- **Learner**: [Name]
- **Date**: YYYY-MM-DD
- **Instrument**: English Learning OS Diagnostic Battery (Form A)
- **Status**: Formative Diagnostic Profile (Not an accredited CEFR certification)
- **Instrument Measurement Ceiling**: Pre-A1 to B2

| Dimension | Diagnostic Band | Boundary State | Confidence | Evidence Quality & Clinical Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Acoustic Listening** | A1 | A1-high / A2-low | Medium | Struggles with connected speech reductions; workplace topic recognized. |
| **Text Reading** | A2 | Solid A2 | High | Successfully parsed workplace narrative; technical schema evident. |
| **Spoken Production** | Pre-A1 | Solid Pre-A1 | High | Heavy retrieval latency (>5s); single-word responses. |
| **Phonological Control**| Pre-A1 | Pre-A1 / A1-low | High | Stop epenthesis marked; /i/-/ɪ/ vowel contrast collapsed. |
| **Written Composition**| A1 | A1-high | Medium | Sentence combining successful with basic coordinators; needs modal practice. |
| **Operational Grammar**| A1 | A1 | High | Present continuous in use; past irregular verbs missing. |
| **Receptive Lexis (K1–K3)**| Foundational | K1: High, K2: Mod, K3: Emergent | High | Core everyday lemmas solid; professional vocabulary expanding. |

- **Identified Primary Bottleneck**: `BOTTLENECK_ACOUSTIC_DECODING`
- **Clinical Rationale**: Learner has passive lexical knowledge in text, but fails to segment words in conversational audio due to connected speech reductions.
- **Dynamic 60-Minute Routine Prescription**:
  - Block 1 (15m): FSRS Anki review (K1/K2 core lemmas + minimal pairs).
  - Block 2 (30m): Bimodal reading-while-listening + acoustic micro-dictation drills.
  - Block 3 (15m): Scaffolded AI dialogue with Gemini Live focusing on basic SVO production and epenthesis suppression.
```
