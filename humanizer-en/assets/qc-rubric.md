# QC Rubric — Final Scoring, Loop Protocol, Stop Conditions

Reference asset for `humanizer-en` Stage 5 VERIFY. Score the *final* text after each round; the rubric gates the loop.

## 1. Score Dimensions (0–3 each, plus hard gates)

| Dimension | 0 (fail) | 1 | 2 | 3 (pass) |
|---|---|---|---|---|
| **Specificity** | no names/numbers/scenes anywhere | occasional anchor | most claims anchored | every key claim has a person, number, date, or scene (real, user-supplied — never invented) |
| **Stance** | no detectable opinion; both-sides throughout | hedged position | clear position on most claims | author takes positions, owns one strong one, admits one uncertainty |
| **Sentence-length variance** | CV < 0.25 | CV 0.25–0.34 | CV 0.35–0.44 | CV ≥ 0.45 with ≤6-word sentences present and no 4-in-a-row within ±3 words |
| **Connector diversity** | Moreover/Furthermore/Additionally chain throughout | heavy repetition | some variety | juxtaposition does most work; connectors unremarkable |
| **Lexical-tell density** | > 4.0/1k | 2.1–4.0/1k | 1.1–2.0/1k | ≤ 1.0/1k (per assets/lexical-tells.md tier weighting) |
| **Template-syntax density** | > 5.0/1k | 3.1–5.0/1k | 1.6–3.0/1k | ≤ 1.5/1k |
| **Hollow-rhetoric density** | > 5.0/1k | 3.1–5.0/1k | 1.6–3.0/1k | ≤ 1.5/1k |
| **Voice preservation** | reads like a different (nicer) author | markers mostly gone | markers intact | the author's tics, rhythm, and humor intact |
| **Register fit** | wrong genre entirely | frequent mismatch | occasional drift | genre-conventional throughout |

**Hard gates (any failure blocks regardless of rubric totals):**
- Thinking leakage: **0 instances** of assets/thinking-leakage.md groups A/B/C/E; group D judgment calls documented.
- Fact ledger diff: **empty** — every numeral, proper noun, URL, DOI, quote, citation unchanged.
- Register-mismatch score ≤ 1 for the target genre.

**Pass = all hard gates + ≥ 7 of 9 dimensions at 2+.**

## 2. Loop Protocol

1. Score after every round (Stages 2–4 = one round).
2. Fail → diagnose the worst 2 dimensions/categories → next round targets only those (don't re-sand passing categories; over-editing drifts voice and risks facts).
3. **Expect 2–3 rounds as the normal case; say so to the user.** (Per blader/humanizer: pattern-list editing needs ≥ 2 passes; per our 108-corpus experiment, flavor density only falls under iterated measurement.)
4. **Stop early** when a round improves total densities < 15% → report residuals instead of sanding forever. Every extra pass is another chance to break a fact or launder the voice.
5. Never loop more than 3 rounds without checking in with the user.

## 3. Over-Correction Audit (run once, after the final round)

Over-correction is its own AI flavor — "the AI flavor of anti-AI-flavor" (per Shen Zhirong 2026-07 warning on 反AI味的AI味). Check each; any hit → partially revert:

| Over-correction tell | Symptom | Revert by |
|---|---|---|
| Uniform choppiness | every sentence now 3–7 words; CV high but monotone rhythm | restore some long sentences where content carries lists |
| Compulsive coldness | all warmth stripped; reads hostile | re-add the author's own warm phrasings, not generic ones |
| Synonym-rotation pattern | delve→explore, crucial→vital, every swap mechanical | vary syntax instead; some words should simply be deleted |
| Forbidden-word superstition | "crucial" purged even where it is the precise term | restore precise words; density is the signal, presence is not |
| Specificity theater | invented names/numbers "to sound human" | remove fabrications; re-ask the user (hallucination ≠ humanization) |
| Detector-chasing | user starts optimizing for an AI-detector score | invoke §4 disclaimer; refuse to optimize detector scores |
| Voice laundering | output is competent but anonymous | restore author markers from the intake voice sample |

## 4. The HumT Warning — When Humanizing Is the Wrong Goal

Stanford's HumT line (Cheng, Yu & Jurafsky, ACL 2025, arXiv 2502.13259) measured humanness directly and found: humanized tone is *systematically adjustable* (HumT + decoding can dial it), **but users often prefer the less-human output** — humanness reads as warmth, femininity, and *lower status*, and in many task contexts it costs trust. Independently, human judges don't reliably prefer human-written text when blind (per Wang et al. ACL 2026, 87.6% detection ceiling but unstable preferences; per NYT 2026-03-09 quiz, 54% of readers preferred the AI passages).

**Therefore: stop humanizing when —**
1. The text is a support macro, safety/medical/financial notice, or system message — neutral machine register is the user-serving choice (per HumT).
2. The genre mandates formality (legal, regulatory, policy) — register is genre, not flavor.
3. The user asked for the assistant voice, explicitly or by clear context.
4. The rubric passes and one more round would only move detector cosmetics — that is out of scope by design.
5. Humanizing would mean inventing specifics the user hasn't supplied — ask or stop; never fabricate.

## 5. Detector Honesty (mandatory report language)

Include verbatim in every final report (Stage 5d):

> Note: stylometric detectors may still recognize this text as machine-assisted — humanizer attacks fool standard detectors but do not wash off style fingerprints (Rivera Soto et al., JHU 2025, arXiv 2505.14608). This skill's goal is text that reads human to human readers, not evading detection. Chasing detector scores is out of scope and counterproductive: detectors misfire both ways (61%+ of non-native-English essays falsely flagged, per Liang et al. 2023).

Do not run detectors, quote detector scores, or promise bypass rates. The commercial-humanizer market's bypass claims span 0–93% in independent testing (per fast.io 2026 review) — the number is noise, and optimizing for it produced the "dumb down the writing" anti-pattern documented among students forced to chase AI-rate scores (per our research/04: the 86.8% AI-rate case where a student degraded their own writing to satisfy a detector).

## 6. Report Skeleton (Stage 5c)

```
## humanizer-en report
Genre / audience / mode: …
Rounds run: N (deletions N, rewrites N, trace-wash removals N)
| Category          | Before /1k | After /1k | Gate | Status |
|-------------------|-----------:|----------:|------|--------|
| hollow rhetoric   |            |           | ≤3.0 |        |
| template syntax   |            |           | ≤3.0 |        |
| lexical tells     |            |           | ≤2.0 |        |
| register mismatch |            |           | ≤1   |        |
| thinking leakage  |            |           | 0    |        |
| sentence CV       |            |           | ≥.45 |        |
Fact-ledger diff: empty / exceptions…
Top changes: 10 lines, original → fixed
Trace-wash log: pattern IDs + one-line originals
Open specificity questions: …
[verbatim §5 disclaimer]
```

## Sources（出处）

- Cheng, Yu & Jurafsky, HumT & DumT (ACL 2025) — arxiv.org/abs/2502.13259
- Wang et al., human detection ceiling & preference instability (ACL 2026) — arxiv.org/abs/2502.11614; NYT "Who's a Better Writer" quiz (2026-03-09, 54% preferred AI passages)
- Rivera Soto et al., JHU 2025, style fingerprints survive humanizing — arxiv.org/abs/2505.14608
- Liang et al. 2023, non-native false positives (61%+ TOEFL essays) — sciencedirect.com/science/article/pii/S2666389923001307
- Sadasivan et al. 2023, detection unreliability under paraphrase — arxiv.org/abs/2303.11156
- blader/humanizer two-pass design — github.com/blader/humanizer
- Commercial-humanizer bypass divergence (0–93%) — fast.io/resources/undetectable-ai-review-2026/; 86.8% AI-rate degradation case — dzwww.com (2026-05-10), via our research/04
- Shen Zhirong over-correction warning (潮新闻 2026-07-27) — tidenews.com.cn/news.html?id=3512842
- Our 108-corpus experiment (loop calibration, directional) — ../../experiment/EXPERIMENT-NOTES.md
