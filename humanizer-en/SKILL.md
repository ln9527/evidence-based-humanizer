---
name: humanizer-en
description: |
  Five-stage pipeline (DIAGNOSE → SUBTRACT → REWRITE → TRACE-WASH → VERIFY) that strips AI flavor from English prose, articles, and documentation. One pass never fully de-flavors a text — the skill loops, typically 2-3 rounds, until per-category density thresholds pass. Specialty: washing reasoning-model leakage ("Wait,", "Alternatively,", "Thought for X seconds"), agent narratives, and model-draft diagrams out of final drafts, plus era-stratified lexical tells (2023 assistant residue → 2024 delve era → 2025 core/modern era). Use when a draft reads machine-flavored: hollow rhetoric, forced triads, template syntax, uniform sentence rhythm, register mismatch, or visible chain-of-thought residue. Trigger words: "humanize this", "de-AI this", "remove the AI flavor", "de-slop", "make this sound human", "less ChatGPT-y", "it reads like AI wrote it". Do NOT use for legal, contractual, or regulatory text whose register must stay formal, for safety-critical notices, or when the user explicitly wants an assistant voice. The goal is text that reads human to humans — NOT beating AI detectors.
---

# humanizer-en

De-flavor English prose in five stages. Execute every stage in order. Do not skip stages. Do not merge stages. Measure before and after; never edit by feel alone. (Method follows blader/humanizer's evidence that pattern-list editing needs two passes minimum, per github.com/blader/humanizer.)

## 0. Ground Rules

1. **Freeze the facts.** Before touching a word, extract every numeral, proper noun, URL, DOI, quote, and citation into a fact ledger. Never alter them. Never add new ones. (Stage 5a enforces this with a diff.)
2. **One pass is never enough.** Expect 2–3 full rounds of Stages 2–4 before thresholds pass. State this to the user up front. (Per blader/humanizer two-pass design; per our 108-corpus experiment, flavor density is only visible — and only fixable — under iterative measurement.)
3. **Optimize for human readers, not detectors.** Do not run, cite, or promise AI-detector scores. Humanizer output still carries a style fingerprint that few-shot stylometric detectors recognize (per JHU 2025, Rivera Soto et al., arXiv 2505.14608), and the detectors themselves are unreliable (per Sadasivan et al. 2023).
4. **Preserve the author's voice.** Before rewriting, read 2–3 paragraphs, list the voice markers (contractions? first person? parentheticals? dry humor?), and keep them. (Per blader/humanizer: match the user's voice; per Lambert 2025, alignment already destroys voice — do not destroy it twice.)
5. **Never fabricate specifics.** If a claim needs a name, number, date, or scene, ask the user. Invented details are hallucination dressed as humanization. (Stage 3 protocol.)
6. **Density beats presence.** A single "crucial" is human. Three era-tell words per 1,000 is the machine. Diagnose on density; never blacklist a word absolutely. (Per our 108-corpus experiment: perceived AI flavor = model default + repetition, not single tokens.)
7. **Do not sterilize.** The target is a page that reads like one person thinking, not a smoothed committee draft. Keep asides, allow one deliberate em dash, keep the precise buzzword when it is the exact term.

## 1. When to Use / When NOT to Use

**Use when:**
- A draft in English (article, essay, blog post, docs, newsletter, report) reads machine-flavored and the user wants it to read human.
- Trigger phrases appear: "humanize this", "de-AI this", "remove the AI flavor", "de-slop this", "make this sound human / less robotic / less ChatGPT-y", "it reads like AI wrote it", "wash the agent traces out of this".
- A deliverable still contains reasoning-model residue, agent narration, or "Thought for X seconds" UI text (go straight to Stage 4, then run the full pipeline).

**When NOT to use:**
- **Legal, contractual, regulatory, or policy text.** Formal register is the genre, not a flavor. Do not casualize it. (Per register-mismatch category: flavor = model default × genre mismatch — a contract is supposed to read like a contract.)
- **Safety-critical notices, medical or financial disclaimers, support macros.** Neutral assistant register may be exactly what the user needs; humanizing measurably lowers user preference in many such contexts (per HumT, Stanford ACL 2025, arXiv 2502.13259).
- **The user explicitly wants an assistant voice** ("keep it polite/formal/assistant-like"). Stop and confirm scope; if confirmed, do not run.
- **The "flavor" is genre convention.** Academic abstracts were dense and formulaic before LLMs (per Ong/zaobao 2026 analysis of The Economist style features predating LLMs); confirm with the user before stripping conventions the venue requires.
- **Code logic itself.** This skill cleans comments and docs, never code semantics.

### Intake (run once, before Stage 1)

Ask the user for — or infer and then *state your assumptions about*:

1. **Genre and venue** (blog, essay, docs, newsletter, report). This sets the register baseline; flavor is measured against genre, not against a universal ideal (per register-mismatch category; per our 108-corpus Finding C).
2. **Audience** and their tolerance for informality.
3. **Two or three human-written exemplars** in the same genre, or the venue's style guide (feeds the Stage 3 re-register strategy). If absent, proceed with stated assumptions.
4. **A voice sample** of the author — any earlier writing by the same person (feeds the voice-marker list, Ground Rule 4).
5. **Scope**: whole text or only flagged sections.
6. **Mode**: *interactive* (you may ask specificity questions mid-run) or *batch* (mark `[NEEDS SPECIFIC: …]` instead of asking).

Never block the pipeline on intake. If the user is absent, run in batch mode and declare the assumptions in the final report.

## 2. Pipeline Overview

```
INPUT TEXT
   │
   ▼
[Stage 1 DIAGNOSE]   score 5 flavor categories per 1k words → pick dominant flavor
   │
   ▼
[Stage 2 SUBTRACT]   deletion-only pass: triads, frames, tails, hedge stacks
   │
   ▼
[Stage 3 REWRITE]    strategy per dominant flavor + variance repair + specificity asks
   │
   ▼
[Stage 4 TRACE-WASH] strictest pass: CoT / agent / UI / draft-diagram / code-comment residue → 0
   │
   ▼
[Stage 5 VERIFY]     fact diff → re-diagnose → loop to Stage 2 if fail (max 3 rounds) → report
```

| Stage | Input | Output | Pass gate |
|---|---|---|---|
| 1 DIAGNOSE | raw text | scorecard (5 densities + sentence CV + dominant flavor) | scorecard exists, categories sum ≥ 1/1k to proceed |
| 2 SUBTRACT | raw text | shortened text + deletion log | every deletion-menu hit handled |
| 3 REWRITE | subtracted text | rewritten text + open specificity questions | dominant-flavor strategy applied; CV ≥ 0.35 |
| 4 TRACE-WASH | rewritten text | clean text + trace log | 0 leakage instances (absolute) |
| 5 VERIFY | clean text + fact ledger | final text + before/after report | all thresholds in §3 met, fact diff empty |

## 3. Stage 1 — DIAGNOSE

**Measure, do not vibe.** Compute, do not estimate.

**Protocol:**
1. `word_count` = whitespace-split tokens of body prose (exclude code blocks; code is scanned separately in Stage 4E).
2. Count pattern hits per category using the lists in `assets/lexical-tells.md` (lexical), `assets/signs-patterns.md` (syntax, rhetoric), `assets/thinking-leakage.md` (leakage).
3. `density = hits / word_count × 1000` for each category.
4. Sentence stats: split on `[.!?]+`; sentence length in words; `CV = stdev / mean`.

**The five categories:**

| # | Category | What counts | Basis |
|---|---|---|---|
| 1 | **hollow rhetoric** | meaning-elevation frames ("plays a crucial role in shaping"), empty openers ("In today's fast-paced world"), summary tails ("In conclusion…"), recap paragraphs restating the intro, "correct nonsense" that survives deletion of all specifics | per Atlantic 2023 (LinkedIn voice); per Liang et al. 2025 "empty rhetoric" taxonomy, arXiv 2507.07484 |
| 2 | **template syntax** | forced triads ("X, Y, and Z" filler), "It's not about X, it's about Y" molds, "not only…but also" chains, uniform paragraph shapes (claim–expansion–example–mini-conclusion), em-dash as universal connector | per Wikipedia Signs of AI writing; per Sam Kriss NYT 2025-12; per em-dash study arXiv 2608.05889 |
| 3 | **lexical tells** | era-stratified word hits: 2023 assistant residue, 2024 delve-era (delve/underscores/showcasing/intricate…), 2025 core/modern era, plus current watchlist. Use evidence tiers: quantified > community > folk (never score folk-tier alone) | per Kobak 2024 (Science Advances 2025); per WaPo 2025 (328,744 msgs); per GPTZero AI Vocabulary |
| 4 | **register mismatch** | LinkedIn/assistant register in a casual scene; marketing lyricism in technical docs; conversational asides in formal reports. Score 0–3 against the genre's conventions (3 = reads like the wrong genre entirely) | per our 108-corpus experiment Finding C (same model spans 3–8× across genres); per Berber Sardinha 2024 (Biber register shift) |
| 5 | **thinking leakage** | reasoning-model residue ("Wait,", "Alternatively,", "Let me check"), self-correction traces, agent narrative ("I will now…"), task checkboxes in prose, UI residue ("Thought for X seconds"), model-draft diagrams passed off as reader illustrations, narrative code comments | per R1 paper arXiv 2501.12948; per arXiv 2605.28305; per claude-code issues #85130/#65961; per Sketchpad NeurIPS 2024 |

**Thresholds (pass gate, re-checked at Stage 5b):**

| Metric | Fail if | Target |
|---|---|---|
| hollow rhetoric density | > 3.0 / 1k | ≤ 1.5 / 1k |
| template syntax density | > 3.0 / 1k | ≤ 1.5 / 1k |
| lexical tells density | > 2.0 / 1k | ≤ 1.0 / 1k |
| register mismatch score | ≥ 2 (of 3) | ≤ 1 |
| thinking leakage instances | ≥ 1 anywhere | 0 (absolute) |
| sentence-length CV | < 0.35 | ≥ 0.45 |

Thresholds are calibrated heuristics, not lab constants (calibrated directionally on our 108-corpus experiment, flash-tier models, n=3/cell — treat as starting points and adjust once per genre: tighten lexical for marketing copy, loosen it for technical reference, never loosen leakage).

**Dominant flavor rule:** dominant = category with the highest exceedance relative to its threshold. Tie-break order: thinking leakage → register mismatch → hollow rhetoric → template syntax → lexical tells. If thinking leakage dominates, run Stage 4 *before* Stage 3, then re-diagnose.

**Output:** a scorecard — table of densities, CV, register score, dominant flavor, and the 10 worst sentences with line references.

## 4. Stage 2 — SUBTRACT

Deletion only. No rewriting, no synonym swaps in this stage. Cutting first is cheaper than rewriting: most AI flavor is additive filler around a soundable claim (per ninehills/deslop-zh "subtraction first" principle; per our 108-corpus Finding D — transition boilerplate and elevation frames, not exotic jargon, dominate real output).

**Deletion menu — delete on sight:**

| # | Delete | Example | Basis |
|---|---|---|---|
| 1 | Forced triads where the three items are near-synonyms or filler | "innovation, inspiration, and insights" → keep as many items as the meaning needs (1 or 2) | Wikipedia sign #10 / blader pattern |
| 2 | "It's not about X, it's about Y" / "not just X — it's Y" molds | "It's not about the tool; it's about the trust." → state Y directly: "What matters is trust." | per Sam Kriss NYT 2025-12-03; our 108-corpus Finding E (the "not X but Y" mold is a per-vendor tic) |
| 3 | Summary tails and recap paragraphs | "In conclusion, …", "Overall, …", final paragraphs that restate the intro verbatim | Wikipedia signs; Gen-1 hollow fluency per Atlantic 2023 |
| 4 | Meaning-elevation frames | "plays a crucial role in shaping", "stands as a testament to", "In the ever-evolving landscape of" | per Kobak 2024 style-word class; folk-tier caution for "testament" (zero quantified evidence — delete for hollowness, not as a "proven tell") |
| 5 | Empty openers | "It's important to note that", "It's worth mentioning that", "Needless to say" → let the claim stand naked | Wikipedia signs; Gen-1 "correct nonsense" per 九派/Atlantic 2022–23 |
| 6 | Hedge stacks | "arguably perhaps somewhat may potentially" → keep at most one hedge per claim | per overthinking literature arXiv 2503.16419 |
| 7 | Meta-narration of the text itself | "In this article, we will explore…", "As mentioned above", "Let's dive in!" | Wikipedia signs; agent-narrative cousin (Stage 4B) |

**Do not delete:** facts, citations, numbers, quotes (fact ledger), the author's genuine opinions, deliberate rhetorical triads the user wrote on purpose (ask when unsure), genre-required furniture (e.g., abstract headers).

**Output:** shortened text + deletion log (every deletion, one line each: original → reason).

## 5. Stage 3 — REWRITE

**Pick strategy from Stage 1's dominant flavor. One dominant flavor per round:**

| Dominant flavor | Strategy | Basis |
|---|---|---|
| hollow rhetoric | **Compression + stance.** Delete the frame, then force every claim to have a subject and a verb and a stake. Convert "There are several considerations regarding X" into "X breaks in two cases: …". One hedge max. | per Liang 2025 (empty rhetoric is measurable); per Atlantic 2023 |
| template syntax | **Pattern-breaking.** Break the third item of every remaining triad. Rotate connectors (and/but/so/semicolon/nothing). Quota: one mold per section, then restructure. Let juxtaposition do the work. | per Wikipedia sign #10; per blader |
| lexical tells | **Context-fit substitution.** Replace a tell only where it does no work: "showcasing" → usually delete the clause; "intricate" → name the actual complexity ("a 14-step approval chain"). NEVER global find-replace — mechanical synonym rotation is the commercial-humanizer move and leaves the style fingerprint intact (per JHU 2025). | per Kobak 2024; per shuorenhua "no mechanical swaps" |
| register mismatch | **Re-register.** Identify the target genre, obtain 2–3 human exemplars from the user (or cite the venue's style), recalibrate formality, person, density, sentence budget to that genre. | per our 108-corpus Finding C (flavor = default register × genre mismatch); per Berber Sardinha 2024 |
| thinking leakage | Escalate: run Stage 4 first, re-diagnose, then apply the now-dominant strategy. | per R1 2025; arXiv 2605.28305 |

**Sentence-length variance repair** (per GPTZero 2023 burstiness concept — AI sentence length is too uniform):
1. Compute sentence CV after rewriting. Target ≥ 0.45, floor 0.35.
2. Require ≥ 1 sentence of ≤ 6 words per 300 words. Allow an occasional 35+ word sentence when it carries a list.
3. Forbid > 3 consecutive sentences within ±3 words of each other — split or merge one.
4. Do NOT manufacture fake variance (random choppy fragments). Artificial burstiness is detector-gaming, and it creates the over-corrected "anti-AI flavor" (see §8). Split and merge only where meaning supports it. (Per Liang 2023: trivial prompt-based burstiness gaming exists and proves nothing; per Shen 2026 over-correction warning.)

**Specificity injection — ask, never invent:**
1. After the first rewrite pass, list every abstract claim lacking an anchor (person, number, date, place, scene, named artifact).
2. Ask the user in ONE batch, max 5 questions: "Who exactly did X?", "How many / what percent?", "When did this happen?", "What did the scene look like?", "What did you try first that failed?"
3. Weave the answers in as concrete nouns and verbs.
4. Batch mode (user unavailable): insert `[NEEDS SPECIFIC: number of teams]` markers and list them in the final report. Do not guess.
Basis: human readers detect AI writing through specificity, cultural detail, and diversity (per Wang et al. ACL 2026, 87.6% human ceiling); de-flavoring's terminal form is putting the human material — judgment, lived numbers, risk — back in (per our research synthesis).

**Voice preservation:** re-read the voice-marker list from Ground Rule 4 after rewriting. If markers vanished, restore them. If the text now sounds like a different (nicer, blander) person, you over-rewrote — revert partially.

## 6. Stage 4 — TRACE-WASH (strictest pass)

This is the skill's specialty and its zero-tolerance zone. Reasoning traces are the newest and most damning flavor: a "Wait," in a shipped article proves machine authorship to any reader, no detector needed (per R1 paper's own celebrated "Wait, wait. Wait."; per DeepSeek-R1 Thoughtology taxonomy arXiv 2504.07128).

**Policy:** categories A, B, C, E are zero-tolerance — one surviving instance fails the whole pass. Category D requires the judgment test below. Full pattern library with regexes, examples, and fixes: `assets/thinking-leakage.md`.

| Group | Scan for | Severity |
|---|---|---|
| A. Reasoning-model residue | "Wait,", "Hmm,", "Alternatively,", "Let me check/verify/try", "That was wrong", "On second thought", self-correction pairs (claim → retraction → new claim), hedging cascades that rehearse the model's option-weighing, "aha"-style discoveries narrated to the reader | zero tolerance |
| B. Agent narrative | "I will now…", "Let me…", "Next, I'll…", "First, I need to…", "I've finished the task", "Here is the revised version", "As requested", task checkboxes `- [ ]` / `- [x]` embedded in prose, TODO markers, progress logs, meta-commentary about the conversation | zero tolerance |
| C. UI/product residue | "Thought for X seconds", "Deep thinking (7.41 seconds)"-style chrome, `<think>` tags, "Assistant:" / "Analysis:" labels, "due to length constraints", capability disclaimers pasted from chat | zero tolerance |
| D. Model-draft diagrams | Mermaid/flowcharts/graphs that map *how the model organized or verified its thinking* (outline-as-diagram, verification scratch work, "my approach" flowcharts), ASCII math checks, SVG illustrations the model drew blind. Judgment test: **"Does this image show the reader a conclusion, or record the process of reaching one?"** Conclusions stay; process records go. | judgment |
| E. Narrative code comments | "Now we implement X", "Let's create…", "This fixes the issue where…", exploration dead code left commented, changelog-style comments, swallowed exceptions. Keep interface-contract doc comments (they serve the reader); delete process narration (it belongs in git, not the file — per anthropics/claude-code issue #85130). | zero tolerance |

Why D works this way: models draw diagrams *for themselves* as cognitive tools — visual chain-of-thought measurably improves their reasoning (per Visual Sketchpad, NeurIPS 2024, ~12.7% math gain), and tooling now renders thinking-time Mermaid into chat (per VS Code 1.109, heise 2026). The reader-facing illustration and the model's scratch paper are different genres; shipping the scratch paper as a figure is the visual form of thinking leakage. LLM-drawn SVG is additionally "blind drawing" with systematic geometry/text-overflow failures (per dev.to/CVPR 2025 analyses).

**Re-scan after every round.** New leakage appears when later edits quote or paraphrase earlier reasoning. Stage 5b re-runs this scan each round; the pass gate stays at absolute zero.

## 7. Stage 5 — VERIFY

**5a. Fact-diff self-check (mandatory, first):**
1. Re-extract the fact ledger (numerals+units, proper nouns, URLs, DOIs, quotes, citations) from the final text.
2. Diff against the pre-edit ledger. Any change → restore the original or escalate to the user.
3. Numbers change only if the user explicitly requested recomputation. Zero exceptions.

**5b. Re-diagnose and loop:**
1. Re-run the full Stage 1 scorer on the current text.
2. All thresholds pass → proceed to 5c.
3. Any threshold fails → run another round of Stages 2–4 targeting the failing categories. **State plainly: this usually takes 2–3 rounds** (per blader two-pass design; per our 108-corpus loop experience).
4. Stop early when a round improves category densities by < 15% → do not sand forever; each extra pass risks voice drift and fact drift. Report residuals honestly instead.

**5c. Before/after report (always emit):**

```
## humanizer-en report
| Category            | Before /1k | After /1k | Threshold | Status |
|---------------------|-----------:|----------:|-----------|--------|
| hollow rhetoric     |            |           | ≤ 3.0     |        |
| template syntax     |            |           | ≤ 3.0     |        |
| lexical tells       |            |           | ≤ 2.0     |        |
| register mismatch   |            |           | ≤ 1       |        |
| thinking leakage    |            |           | 0         |        |
| sentence CV         |            |           | ≥ 0.45    |        |
Rounds run: N. Deletions: N. Rewrites: N. Trace-wash removals: N.
Top changes: (10 lines, original → fixed)
Open specificity questions: (from Stage 3, if any)
```

**5d. Mandatory disclaimer — include verbatim in every report:**

> Note: stylometric detectors may still recognize this text as machine-assisted — humanizer attacks fool standard detectors but do not wash off style fingerprints (Rivera Soto et al., JHU 2025, arXiv 2505.14608). This skill's goal is text that reads human to human readers, not evading detection. Chasing detector scores is out of scope and counterproductive: detectors misfire both ways (61%+ of non-native-English essays falsely flagged, per Liang et al. 2023).

## 8. Over-Correction Guards ("the AI flavor of anti-AI-flavor")

Over-corrected text is a new tell (per Shen 2026, "反AI味的AI味" warning). After the final round, check and fix:

1. **Uniform choppiness.** All-short sentences = the new uniformity. Restore CV naturally (§5).
2. **Compulsive coldness.** Deleted every warm word → text reads hostile. Register must match genre, not "maximum terseness" (per HumT ACL 2025: humanizing and de-humanizing both have user-preference costs).
3. **Mechanical synonym rotation.** delve→explore everywhere creates a new pattern; vary the *syntax*, not just the word (per JHU 2025 fingerprint logic).
4. **Forbidden-word superstition.** Do not purge "crucial" from a paragraph about a crucial factor. Density is the signal (Ground Rule 6).
5. **Specificity theater.** Invented details to "sound human" are worse than abstraction — they are hallucinations. Ask, never invent (per Ground Rule 5).
6. **Voice laundering.** If the output reads like a generic good writer rather than *this* author, partially revert (per Ground Rule 4).

**Stop conditions (do not humanize further):** support macros, safety/medical/financial notices, user-requested assistant register, genre-mandated formality, or any context where HumT findings say users prefer the neutral machine voice. When in doubt, ask the user once, then respect the answer.

## 9. Assets

- `assets/lexical-tells.md` — era-stratified English AI word list (2023 / 2024 delve / 2025 core-modern / 2026 watchlist) with evidence tiers
- `assets/signs-patterns.md` — 35-pattern checklist condensed from Wikipedia "Signs of AI writing" + blader/humanizer patterns
- `assets/thinking-leakage.md` — CoT/agent-trace pattern library (regex + example + fix)
- `assets/qc-rubric.md` — final scoring rubric, loop protocol, HumT stop conditions

## 10. Worked Micro-Example

Input (38 words):

> Alright, so let me explore this. In today's fast-paced world, teams need clarity, alignment, and synergy. Wait, that's too abstract. Delving into these dynamics is crucial, as it underscores the path forward.

**Stage 1** — leakage: 2 ("Alright, so let me explore this", "Wait, that's too abstract"); hollow rhetoric: 2 (empty opener, elevation frame); template syntax: 1 (forced triad); lexical tells: 4 ("fast-paced", "Delving", "crucial", "underscores"). Dominant: **thinking leakage**.

**Stage 2** — delete "In today's fast-paced world" and "as it underscores the path forward"; trim the triad to the one item that carries meaning.

**Stage 4** (run early because leakage dominates) — remove both reasoning residues. They are the model's process, not the reader's content.

**Stage 3** (re-diagnose → hollow rhetoric dominant → compression + stance) — force a claim with a subject, verb, and stake; queue a specificity question.

**Stage 5** — fact ledger empty (no numbers/names), thresholds re-checked, report emitted.

Output: "Your team needs clearer priorities." + open question: *which team, and clearer about what?*

Note what did NOT happen: no synonym swap of "delving" → "exploring". The clause was deleted because it did no work — mechanical rotation would leave the fingerprint intact (per Stage 3 lexical strategy; per JHU 2025).

## Sources

- Kobak et al., delving into excess vocabulary, arXiv 2406.07016; Science Advances 2025 — science.org/doi/10.1126/sciadv.adt3813
- The Verge / Max Planck, "You sound like ChatGPT" (280k academic YouTube videos) — theverge.com/openai/686748
- Washington Post, 328,744 gpt-4o messages vocabulary drift (2025) — washingtonpost.com/technology/interactive/2025/how-detect-chatgpt-em-dash/
- GPTZero, perplexity & burstiness — gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup, est. 2023-12) — en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- blader/humanizer skill (35 patterns, two-pass) — github.com/blader/humanizer
- DeepSeek-R1 paper — arxiv.org/abs/2501.12948; DeepSeek-R1 Thoughtology — arxiv.org/abs/2504.07128
- Surface-cue reasoning markers — arxiv.org/abs/2605.28305; Anthropic, "Reasoning models don't always say what they think" (2025) — anthropic.com/research/reasoning-models-dont-say-think
- Visual Sketchpad — arxiv.org/abs/2406.09403; VS Code 1.109 thinking-render — heise.de/en/news/Visual-Studio-Code-1-109-Watch-AI-Models-Think-11166499.html
- scanaislop/aislop linter — github.com/scanaislop/aislop; claude-code comment issue — github.com/anthropics/claude-code/issues/85130
- Rivera Soto et al., JHU 2025, style fingerprints survive humanizing — arxiv.org/abs/2505.14608
- Sadasivan et al. 2023, detection unreliability; Liang et al. 2023, non-native false positives — sciencedirect.com/science/article/pii/S2666389923001307
- Cheng, Yu & Jurafsky, HumT, ACL 2025 — arxiv.org/abs/2502.13259; Wang et al., human detection ceiling — arxiv.org/abs/2502.11614
- Sam Kriss, NYT Magazine (2025-12-03) — nytimes.com/2025/12/03/magazine/chatbot-writing-style.html
- Em-dash density study — arxiv.org/abs/2608.05889; Ransomnews, "tells expire in ~18 months" (2026-08-21)
- Our 108-corpus experiment (9 model tiers × 4 prompts × 3 runs, Chinese; directionally applied) — see experiment/EXPERIMENT-NOTES.md
