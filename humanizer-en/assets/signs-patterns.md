# Signs & Patterns — 35-Pattern Checklist

Reference asset for `humanizer-en` Stages 1–3 (hollow rhetoric + template syntax categories).

**Provenance.** Condensed from Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup, created 2023-12-04, editor Chaotic Enby initiating; now ~65–78 entries with 2,000+ revisions — the most-cited AI-flavor framework in public use), as distilled into 35 rewrite patterns by the community skill blader/humanizer (Siqi Chen, repo created 2026-01-18, ~39,200 stars; NOT an Anthropic official skill — that attribution is a circulating error). This file re-organizes both sources into the skill's five diagnostic categories.

**The blader two-pass method (adopted by this skill's loop):**
- Pass 1: rewrite the passage *from memory* without looking at the original — this breaks template architecture at the root.
- Pass 2: check the rewrite against the pattern list, item by item.
Our pipeline generalizes this: Stage 2+3 ≈ pass 1, Stage 5b re-diagnosis ≈ pass 2, repeated until thresholds pass (typically 2–3 rounds).

## A. Puffery & Elevation (feeds: hollow rhetoric)

| # | Tell | Example | Fix |
|---|---|---|---|
| 1 | meaning-elevation frame | "plays a crucial role in shaping…" | delete frame; state what actually happens |
| 2 | significance inflation | "This groundbreaking study…" | cut the adjective; let the finding carry weight |
| 3 | vague importance | "In an increasingly interconnected world…" | delete opener; start with the claim |
| 4 | "testament" construction | "stands as a testament to" | folk tell, unquantified — delete as filler, don't cite as proof |
| 5 | adjective stacking on nouns | "comprehensive, robust, scalable solution" | keep the one that discriminates |
| 6 | emotional summary of a mundane fact | "This highlights the beauty of…" | name the actual consequence |

## B. Template Syntax (feeds: template syntax)

| # | Tell | Example | Fix |
|---|---|---|---|
| 7 | forced triad (near-synonyms) | "innovation, inspiration, and insights" | keep as many items as the meaning needs (Wikipedia sign #10) |
| 8 | "It's not about X, it's about Y" | "It's not about the tool; it's about the trust." | state Y directly (per Sam Kriss, NYT 2025-12) |
| 9 | not only…but also chains | "not only efficient but also elegant" | one mold per section, then restructure |
| 10 | "X isn't just Y — it's Z" | same family as 8 | collapse into one direct assertion |
| 11 | rhetorical question ladder | "But what does this mean for you?" | answer it, or delete it |
| 12 | "Enter X" / "Meet X" / "Say hello to X" | "Enter the vector database." | name the thing plainly |
| 13 | rule-of-three paragraphs (every paragraph exactly 3 sentences) | — | vary paragraph shape; merge or split |
| 14 | topic-sentence + 3 supports + mini-conclusion (uniform block shape) | — | let one support run long, cut another |
| 15 | em dash as universal connector | "X — which matters — because Y" | split the sentence; keep ≤ 1 deliberate em dash per page |
| 16 | colon-reveal template | "The answer is simple: X" | fold into normal syntax |
| 17 | "In a world where…" opener | — | delete; start in scene |

## C. Rhythm & Flow Tics (feeds: template syntax + sentence CV)

| # | Tell | Example | Fix |
|---|---|---|---|
| 18 | uniform sentence length (low burstiness) | every sentence 18–24 words | target CV ≥ 0.45; one ≤6-word sentence per 300 words (per GPTZero burstiness) |
| 19 | connector chains at line starts | Moreover… Furthermore… Additionally… | rotate or drop; let juxtaposition work |
| 20 | "First… Second… Third… Finally" scaffolding left visible | — | keep only where sequence IS the content |
| 21 | every paragraph opening with a transition | "However, the results…" | vary openings; some paragraphs can just start |
| 22 | summary tail restating the intro | "In conclusion, we have seen…" | delete; the reader finished it already |

## D. Structural Scaffolding (feeds: hollow rhetoric + register mismatch)

| # | Tell | Example | Fix |
|---|---|---|---|
| 23 | essay-outline meta-narration | "In this article, we will explore three aspects…" | delete; write the aspects |
| 24 | fake balanced "perspectives" | "Some argue X, while others believe Y" | name who argues, or take a side |
| 25 | vague attribution | "Experts agree that…" | cite the expert or drop the claim |
| 26 | universalized "you" in technical docs | "You might be wondering…" | match genre register; docs ≠ newsletter |
| 27 | listicle where prose belongs | "5 key takeaways:" in an essay | re-prose, keep lists where genre wants them |
| 28 | hollow closing invitation | "The possibilities are endless." | end on the strongest concrete fact |

## E. Rhetorical Moves (feeds: hollow rhetoric)

| # | Tell | Example | Fix |
|---|---|---|---|
| 29 | "delve/dive deep" announcement | "Let's delve into the details." | just give the details |
| 30 | metaphor without development | "a tapestry of factors" | one metaphor, developed, or none |
| 31 | synthetic earnestness | "It's not just code — it's a journey." | cut; earn sentiment or drop it (per Sam Kriss) |
| 32 | grand-history framing | "Throughout history, humans have…" | start at the specific case |
| 33 | wisdom-of-the-ages closer | "At the end of the day, what truly matters is…" | delete the homily |

## F. Conversational Residue (feeds: thinking leakage — route to Stage 4)

| # | Tell | Example | Fix |
|---|---|---|---|
| 34 | assistant-chat residue | "Certainly! Here's the revised version:" | delete the butler prefix; deliver the content |
| 35 | capability disclaimers in text | "As of my knowledge cutoff…" | remove from deliverables; verify facts instead |

## Scoring Rules

- Each table hit counts once toward its category density (per 1k words), EXCEPT folk-tier examples (#4, #30) which count half.
- #18 counts as a template-syntax hit only when CV < 0.35 (else it's the variance repair track, Stage 3).
- Category F hits always escalate to Stage 4 regardless of density (zero tolerance there).

## Sources（出处）

- Wikipedia, "Signs of AI writing", WikiProject AI Cleanup (created 2023-12-04; ~65–78 entries, 2,051 revisions) — en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- blader/humanizer (35 patterns, two-pass rewrite; repo by Siqi Chen, 2026-01-18; ~39,207★) — github.com/blader/humanizer
- GPTZero, perplexity & burstiness — gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Sam Kriss, "The Chatbot Eigenstyle" / chatbot-writing-style (NYT Magazine, 2025-12-03: "It's not X, it's Y", tapestry/liminal, "synthetic earnestness", reverse contamination) — nytimes.com/2025/12/03/magazine/chatbot-writing-style.html
- Kobak et al. style-word class — arxiv.org/abs/2406.07016; science.org/doi/10.1126/sciadv.adt3813
- Em-dash density (146k congressional press releases, 2025 doubling; exploratory) — arxiv.org/abs/2608.05889
- Corrected attribution note: blader/humanizer is third-party, not Anthropic-official (per our research/05-related-work.md fact-check table)
