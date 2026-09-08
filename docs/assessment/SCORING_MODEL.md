# Deterministic Scoring Model: English Learning OS

> **Core Tenet**: *Scoring must be reproducible, explainable, and free of hidden AI "gut feelings". False psychometrics (e.g., fictitious statistical confidence intervals) are strictly prohibited.*

---

## 1. Mathematical & Architectural Philosophy

### 1.1 Rejection of False Psychometrics
In educational testing, constructing statistical "confidence intervals" (e.g., $95\% \text{ CI} = [1.32, 1.68]$) requires:
1. Large normative calibration cohorts ($N > 1,000$).
2. Validated Item Response Theory (IRT) difficulty and discrimination parameters ($\alpha, \beta, \gamma$).
3. Standardized item reliability coefficients (Cronbach's $\alpha$).

Because the English Learning OS uses custom diagnostic items rather than a million-student standardized exam, **generating fake statistical confidence intervals is unscientific**.

### 1.2 Non-Parametric Uncertainty Modeling
Instead of pseudo-statistical intervals, the system models uncertainty using transparent, explainable categories:
- **Confidence Rating**:
  - `High`: Performance is consistent across all items in the battery; no contradictory signals.
  - `Medium`: Minor variance between items (e.g., passed complex item, missed simpler item) or borderline threshold performance.
  - `Low`: Extreme item variance, severe test anxiety indicated in intake, or premature early stopping due to fatigue.
- **Boundary Bands**: Explicit reporting of transition states (e.g., `A2-high / B1-low` instead of a fake decimal score like `CEFR = 2.73`).
- **Evidence Sufficiency**: Tagged as `Sufficient` (all battery parts completed) or `Partial` (routing stopped early).

---

## 2. The 9-Dimensional State Vector $\vec{P}$

The learner's proficiency is modeled as a vector spanning **Pre-A1 to C2**:

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

---

## 3. Objective Task Scoring Rules

### 3.1 Receptive Scoring: Listening & Reading

#### Part A: Listening Comprehension
- Task A1 (Discrimination): 3 items, 1.0 pt each.
- Task A2 (Micro-Dictation): 4 items, 1.0 pt each.
- Task A3 (Optional C1/C2 Extension): 2.0 pts.
- Raw Score ($S_L$): Range $[0.0, 9.0]$.

| Raw Score ($S_L$) | Diagnostic Classification | Uncertainty & Diagnostic Notes |
| :---: | :---: | :--- |
| $0.0 \le S_L < 2.0$ | `Pre-A1` | Severe acoustic segmentation barrier; cannot parse connected speech. |
| $2.0 \le S_L < 3.5$ | `A1` | Recognizes isolated content words; misses functional words and reductions. |
| $3.5 \le S_L < 4.5$ | `A2-low` (Boundary: `A1-high / A2-low`) | Borderline; grasps slow speech, but misses natural connected speech. |
| $4.5 \le S_L < 5.5$ | `A2` | Parses standard clear speech; tolerates moderate speech rates. |
| $5.5 \le S_L < 7.0$ | `B1` | Robust bottom-up parsing; handles standard connected speech. |
| $7.0 \le S_L < 8.0$ | `B2` | Parses fast technical discourse with native reductions. |
| $8.0 \le S_L \le 9.0$ | `C1 / C2` | Parses complex, fast, idiomatic multi-speaker discourse effortlessly. |

#### Part B: Reading Comprehension
- Task B1 (Core Passage): 3 items, 1.0 pt each.
- Task B2 (Optional C1/C2 Extension): 2.0 pts.
- Raw Score ($S_R$): Range $[0.0, 5.0]$.

| Raw Score ($S_R$) | Diagnostic Classification | Uncertainty & Diagnostic Notes |
| :---: | :---: | :--- |
| $0.0 \le S_R < 1.0$ | `Pre-A1` | Reads isolated words only; unable to parse 2-sentence narrative. |
| $1.0 \le S_R < 2.0$ | `A1` | Understands simple isolated clauses; struggles with complex connectors. |
| $2.0 \le S_R < 2.75$ | `A2` | Comprehends clear sequential workplace narratives. |
| $2.75 \le S_R \le 3.0$ | `B1` | Full syntactic comprehension of standard workplace text. |
| $3.0 < S_R < 4.0$ | `B2` | Rapidly skims technical documentation without dictionary assistance. |
| $4.0 \le S_R \le 5.0$ | `C1 / C2` | Parses dense technical and architectural prose effortlessly. |

---

### 3.2 Productive Scoring: Speaking & Pronunciation

#### Part C: Spoken Production & Interaction
Evaluated on four 5-point criteria from [CEFR_RUBRIC.md](./CEFR_RUBRIC.md):
1. Intelligibility & Phonological Clarity $[1 - 5]$
2. Grammatical Accuracy & Complexity $[1 - 5]$
3. Lexical Range & Precision $[1 - 5]$
4. Fluency & Retrieval Latency $[1 - 5]$

$$\text{Composite Spoken Score } S_{SP} = \frac{\sum \text{Criteria}}{4} \quad (\text{Range } [1.0, 5.0])$$

| Composite $S_{SP}$ | Diagnostic Band | Behavioral Criteria |
| :---: | :---: | :--- |
| $1.0 \le S_{SP} < 1.8$ | `Pre-A1` | Single-word utterances; retrieval pauses $>5$ seconds; no connected syntax. |
| $1.8 \le S_{SP} < 2.6$ | `A1` | Simple memorized SVO frames; frequent long pauses for retrieval. |
| $2.6 \le S_{SP} < 3.4$ | `A2` | 3–5 connected sentences; pauses for grammatical planning; intelligible message. |
| $3.4 \le S_{SP} < 4.2$ | `B1` | Continuous narrative; spontaneous repair; handles routine standups. |
| $4.2 \le S_{SP} < 4.8$ | `B2` | High fluency; nuanced technical explanation; rare intrusive hesitation. |
| $4.8 \le S_{SP} \le 5.0$ | `C1 / C2` | Complete spontaneous fluency, natural idiom, and effortless prosody. |

#### Part D: Pronunciation & Articulatory Mechanics
- Task D1 (Perception): 5 minimal pair items ($[0, 5]$).
- Task D2 (Production): 4 candidate interference sentences scored for epenthesis, stress, nasal closure, and vowel quality ($[0, 5]$).
- Raw Score ($S_{PC}$): Range $[0.0, 10.0]$.

---

### 3.3 Written Composition & Lexical Size

#### Part E: Written Composition & Sentence Combining
- Task E1 (Sentence Combining): 3 items ($[0, 3]$).
- Task E2 (Functional Workplace Message): 3 criteria ($[0, 3]$).
- Raw Score ($S_W$): Range $[0.0, 6.0]$.

#### Part G: Lexical Size Sampling (Nation's VLT Format)
Samples from K1, K2, K3 bands (3 items per band = 9 items):
$$\text{Estimated Receptive Vocabulary Size } V_{\text{est}} = \sum_{k=1}^{3} \left( \frac{\text{Correct Items}_k}{3} \times 1,000 \right)$$
- $V_{\text{est}} < 800$ lemmas $\implies$ `Pre-A1 Lexicon`.
- $800 \le V_{\text{est}} < 1,500$ lemmas $\implies$ `A1 Lexicon`.
- $1,500 \le V_{\text{est}} < 2,500$ lemmas $\implies$ `A2 Lexicon`.
- $V_{\text{est}} \ge 2,500$ lemmas $\implies$ `B1+ Lexicon`.

---

## 4. Bottleneck Detection Engine

The system applies the **Weakest Link Principle** to determine what the 60-minute routine allocation engine must prioritize:

```python
def identify_bottleneck(profile_vector):
    # Hierarchy of communicative dependency:
    # 1. Phonological Intelligibility (epenthesis/stress breakdown blocks understanding)
    # 2. Receptive Acoustic Listening (inability to parse speech blocks interaction)
    # 3. Core Vocabulary (without K1 lemmas, syntax has no building blocks)
    # 4. Spoken Production / Fluency Latency
    # 5. Grammar & Written Composition

    if profile_vector["PC"] <= "A1" and profile_vector.get("epenthesis_severe", False):
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

## 5. Explainable Diagnostic Profile Card

Every scoring session generates an auditable, human-readable profile card:

```markdown
### Diagnostic Assessment Summary
- **Learner**: G. Bispo
- **Date**: YYYY-MM-DD
- **Assessment Mode**: Baseline Diagnostic Battery (Forms A/B)
- **Status**: Formative Diagnostic Profile (Not an accredited CEFR certification)

| Dimension | Raw Score | Diagnostic Band | Confidence Rating | Diagnostic Observation |
| :--- | :---: | :---: | :---: | :--- |
| **Acoustic Listening** | 3.0 / 7.0 | A1 | High | Connected speech causes breakdown; flapping and reductions missed. |
| **Text Reading** | 2.5 / 3.0 | A2 | High | Strong technical syntax parsing; grasps chronological flow. |
| **Spoken Production** | 1.5 / 5.0 | Pre-A1 | High | High retrieval latency (>5s); single-word responses. |
| **Phonological Control**| 4.0 / 10.0 | Pre-A1 | High | Final stop epenthesis marked; vowel contrast /i/-/ɪ/ collapsed. |
| **Written Composition**| 3.5 / 6.0 | A1+ | Medium | Understands basic connectors; needs irregular verb consolidation. |
| **Receptive Vocabulary**| 1,600 | A2 | High | Good K1 mastery; partial K2 knowledge; tech words recognized. |

- **Primary Cognitive Bottleneck**: `BOTTLENECK_PHONOLOGICAL_EPENTHESIS` + `ACOUSTIC_DECODING`
- **Dynamic Routine Prescription**: Prioritize bimodal reading-while-listening in Block 2; prioritize stop closure drills in Block 3.
```
