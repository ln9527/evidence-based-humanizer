# Lexical Tells — Era-Stratified English AI Word List

Reference asset for `humanizer-en` Stage 1 (lexical tells category) and Stage 3 (substitution strategy).
Count hits per 1,000 words. Density is the signal; a single hit is not (per our 108-corpus experiment, Finding D: perceived AI flavor = model default register + repetition, not exotic tokens).

## How to Use This List

1. **Score by tier.** Quantified-tier hits weigh full; community-tier hits weigh half; folk-tier hits weigh zero for diagnosis (they may still be deleted in Stage 2 as hollow rhetoric — but never cited as "evidence of AI").
2. **Adjust for era decay.** Tells expire: a word's spike burns out roughly 18 months after it becomes famous, because vendors retrain against it (per Ransomnews 2026-08-21, 21,442 arXiv abstracts: delve −94% from its 2024 peak; per headcore.digital 2026 rotation model; per WaPo 2025: delve already declining in 328,744 gpt-4o messages). A 2023-era tell surviving in a 2026 text is more likely a human imitating AI — or a stale humanizer at work.
3. **Account for reverse contamination.** Humans have absorbed delve, tapestry, and prowess into spontaneous speech (per Max Planck / The Verge 2025-06-20: meticulous/delve/realm/adept up to +51% in human academic YouTube scripts). Lexical tells alone never prove machine authorship; never accuse, only clean.
4. **Never bulk find-replace.** Substitute only where the word does no work (per JHU 2025 fingerprint finding — mechanical rotation changes the signature, not the fingerprint; per shuorenhua: no mechanical synonym swaps).

## Era 1 — 2023: Assistant Residue & Hollow Fluency

The first generation: RLHF-safe "correct nonsense", LinkedIn register, refusal boilerhead. (per The Atlantic 2023-04 "LinkedIn voice"; per The Verge 2023-04-25 on "as an AI language model" contaminating reviews and papers; per Ted Chiang's blurry-JPEG New Yorker 2023-02-09.)

| Tier | Tell | Notes |
|---|---|---|
| Q | as an AI language model | the 2023 signature; The Verge documented it in spam reviews, fake papers, court filings |
| Q | I'm sorry, but I cannot / I cannot fulfill this request | refusal residue; RLHF safety formatting |
| C | It's important to note that / It's worth noting that | empty authority projector |
| C | In today's fast-paced world / In the digital age / In an era of | hollow opener frame |
| C | unlock the potential / game-changer / revolutionize / take it to the next level | LinkedIn elevation class |
| C | Moreover, / Furthermore, / Additionally, (chained at line starts) | connector chain |
| C | Let's dive in! / Let's explore | reader-command opener |

## Era 2 — 2024: The Delve Era (quantified)

The quantified core. Kobak et al. measured 15M PubMed abstracts (2010–2024): excess vocabulary appears abruptly after ChatGPT's release; ≥13.5% of 2024 abstracts LLM-processed; 45.2% of excess words are *style* words, not content words (arXiv 2406.07016; Science Advances 2025, science.org/doi/10.1126/sciadv.adt3813).

| Tier | Tell | Quantified excess |
|---|---|---|
| Q | delves / delving into | 28× baseline (Kobak) |
| Q | underscores | 13.8× (Kobak) |
| Q | showcasing | 10.7× (Kobak) |
| Q | potential, findings, crucial | top overused *common* words; potential δ=0.052 (Kobak) |
| Q | intricate, notably, comprehensive, meticulous | style-word class; meticulous also Max Planck +51% class |
| M | realm, adept | Max Planck human-contamination class — weak as AI evidence, still AI-flavored in prose |
| M | tapestry, prowess | spread into human speech (Max Planck); weakly quantified — treat as flavor, not proof |
| F | testament (stands as a testament to), boast | **zero systematic quantification** (Kobak: zero occurrences) — folk tells; delete as hollow rhetoric, never diagnose on them |

Max Planck nuance worth remembering: bolster, unearth, and nuance *declined* in human speech post-ChatGPT — a reminder that not every "fancy word" story points the same direction.

## Era 3 — 2025: The core/modern Era

Vocabulary drift measured on 328,744 gpt-4o messages (2024-05 → 2025-07): delve collapsing, **core ~5× and modern >8% relative growth** (per Washington Post 2025 interactive). Simultaneously: sycophantic openers become cross-vendor tics, and the em dash doubles in formal prose (per arXiv 2608.05889: congressional press-release em-dash density 0.10–0.12 → 0.217 per 1k chars in 2025; exploratory, medium confidence).

| Tier | Tell | Notes |
|---|---|---|
| Q | core (as intensifier: "core principle", "at its core") | WaPo ×5 |
| Q | modern ("a modern approach") | WaPo >8% |
| C | robust, seamless, leverage (v.), harness, foster, elevate, embark on, navigate (metaphorical), unlock, pivotal, paramount, landscape (fig.), journey (fig.), dive deep, unpack, demystify, streamline, supercharge | GPTZero AI Vocabulary universe (top-50 list, updated monthly since 2024-10) + community consensus; density matters |
| Q | You're absolutely right / Great question | sycophantic openers (per anthropics/claude-code issue #3382; per GPT-4o sycophancy rollback, OpenAI 2025-04-28) — conversational, but leak into prose leads |
| Q | em dash as universal connector (3+ per 1k words) | punctuation tell; one deliberate em dash is human, a house style of them is the machine |

## Era 4 — 2026 Watchlist

The reasoning-model generation. Its tells are not vocabulary but *process residue* — words that mark the model thinking at the reader. These belong primarily to Stage 4 TRACE-WASH (see `thinking-leakage.md`); listed here because they surface as lexical hits first.

| Tier | Tell | Notes |
|---|---|---|
| Q | Wait, / Hmm, / Alternatively, (sentence-initial) | R1-style reasoning markers (per R1 paper arXiv 2501.12948; per arXiv 2605.28305: surface cues, not real reflection — safe to strip) |
| Q | Thought for X seconds | UI chrome pasted as prose (per OpenAI o1 model card 2024-09) |
| Q | Let me check / Let me verify / On second thought | self-monitoring narration |
| C | I will now… / Here is the revised version | agent narrative leaking into deliverables |
| C | whatever replaces core/modern next | per the 18-month expiry law: re-baseline this list against GPTZero AI Vocabulary (monthly) and Wikipedia "Signs of AI writing" (continuously revised, 2,000+ revisions) before heavy use |

## Diagnosis Quick Rule

```
lexical-tell density = (Q hits + 0.5 × C hits) / words × 1000
```

- ≥ 2.0/1k → fail Stage 5b gate; run Stage 3 lexical strategy.
- 1.0–2.0/1k → acceptable; check concentration (all hits in one section = template paragraph, fix locally).
- < 1.0/1k → pass; do not touch remaining hits individually (Ground Rule 6: density beats presence).

## Sources（出处）

- Kobak et al., "Delving into ChatGPT usage in academic writing through excess vocabulary" — arxiv.org/abs/2406.07016; Science Advances 2025 — science.org/doi/10.1126/sciadv.adt3813
- Max Planck / The Verge, "You sound like ChatGPT" (~280k academic YouTube videos) — theverge.com/openai/686748
- Washington Post, "How to detect ChatGPT's em dash" (328,744 gpt-4o messages) — washingtonpost.com/technology/interactive/2025/how-detect-chatgpt-em-dash/
- GPTZero AI Vocabulary (top-50 AI words, monthly updates since 2024-10) — gptzero.me
- GPTZero, perplexity & burstiness — gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Wikipedia, "Signs of AI writing" (WikiProject AI Cleanup, est. 2023-12) — en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- The Verge on "as an AI language model" (2023-04-25) — theverge.com/2023/4/25/23697218
- The Atlantic on LinkedIn-voice AI prose (2023-04) — theatlantic.com/technology/archive/2023/04/ai-chatbots-llm-text-generator-information-credibility/673841/
- Ted Chiang, "ChatGPT Is a Blurry JPEG of the Web" — newyorker.com/tech/annals-of-technology/chatgpt-is-a-blurry-jpeg-of-the-web
- Ransomnews, AI tells ~18-month expiry (2026-08-21, 21,442 arXiv abstracts); headcore.digital era-rotation model (2026)
- Em-dash density study — arxiv.org/abs/2608.05889
- anthropics/claude-code issue #3382 ("You're absolutely right"); OpenAI GPT-4o sycophancy rollback — openai.com/index/sycophancy-in-gpt-4o/
- Our 108-corpus experiment — ../../experiment/EXPERIMENT-NOTES.md
