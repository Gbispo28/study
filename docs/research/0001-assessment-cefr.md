# Research Note 0001: Assessment & CEFR Framework Alignment

- **Date**: 2026-09-08
- **Domain**: Assessment, Second Language Acquisition (SLA), Common European Framework of Reference (CEFR)
- **Primary Investigator**: Learning Science Researcher & Orchestrator
- **Epistemic Classification**: `EXPERT CONSENSUS` (CEFR Architecture) / `STRONG EVIDENCE` (Multi-trait Assessment Validity)

---

## 1. Research Question

How should the **English Learning OS** design its proficiency assessment model to accurately diagnose and track an adult learner (Brazilian native speaker, tech background) without falling into the trap of a single collapsed scalar score or falsely presuming an initial A0/A1 across all skill dimensions?

---

## 2. Theoretical & Methodological Foundations

### 2.1 Council of Europe CEFR Companion Volume (2020)
The CEFR was comprehensively updated in the *Common European Framework of Reference for Languages: Learning, Teaching, Assessment – Companion Volume* (Council of Europe, 2020). Key structural shifts critical for our architecture include:
1. **Replacement of the 4-skills model with 4 communicative modes**:
   - **Reception** (Listening & Reading)
   - **Production** (Spoken & Written Production)
   - **Interaction** (Spoken & Written Interaction)
   - **Mediation** (Explaining data, translating concepts, facilitating pluricultural collaboration)
2. **De-emphasis of native-speaker norms**:
   - Phonological control descriptors were completely rewritten in 2020. The target is explicitly defined as **intelligibility**, **articulatory clarity**, and **prosodic control**, rather than accent extinction or resemblance to an idealized native speaker.
3. **Pre-A1 definition**:
   - The Companion Volume formally established descriptors for **Pre-A1**, defining the threshold where a learner can recognize isolated familiar words, recognize simple numbers, and produce single-word greetings.

### 2.2 English Profile (Cambridge & Council of Europe)
The *English Profile Programme* provides empirical corpus evidence (Cambridge Learner Corpus) of what learners actually produce at each CEFR level:
- **English Vocabulary Profile (EVP)**: Details words, phrases, idioms, and phrasal verbs mapped to levels A1 through C2. Crucially, EVP demonstrates that words are polysemous across levels: *head* as a body part is A1, *head* as "leader" is B1, and *head* as a verb ("head towards") is B2.
- **English Grammar Profile (EGP)**: Details grammatical forms and functional categories across levels A1–C2. It shows that basic word order (SVO) and present continuous for immediate actions emerge at A1, whereas modal verbs of obligation, present perfect for unfinished time, and comparative structures solidify at A2/B1.

---

## 3. Core Findings & Diagnostic Insights

### 3.1 The Fallacy of the Collapsed Scalar Score
In commercial language testing (e.g., Duolingo score, raw TOEIC number), a learner is assigned a single scalar score (e.g., "A2" or "62/100").
In empirical SLA, adult learners—especially software engineers who interact daily with technical documentation, code syntax, and error messages—exhibit **highly jagged, multi-dimensional profiles**:
- **Receptive Reading**: Frequently A2 or B1 (capable of parsing documentation, Git commands, technical articles).
- **Acoustic Listening**: Frequently A1 (struggling with connected speech, reductions, and fast native tempo).
- **Spoken Interaction**: Frequently Pre-A1 or A0 (high affective filter, extreme latency during spontaneous retrieval, lack of articulatory habit).
- **Writing**: Frequently A1/A2 in controlled environments with asynchronous processing.

**Pedagogical Conclusion**: Collapsing these divergent competencies into a single "A1" label misdiagnoses the learner's actual cognitive bottlenecks and leads to mismatched curriculum assignments (e.g., forcing a learner to read trivial "cat on the mat" texts when their actual barrier is auditory phoneme segmentation).

### 3.2 English Learning OS Diagnostic Dimensions vs Official CEFR
To maintain scientific integrity, we explicitly distinguish between **Official CEFR Dimensions** and **System-Specific Diagnostic Dimensions**:

| Diagnostic Dimension | Mapped Official CEFR Scale (2020) | Measurement Modality |
| :--- | :--- | :--- |
| **Acoustic Listening** | Overall Listening Comprehension; Understanding Conversation | Audio playback without text; speed/reduction tolerance |
| **Text Reading** | Overall Reading Comprehension; Reading for Information | Silent reading; comprehension & inferencing items |
| **Spoken Production** | Sustained Monologue (Describing Experience / Giving Information) | Elicited oral summary / picture narration (recorded audio) |
| **Spoken Interaction** | Overall Spoken Interaction; Conversation | Turn-taking with conversational AI / structured prompts |
| **Written Composition** | Overall Written Production; Creative / Functional Writing | Prompted composition; sentence-combining accuracy |
| **Phonological Control** | Phonological Control (Intelligibility, Prosody, Articulation) | Minimal pairs perception + acoustic production analysis |
| **Grammatical Competence** | General Linguistic Range; Grammatical Accuracy | Productive sentence completion + functional grammar usage |
| **Receptive Vocabulary** | Vocabulary Range (Receptive) | Vocabulary Levels Test (VLT) frequency sampling (1k–5k) |
| **Productive Vocabulary** | Vocabulary Control (Productive) | Elicited naming & translation in communicative context |

---

## 4. Conflicting Evidence & Boundary Conditions

- **Subjective Self-Assessment Bias**: Research on the CEFR Self-Assessment Grid (Blanche & Merino, 1989; Ross, 1998) shows that low-proficiency learners frequently over-estimate their speaking ability due to lack of metacognitive awareness (Dunning-Kruger effect), while anxious learners severely underestimate their receptive listening and reading skills.
  - *Mitigation*: Self-assessment questionnaires (intake) must be validated by objective performance tasks in the baseline battery.
- **Practice Effects in Repeated Testing**: Administering identical CEFR assessment tasks closer than 60–90 days apart produces artificial gains driven by test familiarity rather than linguistic acquisition (Alderson, 2005).

---

## 5. Architectural Implications for English Learning OS

1. **Multi-Dimensional Baseline Vector**: The system must represent learner state as a vector:
   $$\vec{P} = \langle L, R, SP, SI, W, PC, GC, VR, VP \rangle$$
   where each dimension ranges from `Pre-A1` to `C2`, accompanied by an explicit confidence rating (`Low`, `Medium`, `High`).
2. **Deterministic Diagnostic Battery**: Author `docs/assessment/BASELINE_PROTOCOL.md` and `docs/assessment/SCORING_MODEL.md` to evaluate each dimension independently using objective scoring criteria and transparent rubrics.
3. **Curriculum Decoupling**: Receptive input content must be calibrated to the learner's Reading/Listening levels, while spoken drills must be calibrated to their Spoken Production level.

---

## 6. Authoritative References

1. Council of Europe (2020). *Common European Framework of Reference for Languages: Learning, teaching, assessment – Companion volume*. Strasbourg: Council of Europe Publishing. [https://www.coe.int/en/web/common-european-framework-reference-languages](https://www.coe.int/en/web/common-european-framework-reference-languages)
2. Cambridge University Press & UCLES (2015). *English Vocabulary Profile & English Grammar Profile*. English Profile Studies. [https://www.englishprofile.org/](https://www.englishprofile.org/)
3. Alderson, J. C. (2005). *Diagnosing foreign language proficiency: The interface between learning and assessing*. Continuum.
4. Blanche, P., & Merino, B. J. (1989). Self-assessment of foreign-language skills: Implications for teachers and researchers. *Language Learning*, 39(3), 313-338. doi:10.1111/j.1467-1770.1989.tb00595.x
5. North, B. (2014). *The CEFR in Practice*. Cambridge University Press.
