# Research Note 0001: Assessment & CEFR Framework Alignment

- **Date**: 2026-09-08
- **Domain**: Assessment, Second Language Acquisition (SLA), Common European Framework of Reference (CEFR)
- **Primary Investigator**: Learning Science Researcher & Orchestrator
- **Epistemic Classification**: `EXPERT CONSENSUS` (CEFR Architecture) / `STRONG EVIDENCE` (Multi-trait Assessment Validity)

---

## 1. Research Question

How should the **English Learning OS** design its proficiency assessment model to accurately diagnose and track an adult learner (Brazilian native speaker, tech background) across the full CEFR spectrum (Pre-A1 through C2) without falling into the trap of a single collapsed scalar score, artificial ceiling caps, or false claims of official psychometric certification?

---

## 2. Theoretical & Methodological Foundations

### 2.1 Council of Europe CEFR Companion Volume (2020)
The CEFR was comprehensively updated in the *Common European Framework of Reference for Languages: Learning, Teaching, Assessment – Companion Volume* (Council of Europe, 2020). Key structural shifts critical for our architecture include:
1. **Replacement of the 4-skills model with 4 communicative modes**:
   - **Reception** (Listening & Reading)
   - **Production** (Spoken & Written Production)
   - **Interaction** (Spoken & Written Interaction)
   - **Mediation** (Explaining data, translating concepts, facilitating collaboration)
2. **De-emphasis of native-speaker norms**:
   - Phonological control descriptors were completely rewritten in 2020. The target is explicitly defined as **intelligibility**, **articulatory clarity**, and **prosodic control**, rather than accent extinction or resemblance to an idealized native speaker.
3. **Full Scale Descriptors vs. Custom Instrument Measurement Ceiling**:
   - The Companion Volume establishes descriptors across the entire continuum: **Pre-A1, A1, A2, B1, B2, C1, and C2**.
   - However, an assessment instrument's operational measurement range depends strictly on item sampling depth. A compact diagnostic battery (~60 min) cannot defensibly discriminate higher-tier proficiencies (C1 vs C2) without extensive multi-genre reading, complex discursive listening, and varied oral interviews.
   - **Canonical Instrument Boundary**: The internal diagnostic battery operates with an **explicit measurement ceiling at B2**. When performance approaches or exceeds this ceiling, the system outputs `ABOVE CURRENT INSTRUMENT CEILING — EXTERNAL/EXTENDED ASSESSMENT REQUIRED`. It never infers C1 or C2 from single isolated advanced items.

### 2.2 Formative Routing & Measurement Ceiling Policy
To profile beginner-to-intermediate learners without inducing test fatigue:
- **Core Formative Routing**: The battery evaluates Pre-A1, A1, A2, and intermediate B1/B2 competencies, locating the learner's specific communicative bottlenecks.
- **Adaptive Early Stopping**: If an adult beginner demonstrates severe failure on initial core items ($<40\%$ on A1 listening), testing in that dimension terminates immediately to prevent cognitive distress and invalid guessing.
- **Ceiling Reporting**: Learners demonstrating near-perfect performance across core and extension items are flagged as exceeding the custom battery's measurement range, with high-level evaluation deferred to certified external instruments (e.g., Cambridge, IELTS).

---

## 3. Official CEFR Scales vs. English Learning OS Diagnostic Dimensions

To maintain strict scientific integrity, we explicitly distinguish between **Official CEFR Companion Volume Scales** and **Custom English Learning OS Diagnostic Dimensions**:

| Custom Diagnostic Dimension | Mapped Official CEFR Scale (Council of Europe 2020) | Scope & Measurement Modality | Instrument Measurement Range |
| :--- | :--- | :--- | :---: |
| **Acoustic Listening** | Overall Listening Comprehension; Understanding Conversation | Audio playback without text; speed/reduction tolerance. | Pre-A1 to B2 (Ceiling at B2) |
| **Text Reading** | Overall Reading Comprehension; Reading for Information | Silent reading; comprehension & inferencing items. | Pre-A1 to B2 (Ceiling at B2) |
| **Spoken Monologue Production** | Sustained Monologue (Describing Experience / Putting a Case) | Elicited oral summary / recorded technical explanation. | Pre-A1 to B2 (Ceiling at B2) |
| **Spoken Interactive Turn-Taking** | Overall Spoken Interaction; Goal-Oriented Cooperation | Real-time conversational dialogue with AI partner. | Pre-A1 to B2 (Ceiling at B2) |
| **Written Composition** | Overall Written Production; Creative & Functional Writing | Prompted composition; sentence combining and issue synthesis. | Pre-A1 to B2 (Ceiling at B2) |
| **Phonological Control** | Phonological Control (Sound Articulation, Prosody, Intelligibility) | Minimal pair perception + acoustic production analysis. | Pre-A1 to B2 (Ceiling at B2) |
| **Operational Grammar** | *Custom Dimension* (Informed by English Grammar Profile) | Functional sentence frames in use; syntactic complexity. | Pre-A1 to B2 (Ceiling at B2) |
| **Receptive Lexical Familiarity** | *Custom Dimension* (Informed by English Vocabulary Profile) | Categorical band familiarity (K1, K2, K3 bands). | Foundational to Intermediate |
| **Productive Lexical Recall** | *Custom Dimension* (Informed by Vocabulary Control) | Elicited lexical production in communicative context. | Pre-A1 to B2 (Ceiling at B2) |

---

## 4. Crucial Regulatory & Psychometric Disclaimers

1. **Non-Certified Diagnostic Tool**: The English Learning OS Diagnostic Pack is an **internal pedagogical placement and progress-profiling instrument**. It is **NOT an officially accredited, certified, or endorsed Council of Europe examination** (such as Cambridge English, IELTS, or TOEFL). It provides formative diagnostic information to guide daily study allocations, not legal or academic certification.
2. **Explicit Rejection of Pseudo-Precision**: Scoring rejects arbitrary raw-score tables, fictitious statistical confidence intervals, and continuous vocabulary size extrapolations from small item sets. Proficiency is assessed against qualitative behavioral descriptors.
3. **Copyright Protection of Original Frameworks**: The CEFR Companion Volume descriptors, English Profile research, and academic Vocabulary Levels Tests (VLT) are referenced with scholarly attribution. All specific test prompts and assessment items in `docs/assessment/` are custom-authored for the English Learning OS.

---

## 5. Architectural Implications for English Learning OS

1. **Multi-Dimensional State Vector with B2 Ceiling**:
   $$\vec{P} = \langle L, R, SP, SI, W, PC, GC, VR, VP \rangle$$
   Each dimension is assigned a qualitative band from `Pre-A1` to `B2` (or `> B2 Ceiling`), accompanied by an explicit non-parametric `Confidence Rating` (`High`, `Medium`, `Low`).
2. **Decoupled Curriculum Routing**: If a learner is B2 in Reading but A1 in Spoken Interaction, the system delivers B2 reading materials while delivering A1 scaffolded oral production drills.

---

## 6. Authoritative References

1. Council of Europe (2020). *Common European Framework of Reference for Languages: Learning, teaching, assessment – Companion volume*. Strasbourg: Council of Europe Publishing. [https://www.coe.int/en/web/common-european-framework-reference-languages](https://www.coe.int/en/web/common-european-framework-reference-languages)
2. Cambridge University Press & UCLES (2015). *English Vocabulary Profile & English Grammar Profile*. English Profile Studies. [https://www.englishprofile.org/](https://www.englishprofile.org/)
3. Alderson, J. C. (2005). *Diagnosing foreign language proficiency: The interface between learning and assessing*. Continuum.
4. North, B. (2014). *The CEFR in Practice*. Cambridge University Press.
