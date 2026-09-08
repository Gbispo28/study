# Deterministic Scoring Model: English Learning OS

> **Core Tenet**: *Scoring must be reproducible, explainable, and free of hidden AI "gut feelings". Uncertainty must be modeled explicitly.*

---

## 1. Mathematical Architecture: The Multi-Dimensional Profile Vector

The learner's proficiency is modeled as a 9-dimensional state vector $\vec{P}$:

$$\vec{P} = \begin{bmatrix}
L & \text{(Acoustic Listening Comprehension)} \\
R & \text{(Text Reading Comprehension)} \\
SP & \text{(Spoken Monologue Production)} \\
SI & \text{(Spoken Interactive Turn-Taking)} \\
W & \text{(Written Composition & Synthesis)} \\
PC & \text{(Phonological Control & Intelligibility)} \\
GC & \text{(Operational Grammatical Competence)} \\
VR & \text{(Receptive Vocabulary Breadth - Lemmas)} \\
VP & \text{(Productive Vocabulary Recall - Lemmas)}
\end{bmatrix}$$

Each dimension $d \in \vec{P}$ is assigned:
1. **CEFR Band**: One of `Pre-A1`, `A1`, `A1+`, `A2`, `A2+`, `B1`, `B1+`, `B2`.
2. **Confidence Level**: `High` ($\ge 85\%$ consistency across items), `Medium` (borderline performance or minor item variance), or `Low` (insufficient evidence or erratic responses).
3. **Primary Cognitive Bottleneck Flag**: Boolean flag identifying the specific dimension that is currently constraining overall communicative competence.

---

## 2. Objective Task Scoring Models

### 2.1 Receptive Scoring: Listening & Reading

#### Part A: Listening Comprehension
- **Task A1 (Speed & Reduction Discrimination)**: 3 items, 1.0 point each.
- **Task A2 (Micro-Dictation / Bottom-Up Segmentation)**: 4 items, 1.0 point each (scored on lexical and functional word accuracy; minor phonetic spelling slips penalized by 0.25).
- **Total Listening Raw Score ($S_L$)**: Range $[0.0, 7.0]$.

| Raw Score ($S_L$) | CEFR Classification | Diagnostic Interpretation |
| :---: | :---: | :--- |
| $0.0 \le S_L < 2.0$ | `Pre-A1` | Severe acoustic segmentation barrier; cannot parse connected speech. |
| $2.0 \le S_L < 3.5$ | `A1` | Recognizes isolated content words; misses functional words and reductions. |
| $3.5 \le S_L < 4.5$ | `A1+ / A2-low` | Borderline; grasps main ideas if speech is slow, but misses connected speech. |
| $4.5 \le S_L < 5.5$ | `A2` | Parses standard clear speech; tolerates moderate speech rates. |
| $5.5 \le S_L \le 7.0$ | `B1` | Robust bottom-up parsing; handles standard connected speech and technical discourse. |

#### Part B: Reading Comprehension
- **Task B1 (Syntax & Inferencing)**: 3 items, 1.0 point each.
- **Total Reading Raw Score ($S_R$)**: Range $[0.0, 3.0]$.

| Raw Score ($S_R$) | CEFR Classification | Diagnostic Interpretation |
| :---: | :---: | :--- |
| $0.0 \le S_R < 1.0$ | `Pre-A1` | Reads isolated words only; unable to parse 2-sentence narrative. |
| $1.0 \le S_R < 2.0$ | `A1` | Understands simple isolated clauses; struggles with causal connectors (*instead of*). |
| $2.0 \le S_R < 2.75$ | `A2` | Comprehends clear sequential workplace narratives and chronological flow. |
| $2.75 \le S_R \le 3.0$ | `B1` | Full syntactic comprehension and inferencing on workplace texts. |

---

### 2.2 Productive Scoring: Speaking & Pronunciation

#### Part C: Spoken Production & Interaction
Scored deterministically across four 5-point rubric criteria from [CEFR_RUBRIC.md](./CEFR_RUBRIC.md):
1. **Intelligibility & Phonological Clarity** $[1 - 5]$
2. **Grammatical Accuracy & Sentence Structure** $[1 - 5]$
3. **Lexical Range & Appropriateness** $[1 - 5]$
4. **Fluency & Retrieval Latency** $[1 - 5]$

$$\text{Composite Spoken Score } S_{SP} = \frac{\sum \text{Criteria}}{4} \quad (\text{Range } [1.0, 5.0])$$

| Composite $S_{SP}$ | CEFR Classification | Behavioral Thresholds |
| :---: | :---: | :--- |
| $1.0 \le S_{SP} < 1.8$ | `Pre-A1` | Single-word utterances; retrieval pauses $>5$ seconds; no connected syntax. |
| $1.8 \le S_{SP} < 2.6$ | `A1` | Simple memorized SVO frames; frequent long pauses for retrieval. |
| $2.6 \le S_{SP} < 3.4$ | `A2` | 3–5 connected sentences; pauses for grammatical planning; intelligible message. |
| $3.4 \le S_{SP} < 4.2$ | `B1` | Continuous narrative; spontaneous repair; handles routine workplace scenarios. |
| $4.2 \le S_{SP} \le 5.0$ | `B2` | High fluency; nuanced technical explanation; rare intrusive hesitation. |

#### Part D: Pronunciation & Articulatory Mechanics
- **Task D1 (Perception Minimal Pairs)**: 5 items, 1.0 point each ($[0, 5]$).
- **Task D2 (Production - Epenthesis, Stress, Nasals)**: 4 target sentences evaluated for BP interference:
  - Epenthesis on word-final stops: $0.0$ (pervasive), $1.0$ (occasional), $2.0$ (completely suppressed).
  - Word stress accuracy: $0.0$ (misplaced tonic stress), $1.0$ (correct stress).
  - Vowel contrast (/i/ vs /ɪ/): $0.0$ (merged), $1.0$ (distinct).
  - Nasal coda closure (/m, n/): $0.0$ (nasalized vowel only), $1.0$ (complete physical closure).
- **Total Pronunciation Raw Score ($S_{PC}$)**: $[0.0, 10.0]$.

---

### 2.3 Written Composition & Grammar Scoring

#### Part E: Written Composition & Sentence Combining
- **Task E1 (Sentence Combining)**: 3 items, 1.0 point each ($[0, 3]$). Evaluated on connector placement (*because, after, but/although*) and punctuation.
- **Task E2 (Functional Workplace Message)**: Scored on Task Completion ($1.0$), Cohesion ($1.0$), and Grammatical Control ($1.0$) ($[0, 3]$).
- **Total Writing Raw Score ($S_W$)**: Range $[0.0, 6.0]$.

#### Part F: Operational Grammar in Use
- 4 items testing verb aspect, irregular past, modal verbs, and prepositions ($[0.0, 4.0]$).

---

### 2.4 Lexical Size Estimation (Nation's VLT Format)

Part G samples from the K1, K2, and K3 frequency bands (3 items per band = 9 items total):

$$\text{Estimated Receptive Vocabulary Size } V_{\text{est}} = \sum_{k=1}^{3} \left( \frac{\text{Correct Items}_k}{3} \times 1,000 \right)$$

- If $V_{\text{est}} < 800$ lemmas $\implies$ `Pre-A1 Lexicon`.
- If $800 \le V_{\text{est}} < 1,500$ lemmas $\implies$ `A1 Lexicon`.
- If $1,500 \le V_{\text{est}} < 2,500$ lemmas $\implies$ `A2 Lexicon`.
- If $V_{\text{est}} \ge 2,500$ lemmas $\implies$ `B1 Lexicon`.

---

## 3. Bottleneck Identification Algorithm

To determine what the 60-minute routine allocation engine should prioritize, the scoring model applies the **Weakest Link Theorem**:

```python
def identify_bottleneck(profile_vector):
    # Order of communicative dependency:
    # 1. Phonological Intelligibility (if speech is unintelligible, grammar cannot save it)
    # 2. Acoustic Listening (if input cannot be parsed, interaction is impossible)
    # 3. Core Vocabulary (without K1 lemmas, syntax has no building blocks)
    # 4. Spoken Production / Fluency
    # 5. Grammar & Writing

    if profile_vector["PC"] <= "A1" and profile_vector["epenthesis_severe"]:
        return "BOTTLENECK_PHONOLOGICAL_EPENTHESIS"
    elif profile_vector["VR"] < 1000:
        return "BOTTLENECK_CORE_LEXICON_K1"
    elif profile_vector["L"] < profile_vector["R"]:
        return "BOTTLENECK_ACOUSTIC_DECODING"
    elif profile_vector["SP"] <= "Pre-A1":
        return "BOTTLENECK_SPOKEN_RETRIEVAL_LATENCY"
    else:
        return "BALANCED_PROGRESSION"
```

---

## 4. Transparency & Explainability Output Format

Every scoring evaluation must output a structured, auditable JSON and Markdown diagnostic card:

```markdown
### Baseline Diagnostic Report
- **Learner**: G. Bispo (Primary User)
- **Date**: YYYY-MM-DD
- **Evaluator**: English Learning OS Assessment Engine

| Dimension | Raw Score | CEFR Band | Confidence | Diagnostic Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Acoustic Listening** | 3.0 / 7.0 | A1 | High | Connected speech causes breakdown; misses flapping and reductions. |
| **Text Reading** | 2.5 / 3.0 | A2 | High | Strong technical parsing; grasps narrative sequence. |
| **Spoken Production** | 1.5 / 5.0 | Pre-A1 | High | High retrieval latency (>6s); single-word responses. |
| **Pronunciation** | 4.0 / 10.0 | Pre-A1 | High | Pervasive final epenthesis on stops; vowel contrast /i/-/ɪ/ collapsed. |
| **Written Composition**| 3.5 / 6.0 | A1+ | Medium | Understands basic connectors; needs irregular verb consolidation. |
| **Receptive Vocabulary**| 1,600 lemmas| A2 | High | Good K1 mastery; partial K2 knowledge; tech words recognized. |

- **Primary Cognitive Bottleneck**: `BOTTLENECK_PHONOLOGICAL_EPENTHESIS` + `ACOUSTIC_LISTENING`
- **Immediate Prescription**: Focus Block 2 on bimodal reading-while-listening; focus Block 3 on stop epenthesis suppression drills.
```
