# Thinking Leakage — CoT / Agent Trace Pattern Library

Reference asset for `humanizer-en` Stage 4 TRACE-WASH. The skill's specialty and its zero-tolerance zone.

**Why this category exists.** Reasoning models productized the draft: o1 shows "Thought for X seconds" summaries deliberately humanized ("OK", "hm", "I'm curious about" — per o1 model card 2024-09 and Lifehacker's observation); R1's celebrated "Wait, wait. Wait." aha-moment was published *as a feature* (per arXiv 2501.12948). These markers are surface cues, not genuine reflection — suppressing them does not degrade the answer (per arXiv 2605.28305) — so strip them without guilt. The taxonomy of traces: self-verification, hesitation markers, tangents, "aha" narration (per DeepSeek-R1 Thoughtology, arXiv 2504.07128). CoTs are also frequently unfaithful to the model's actual computation (per Anthropic 2025, "Reasoning models don't always say what they think" — and unfaithful CoTs run *longer*), which means leaked traces add length while proving nothing.

**Policy: groups A, B, C, E are zero-tolerance.** One surviving instance fails Stage 4. Group D takes the judgment test. Regexes are ECMAScript-flavor, case-insensitive unless noted; apply multiline (`^` = line start).

## A. Reasoning-Model Residue in Prose — zero tolerance

| ID | Regex | Example hit | Fix |
|---|---|---|---|
| A1 | /^\s*(Wait,?\s*)+/i | "Wait, that contradicts the earlier point." | Delete the marker; keep the corrected claim if it stands alone |
| A2 | /^\s*(Wait,?\s*){2,}wait\.?/i | "Wait, wait. Wait. Is that right?" | Delete entire line — pure process |
| A3 | /^\s*(Hmm+|Hm,|Ah,|Oh,|OK,|Okay,)\s/i | "Hmm, let me reconsider the numbers." | Delete marker + self-talk; keep any corrected content |
| A4 | /^\s*(Alternatively|Or maybe|But then again),/i | "Alternatively, we could frame it as…" | Pick the surviving option; delete the option-weighing |
| A5 | /^\s*Let me (check|verify|think|reconsider|try|see|make sure)/i | "Let me check whether that total is right." | Delete; if verification changed an answer, state the final answer only |
| A6 | /\b(That was (wrong|incorrect)|That doesn't seem right|Scratch that|On (second|further) thought)\b/i | "That was wrong — the 2019 figure is the right one." | Keep final fact ("The 2019 figure…"); delete the retraction theater |
| A7 | self-correction pair detection (manual): claim … negation … re-claim | "Revenue doubled. Actually, that's the 2021 number. Revenue tripled." | Keep "Revenue tripled." Delete both earlier beats |
| A8 | hedging cascade rehearsing option-weighing | "It could be X, though it might be Y, so perhaps the best framing is…" | Decide; state one claim, one hedge max |
| A9 | /\b(aha moment|that's the key insight|now I see)\b/i | "That's an aha moment I can flag here." | Delete; narrate discoveries for the reader, not to the reader |
| A10 | /^\s*(First|Second|Third),? (let me|I need to|I should) /i | "First, let me analyze the dataset." | Delete; the analysis result belongs in the text, not the plan to analyze |

Basis: R1 paper Table 3 (arXiv 2501.12948); Thoughtology taxonomy (arXiv 2504.07128); surface-cue finding (arXiv 2605.28305); product leakage precedents: GitLab Duo work item #2437 (reasoning content leaking into final answers), lettabot issue #530 (thinking text leaking into cron deliveries).

## B. Agent Narrative in Deliverables — zero tolerance

| ID | Regex | Example hit | Fix |
|---|---|---|---|
| B1 | /\bI (will now|'ll now|am going to|am about to)\b/i | "I will now generate the summary." | Delete sentence; deliver the summary |
| B2 | /^\s*Let's (create|add|write|build|implement|update|remove)\b/i | "Let's create a config file." | Delete; do the thing |
| B3 | /\b(Next|Then|Now),? (I|we)'?l?l? (add|create|write|handle)\b/i | "Next, I'll handle the edge cases." | Delete from deliverables (fine in chat, fatal in documents) |
| B4 | /\b(I('ve| have) finished|The task is now complete|That concludes the (task|setup))\b/i | "I've finished the refactor." | Delete; completion state belongs to the handoff message, not the artifact |
| B5 | /^\s*[-*]\s+\[[ xX]\]/m in prose | "- [x] Draft the introduction" | Convert finished items to content; delete the checklist unless the user asked for a plan |
| B6 | /\b(TODO|FIXME|XXX):?\s*(?!.*\b(user|per )\b)/ in final docs | "TODO: refine this later" | Delete or execute; never ship scaffolding |
| B7 | /\b(As (requested|instructed)|Per your (request|instructions)|Here('s| is) the (revised|final|updated|complete) version)\b/i | "Here is the revised version:" | Delete the butler prefix; hand over the content |
| B8 | conversation meta-commentary | "Earlier you mentioned…" / "As we discussed above…" | Rewrite to stand alone: documents must survive out of chat context |

Basis: anthropics/claude-code issue #85130 ("Keep development history out of code comments… put it in git, not the file") and #65961 (verbose comments ignoring stop requests); agent-narrative category from our research/03 notes. Note honestly: a *published* case of "I will now…" surviving in a shipped document is not documented in the literature — treat this group as prevention policy grounded in adjacent evidence, not as a cited epidemic.

## C. UI / Product Residue — zero tolerance

| ID | Regex | Example hit | Fix |
|---|---|---|---|
| C1 | /^(Thought|Thinking|Reasoning) for \d+ (seconds?|minutes?|ms)\b/i | "Thought for 4 seconds" | Delete — it is UI chrome, not content (per o1 model card) |
| C2 | /已深度思考|深度思考（用时|思考过程/ | "已深度思考（用时7.41秒）" | Delete; documented surviving in a published exam reading passage (medium confidence, 21cnjy case) |
| C3 | /<(think|thinking|reasoning|scratchpad)>[\s\S]*?<\/\1>/i | raw think-block in output | Delete entire block; salvage any genuinely reader-facing conclusion |
| C4 | /^\s*(Assistant|Analysis|Thought Process|Reasoning):?\s*$/m | "Analysis:" label bar | Delete label and re-flow |
| C5 | /\b(due to (length|space) constraints|to keep this (response )?(short|brief)|my knowledge cutoff)\b/i | "Due to length constraints, only three examples…" | Delete; either include the content or cut it silently |
| C6 | /\bI (don't|do not) have (access|the ability)/i | "I don't have web access in this session." | Delete from deliverables; the constraint is chat-contextual |

Basis: o1 hidden-CoT productization (per Simon Willison's model-card excerpt, 2024-09-12; Lifehacker on humanized summary style); Chinese exam-paper case (research/03, medium confidence — cite cautiously).

## D. Model-Draft Diagrams Passed Off as Illustrations — judgment

**The test (ask of every figure):** *Does this image show the reader a conclusion, or record the process of reaching one?* Conclusions stay; process records go.

| ID | Pattern | Verdict |
|---|---|---|
| D1 | Mermaid/flowchart of "how I approached / my reasoning process / the steps I took" | cut — the model thinking on paper |
| D2 | Outline rendered as a diagram (each section a node, no information beyond the TOC) | cut or re-prose; a TOC is not a figure |
| D3 | Verification scratch work (ASCII arithmetic, double-check branches, "confirm X → yes") | cut — audibly the model checking itself |
| D4 | Decision trees mapping the model's own choices ("Should I use A or B? → B") | cut the deliberation; if the choice matters to readers, state it in one sentence |
| D5 | Reader-serving diagram (architecture the text references, decision flow the reader must execute, data chart of cited numbers) | keep — check only for blind-drawing defects |
| D6 | Decorative SVG (generic illustration adjacent to text) | usually cut — LLM SVG is drawn blind, with systematic geometry/text-overflow failures (per dev.to analysis; CVPR 2025 vector-graphics literature) |

Basis: Visual Sketchpad (NeurIPS 2024, arXiv 2406.09403) — models draw *for themselves* as cognitive tools (~12.7% math gain); VS Code 1.109 renders thinking-time Mermaid into chat (heise 2026) — tooling now actively blurs scratch paper and illustration; the "process visual residue" framing is our research synthesis (research/03 §D).

## E. Narrative Comments in Code Deliverables — zero tolerance

| ID | Regex (JS-style comments; adapt `//`→`#` for Python) | Example hit | Fix |
|---|---|---|---|
| E1 | /\/\/\s*(Now|Next|First|Then|Finally|Alright|Okay),? (let's |we |I )?(create|add|implement|fix|update|remove|write|handle)/i | "// Now let's implement the retry logic" | Delete; the code says it |
| E2 | /\/\/\s*This (fixes|addresses|handles) (the )?(issue|bug|problem)/i | "// This fixes the issue where…" | Delete — that history belongs in the commit message, not the file (per claude-code #85130) |
| E3 | changelog comments | "// v2: changed timeout to 30s" | Delete; changelogs live in CHANGELOG/git history |
| E4 | commented-out exploration dead code | "// const oldFn = …" blocks | Delete |
| E5 | swallowed exceptions with narrative excuse | "catch (e) { /* ignore for now */ }" | Handle or rethrow; never narrate the ignoring (per aislop rule set) |
| E6 | /\b(I|we) (tried|attempted|considered)\b/i in comments | "// We tried batching but it was slow" | Move the decision record to commit message / ADR; keep at most a one-line *why* if it prevents a future mistake |

Keep: interface-contract doc comments (params, invariants, gotchas a future reader needs). Test: a comment is reader-serving if it explains a constraint the code cannot express; it is process narration if it describes the writing of the code.

Basis: scanaislop/aislop linter ("Catch the slop AI coding agents leave in your code: narrative comments, swallowed exceptions…", 50+ rules, 8 languages — github.com/scanaislop/aislop); ai-slop-detect (70+ markdown/comment patterns); anthropics/claude-code issues #85130, #65961.

## Post-Wash Rules

1. Re-run groups A–C on the *whole* document after every editing round — later edits quote earlier reasoning and re-import traces.
2. If a trace carried a real correction (A6/A7), verify the surviving claim against the fact ledger before deleting the trail.
3. Log every removal in the Stage 5 report under "Trace-wash removals" (pattern ID + one-line original).

## Sources（出处）

- DeepSeek-R1 paper (Wait/aha productization) — arxiv.org/abs/2501.12948
- OpenAI o1 model card, hidden CoT & "Thought for X seconds" — simonwillison.net/2024/Sep/12/openai-o1/; Lifehacker hands-on
- Surface-cue markers (Wait/hmm/Alternatively suppressible) — arxiv.org/abs/2605.28305
- DeepSeek-R1 Thoughtology (trace taxonomy) — arxiv.org/abs/2504.07128
- Anthropic, CoT faithfulness — anthropic.com/research/reasoning-models-dont-say-think
- GitLab Duo leakage work item #2437; lettabot issue #530 — via our research/03-cot-leakage-and-agents.md
- Exam-paper UI residue case (medium confidence) — zujuan.21cnjy.com/question/detail/62760693
- anthropics/claude-code issues — github.com/anthropics/claude-code/issues/85130, /issues/65961
- scanaislop/aislop — github.com/scanaislop/aislop; ai-slop-detect (70+ patterns)
- Visual Sketchpad — arxiv.org/abs/2406.09403; VS Code 1.109 — heise.de/en/news/Visual-Studio-Code-1-109-Watch-AI-Models-Think-11166499.html
- LLM SVG "draws blind" — dev.to/usman_basheers/can-chatgpt-generate-svg-yes-but-it-draws-blind-2jo9; CVPR 2025
