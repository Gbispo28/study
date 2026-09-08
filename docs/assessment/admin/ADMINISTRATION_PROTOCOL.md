# Administration Protocol: English Learning OS Diagnostic Battery

> **Audience**: Test Administrator / Evaluator / AI System Assessor.
> **Target Learner**: Adult Brazilian Portuguese native speaker entering the system.
> **Confidentiality Notice**: This file contains administrative controls, delivery standards, and operational guidelines. **DO NOT EXPOSE TO THE LEARNER PRIOR TO OR DURING TEST EXECUTION.**

---

## 1. Stimuli Standardization & Delivery Specifications

To ensure diagnostic reproducibility and avoid invalidating receptive testing through visual text leakage:

### 1.1 Audio Generation & Voice Baseline
- **Voice Target**: General American English (GAE). Standard non-regional broadcast accent.
- **Audio Source Options**:
  1. *Curated High-Fidelity Human Recordings*: Native GAE speaker recordings delivered as lossless or high-bitrate audio (`.mp3` $\ge 192\text{ kbps}$ or `.wav`).
  2. *Standardized High-Fidelity Neural TTS*: If human recordings are unavailable, use frontier neural speech synthesis (e.g., Gemini Voice API or Google Cloud TTS Neural2/Journey voice model `en-US-Journey-F` or `en-US-Journey-D`).
- **Synthetic TTS Limitation Notice**:
  > [!IMPORTANT]
  > While modern 2026 neural TTS produces realistic prosody, synthetic audio may exhibit minor artifacts in acoustic coarticulation, connected speech flapping, and unstressed vowel centralization compared to natural human discourse. The administrator must note whether synthetic TTS or human audio was utilized.

### 1.2 Speech Rate Guidelines
- **Task A1 (Spoken Comprehension)**:
  - Clip 1 (Connected speech): **130–145 wpm** (natural conversational pace with unstressed vowel reduction, flapping, and linking).
  - Clip 2 (Workplace appointment): **120–135 wpm** (clear professional tempo).
  - Clip 3 (Workplace report): **135–150 wpm** (standard technical cadence).
- **Task A2 (Micro-Dictation)**: **120–140 wpm**. Clean native connected pronunciation without artificial pauses between words.
- **Optional Task A3 (Extension)**: **160–180 wpm**. Fast conversational native cadence with natural idioms, conversational cross-talk tempo, and full unstressed vowel reduction.
- **Task D1 (Phonemic Minimal Pairs)**: Words pronounced clearly with a **1.0-second silence** between Pair Member 1 and Pair Member 2.

### 1.3 Playback & Replay Policy
- **Playback Limit**: Exactly **two (2) playbacks** permitted per item in Part A and Part D1.
- **Scrubbing / Pausing Prohibition**: The learner must listen to each clip continuously from beginning to end. Pausing, rewinding, or looping small fragments during playback is strictly prohibited.
- **Transcript Concealment**: Written transcripts and closed captions must remain strictly invisible to the learner until the entire diagnostic battery has been completed and submitted.

### 1.4 Hardware & Acoustic Environment
- **Headphone Requirement**: Learner must use binaural headphones or high-quality earbuds. Built-in laptop or smartphone speakers in reverberant rooms are discouraged to avoid confounding acoustic segmentation with room echo.
- **Microphone**: Standard smartphone headset microphone (e.g., Galaxy S24 Ultra built-in triple mic or AirPods/wired headset) held at a consistent distance from the mouth.
- **Session Splitting**: If the learner experiences fatigue, the assessment may be split into two sessions on consecutive days:
  - *Session 1*: Receptive Battery (Parts A & B) — ~25 minutes.
  - *Session 2*: Productive & Linguistic Battery (Parts C through G) — ~25 minutes.

---

## 2. Test Administration Checklist

```text
[ ] Verify learner has NOT accessed AUDIO_SCRIPTS.md, ITEM_KEY.md, or SCORING_GUIDE.md.
[ ] Confirm headphones and microphone are functioning properly.
[ ] Deliver BASELINE_FORM.md and SUBMISSION_TEMPLATE.md.
[ ] Play audio stimuli according to playback rules (max 2 plays, no pausing).
[ ] Receive completed SUBMISSION_TEMPLATE.md and 3 audio recording files:
    - spoken_c1 (monologue)
    - spoken_c2 (interaction scenario)
    - spoken_d2 (pronunciation read-aloud)
[ ] Ingest submissions into SCORING_GUIDE.md.
```
