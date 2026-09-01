---
name: humanizer-zh
description: |
  Generic Chinese "de-AI-flavor" pipeline for any Chinese deliverable text —
  articles, 公众号 posts, marketing copy, work documents, official prose,
  academic drafts, 朋友圈. Not the textbook-specific pair. Runs a five-stage
  loop for 2-3 rounds: Stage 1 diagnose five flavor classes per 1000 chars
  (hollow sublimation / template patterns / high-frequency words / register
  mismatch / chain-of-thought leakage) with context gating; Stage 2 subtract
  scaffolding (connector clichés, 随着…的发展 openers, 这说明 closers, forced
  triads, 不仅…而且 stacks, context-gated 赋能/抓手/闭环); Stage 3 rewrite by
  dominant flavor (DeepSeek-style lyrical → concrete detail; translationese →
  Chinese word order; register mismatch → recalibrate to the target occasion)
  plus specificity injection by asking the user, never inventing; Stage 4 —
  the signature, strictest stage — scrub chain-of-thought and agent traces
  (self-corrections like "Wait/等等让我想想", UI residue "已深度思考（用时X秒）",
  agent narration, task checkboxes, self-use Mermaid/outline diagrams,
  narrative code comments); Stage 5 final QC: facts-zero-change diff, re-score
  vs baseline, before/after report, and an honest detector disclaimer (the
  goal is human-feeling Chinese, NOT beating 朱雀/知网 — style fingerprints
  cannot be scrubbed away; Sadasivan 2023, JHU 2025). Every rule cites its
  source (research dossiers 02/03/04/05 + the 108-sample experiment,
  findings A-E). Use when a Chinese text is flagged as AI-flavored, or when
  thinking/agent traces leaked into a deliverable. Do NOT use for English
  text (use blader/humanizer), for the AI-management textbook (use
  tb-deai-style then tb-humanizer), for beating AI detectors, or for
  fact-checking.
  Chinese triggers: 去AI味、人味、人味化、deslop、去味、中文润色、AI腔、
  机器味、AI感、不像AI写的、太像AI、没有人味、思维链泄露、内心戏、
  已深度思考残留、agent痕迹、humanizer-zh。
---

# humanizer-zh — 中文去 AI 味：五阶段流水线（循环 2–3 轮）

对一份中文交付文本执行下述五阶段流水线。**一次执行去不干净**：改写动作本身
会引入新的 AI 味（模型一代比一代"味浓"【实验·发现B】；"反 AI 味的 AI 味"是
已被警告的失效模式【研05·沈志荣】），所以每轮以 Stage 1 重诊断为闭环，默认跑
2 轮、最多 3 轮。

证据锚点（全文以【】标注出处）：【研02】中文特征词表与公文腔×翻译腔、
【研03】思维链泄露与 agent 痕迹、【研04】检测失败史与 humanizer 谱系、
【研05】相关工作与署名纪律、【实验】108 篇默认输出量化（发现 A–E）。完整
词表、句式库、泄露正则、语体基线在 assets/ 四个文件中，本文件只载规则与
阈值。改写例句一律取自研究档案收录的真实例句；示意性构造句均显式标注
"构造示意"，不得当作实测样本引用。

## 0. 总纲与红线（先读，优先级高于一切手法）

1. **目标是"中文读者读起来像人写的"**，不是骗过朱雀/知网等检测器。检测分
   不是质量指标：7 款检测器把 61%+ 的非母语 TOEFL 作文误判为 AI、学生原创
   论文被知网测出 AI 率 86.8%、同文跨平台相差 32%【研04】。
2. **事实/数字/引语/出处零改动**。逐 hunk diff 自查。唯一例外：Stage 4 过程
   痕迹里的数字（如 UI 残留"用时 7.41 秒"【研03】）是待删残留，不是内容
   事实。
3. **信息密度不降**：删掉的字必须是无信息量的字；删后论证链、反例、证据一
   个不能少（同库教材前例 tb-deai-style §1 质量红线，本 skill 沿用）。
4. **不新造具体细节**：需要具体的人/数/场景时走 Stage 3 追问协议，禁止为
   "去味"编造事实性细节（tb-deai-style"数字禁新造"红线同款）。
5. **打破默认 ≠ 替换默认**【研05·沈志荣】：禁止把"删排比"做成"逢三拆二"、
   把"删套话"做成"逢句插口语词"——那是用一个新模板替换旧模板。
6. **语境门控总则**【实验·发现D】：赋能/抓手/闭环/深耕等"铁证黑话"在 108
   篇默认输出中出现 **0 次**；它们是商务/公文语境诱导出来的产物。默认输出
   真正的高频味是**抒情腔**（温柔/治愈/星辰类）与**衔接套话**（值得注意的是
   /综上类）。先判语境，再决定哪层词表全额计分（Stage 1）。

## 1. 何时用 / 何时不用（When NOT to use）

**用本 skill**：
- 任何中文交付文（文章/公众号/文案/工作文档/公文/学术/朋友圈）被反馈"AI 味
  重、机器味、太像 AI、没有人味"，或用户发布前主动要求去味；
- 推理模型/agent 工作流产出的文本，疑似混入思考痕迹、过程独白或自用图表
  （直接进 Stage 4 判定）；
- 用户说出触发词：去AI味、人味、deslop、中文润色、去味。

**不用本 skill**：
1. 英文文本 → 用 blader/humanizer（维基百科 35 模式两遍改写）【研04】；
2. AI 与管理教材项目 → 用教材专用二步对 tb-deai-style（减法）→ tb-humanizer
   （加法），见 §8 分工，不调用本 skill；
3. 目标是"降 AI 检测率/过朱雀/过知网"→ 拒绝作为目标（§7.d 声明照录）；
4. 任务是事实核验、语法纠错、或学术不端意义上的"降重"→ 不是本 skill；
5. 人类手写但"看起来像 AI"的文本 → 先告知误伤风险（小红书用户自写口播文案
   因意象"太 AI"被老板误判"机器人我不需要"【研02】；检测器系统性误伤语言
   受限者【研04】），只按用户明确指定处微调，不因"像 AI"而全文动手；
6. 已跑满 3 轮的文本 → 停手（§2 轮次预算）。

## 2. 流水线总览（每轮固定顺序）

```
Stage 1 诊断 → Stage 2 减法 → Stage 3 改写 → Stage 4 泄露清洗 → Stage 5 终检
                     ↑                                      │
                     └────────── 未达标则回到 Stage 1 ──────┘
```

| 轮次 | 动作 | 停止条件 |
|---|---|---|
| 第 1 轮 | 全量五阶段 | Stage 5 达标即停 |
| 第 2 轮 | 补漏 + 按主导味型深化 | 达标即停（多数文本停在这里） |
| 第 3 轮 | 只做 Stage 4 复扫 + Stage 5 终检，不做大改 | 无论达标与否，本轮后停手 |

理由：轮次越多，"为去味而改写"的动作本身越容易带入新味（过程叙述、新排比、
表演性口语）【研05·沈志荣】；第 3 轮只做最低侵入的清扫。

## 3. Stage 1 诊断（先判语境，再打分）

### 3.1 语境门控（第一步，必做）
判定文本语境并记录：A. 商务/公文/汇报；B. 默认创作（文章/心得/朋友圈/散文）；
C. 营销文案；D. 学术。判定依据：用户声明的目标场合优先于文本自身特征。
- 语境 A → 黑话层（赋能/抓手/闭环/深耕/聚焦…）**全额计分**【cn-humanizer
  一级词；实验·发现D：该层只在商务语境被诱导出现】；
- 语境 B/C → 黑话层命中 ≈0 属预期，**主查抒情腔层与衔接套话层**【实验·
  发现D：这才是 2026 年默认输出的主味】；
- 语境 D → 叠加"无源权威"检查（无引注的"研究表明/数据显示/专家指出"）
  【tb-deai-style L1 同款清单】。

### 3.2 五类打分（每千字，输出分表）
按 assets/zh-lexicon.md 与 assets/zh-patterns.md 逐层计数，除以千字数：
1. **空洞升华**：意义拔高词（见证/塑造/勾勒/画卷/新篇章…）+ 段尾升华句
   （让我们拭目以待/未来可期/这，就是…的力量）【cn-humanizer 宣传腔与意义
   拔高类；光明日报"正确的空话"定性，研02】；
2. **模板句式**：不仅…而且 / 不是…而是 / 随着…的发展 / 在…时代 / 首先-
   其次-最后 / 排比三连 / 四字格堆叠 / 同义词循环 / "的"字连珠 / 通过…从而 /
   在…方面【anti-vibe 五大句式；cn-humanizer 18 模式；deslop-zh 速查清单】；
3. **高频词**：四层词表命中数，黑话层按 3.1 门控加权【cn-humanizer；虎嗅；
   实验】；
4. **语体错位**：对照 assets/zh-register-map.md 的场合基线，算各类分数相对
   该场合"该有的味"的超出量。同一模型跨文体 AI 味相差 **3–8 倍**——错位
   程度才是主罪，不是绝对词频【实验·发现C】；
5. **思维链泄露**：按 assets/zh-thinking-leakage.md 正则清单计数【研03】。

### 3.3 厂牌先验（可选加速，不影响判定）
若已知生成模型，按各厂味型调整检查顺序【实验·发现E】：gemini 系→先查抒情
腔；claude 系→先查衔接套话；DeepSeek 系→先查"不是…而是"堆叠（2.05/千字
全场最高）；GLM 系→先查排比三连（3.85/千字全场最高）；关思维档→先查模板腔
（排比/套话多、抒情少，发现A 细分）。

### 3.4 输出（同时是 Stage 5 的对比基线）
(a) 语境判定；(b) 五类分表（每千字）；(c) 主导味型（最高分类）；(d) 本轮
计划（Stage 2 先删什么、Stage 3 用哪条策略、Stage 4 重点扫哪几类）。

## 4. Stage 2 减法（只删无信息量的字）

逐条扫描，命中即删；每处删除记入改写日志 {原文摘录, 命中规则, 删除理由}：

1. **衔接套话**：综上所述 / 总而言之 / 总的来说 / 值得注意的是 / 值得一提的
   是 / 需要指出的是 / 首先-其次-最后（作段落标头时）【cn-humanizer 二级
   连接词；实验·发现D：默认输出真正高频之一；简圣宇："虚假逻辑连贯性的
   装饰"，研02】。删法：只删引导词，其后实质判断保留。
2. **开场套话**：随着…的发展 / 在当今…时代 / 在…的今天 / 众所周知 /
   毋庸置疑【deslop-zh 速查清单；anti-vibe；tb-deai-style L1】。删法：整句
   删，直接从第一个实质句开始。
3. **总结尾套话**：这说明 / 可以看出 / 由此可见 / 不难看出 / 到这里
   【deslop-zh；ninehills】。删法：删套话引导词；若其后判断只是前文复述，
   连判断一起删。
4. **强行三连排比**：三要素并列若无信息分工即拆，按含义需要决定用几个
  （2 个就 2 个、5 个就 5 个）【blader/humanizer 模式#10"强行三连"，研04】。
   "不是…而是…"三连堆叠（三句实为同义反复）整组处理：保留信息量最大的
   一句，其余删【研02 伪文采排比真实样本】。
5. **"不仅…而且/同时还"堆叠**：一句两重以上递进即拆成独立判断或删弱半
   【anti-vibe 句式①；实验：关思维档该句式 1.6/千字全场最高】。
6. **意义拔高词（语境门控）**：赋能 / 助力 / 抓手 / 闭环 / 深耕 / 聚焦 /
   打造 / 见证 / 塑造 / 勾勒 / 画卷——只在语境 A 或用户点名反感时按词处理；
   语境 B 命中 ≈0，不要为删而找【实验·发现D；cn-humanizer 一级词】。若该词
   承载实义（真实项目名、既定术语），保留并记录理由。
7. **删除测试（每处删除前必做）**：删掉这句，读者获取的信息有损失吗？
   有 → 只压缩不删；无 → 删【tb-deai-style 删除测试同款】。一次删除超过
   2 句的论证性段落，降级为"建议删除 + 标 `[DEL-CHECK]` 待人工确认"，
   不直接落盘。

## 5. Stage 3 改写（按主导味型选策略）

### 5.1 味型 → 策略映射
- **抒情腔过浓**（DeepSeek 式：拓扑/克莱因瓶/睫毛/青苔/瞳仁/涟漪/温柔/治愈/
  星辰/稳稳地接住）→ **换具体细节**：对每个抽象意象问"换成可指认的人/物/
  动作/数字后是什么"。抒情腔是 2026 年默认输出的主味（gemini-3.7 达 6.9/
  千字）【虎嗅常用词总结，研02；实验·发现D】；开思维档抒情词几乎翻倍
  （3.54 vs 1.79）——含混的"诗意"要优先怀疑是推理渗入成稿【实验·发现A】。
- **翻译腔**（"在某种意义上说"/"切实推动"/万能动词 推进-实现-建构/名词化
  空动词"对…进行…"）→ **按中文语序重写**：主干前移、空动词换实动词、
  被动改主动。中文 AI 味是"公文腔×翻译腔"混合态；LLM 非英语输出带英语
  中心词汇语法模式（"带英语口音的二语学习者"）【搜狐《一眼看穿AI》；
  Apple arXiv 2410.15956；研02】。
- **语体错位** → 对照 assets/zh-register-map.md 对**目标场合**重校：朋友圈
  ≠公文≠公众号。错位才是 3–8 倍味差的来源【实验·发现C】。重校方向以场合表
  "该有的味"为准，不是把一切改口语。
- **模板腔（不思考档特征）** → 排比/套话密度高时优先恢复句长方差：长句后
  接三五字短句，破"句句结构完整的主谓宾、句长过于均衡"【简圣宇/社科报；
  实验·发现A：不思考→模板腔，多思考→抒情腔】。

### 5.2 specificity injection（追问协议，禁编造）
文本"空"的根源是缺具体的人/数/场景。执行：列出所有"可用一个具体事实替换的
抽象表述"，**向用户一次性批量追问**（例：文中"效率明显提升"，具体是哪个
环节、从多少到多少？）。用户未答复前：抽象表述原样保留，不编造数字、人名、
案例【红线4；研04·结论："去 AI 味的终极形态不是把 AI 文本改得像人，而是把
人的东西（判断、具体经验、风险承担）放进去"】。

### 5.3 改写自检（每轮 Stage 3 后必做）
- 随机抽三段问：这是"这个作者真会说的"，还是"模板生成的'人味腔'"？答不出
  区别 → 回滚该处，宁可少改【tb-humanizer 反自查同款】；
- 新引入的口语句式不得跨段复用——复用即新模板【红线5】；
- 改写中不得出现"我现在将…/接下来我们…"式过程叙述：那是 Stage 4 的清扫
  对象，而改写动作本身最容易把它带进来【研03】。

## 6. Stage 4 思维链泄露清洗（本 skill 特色，最严格）

按 assets/zh-thinking-leakage.md 的正则清单全量扫描下列七类。**命中即清，
不适用删除测试**（过程痕迹对读者信息量为零），但先过豁免判定：用户明确要求
保留思考过程的文体（教学展示推理、复盘文档、调试日志）→ 标注"过程记录"后
保留，不计入泄露分。

1. **推理自我修正混入正文**："Wait/等等，让我想想/我重新看了一下/刚才说的
   不对"式自我修正与犹豫语。依据：R1 论文把"Wait, wait. Wait. That's an aha
   moment I can flag here."原样当成果收录；"Wait/hmm/Alternatively"已扩散为
   跨模型拟人标记，且被证明是**表面线索而非真实反思**（压制后多数场景不
   掉点）【研03；R1 arXiv 2501.12948；arXiv 2605.28305】。
2. **UI 残留**："已深度思考（用时 X 秒）/深度思考完毕/Thought for X
   seconds"。实锤：一道语文试卷的阅读材料原样保留"已深度思考（用时 7.41
   秒）"【研03；21世纪教育网组卷页】。
3. **agent 过程独白**："我现在将…/第一步…第二步…/接下来我来…"写成正文的
   过程叙述。判定标准："读者需要知道这个过程吗"——不需要即清。注意：此类
   直接公开案例在研究档案中标注为空白，只有间接证据，判定从严但不扩大化
  【研03 C 节】。
4. **任务清单 checkbox 混入交付文**：`- [ ]` / `- [x]` / ✅⬜ 是 agent 的
   工作记忆不是交付内容，整块移出（用户要求"保留待办"除外）。
5. **给自己思考用的图表**：Mermaid/流程图/提纲图被当成给读者的插图。判定：
   图里是"组织思路的过程"（提纲图、验算图）还是"给读者的结论"。前者删或
   降级为附录。依据：画图是模型的认知工具（Visual Sketchpad：推理期自画
   草稿使数学任务平均提升约 12.7%——图是画给自己的）；产品已把思考期图表
   直接渲染给用户（VS Code 1.109"Watch AI Models Think"）——草稿与成稿的
   边界正在消失【研03 D 节】。
6. **代码交付物里的叙述性注释**："现在我们…/这里选择…因为…/上次修复了…"
   开发史注释。用户已正式要求"开发史进 git、不进文件"（anthropics/
   claude-code issue #85130）；现象普遍到出现专门 linter（aislop："Catch
   the slop AI coding agents leave in your code: narrative comments…"）
  【研03 C 节】。清法：删叙述，保留"是什么"的功能性注释。
7. **讨好型元话语与对话残留**："你刚刚那句话其实已经很接近一句总结式表达
   了，我帮你轻轻拧一下，不改你意思。"（V2EX 实例）【研02】；"好的，下面
   是…/当然可以/这是一个非常好的问题"【tb-deai-style L1 谄媚残留清单】。
   交付文里只保留交付内容。

## 7. Stage 5 终检（四项全过才交稿）

a. **事实零改动 diff**：逐 hunk 对比改写前后，数字/引语/出处/案例事实一字
   不动；任何疑似必要的事实级改动，标 `[NUM-CHECK]` 转人工，不落盘【红线2；
   tb-deai-style `[NUM-CHECK]` 通道同款】。
b. **重跑 Stage 1**：输出前后对比分表。达标线（方向性指标，绝对值仅参考
  【实验·局限：n=3/格、社区词表非金标准】）：
   - 总标记词 ≤ 4.0/千字（实验最淡档：glm-5.3 为 3.70、关思维档 3.96）；
   - 主导味型类降幅 ≥ 60%；
   - 五类中无一类 > 1.5/千字；
   - 语体错位类：以"不超出目标场合基线"为准，不用绝对值【实验·发现C】。
   未达标 → 回 Stage 1 进入下一轮（遵守 §2 轮次预算；第 3 轮后无条件停）。
c. **before/after 报告**：轮次记录、各类分数对比、删除统计（按规则分组
   计数）、`[DEL-CHECK]`/`[NUM-CHECK]` 清单、豁免清单。报告用平实中文写；
   报告本身不得出现本 skill 清扫的套话、排比与升华——报告是门面。
d. **声明（附在报告末尾，原文照录）**：
   > 本 skill 的目标是让中文读者读起来像人写的，不是骗过朱雀、知网等 AI
   > 检测器。改写攻击可使检测器趋于随机（Sadasivan 等 2023《Can AI-
   > Generated Text be Reliably Detected?》）；且 humanizer 洗不掉风格
   > 指纹——few-shot 风格检测器仍能识别改写后的文本（Rivera Soto 等，
   > JHU，2025，arXiv 2505.14608）。检测分数不是质量指标。

**HumT 停手规则（何时不要继续"人味化"）**：用户并非总想要"像人"——Stanford
HumT 研究发现许多场景用户反而更不喜欢拟人化输出，拟人语气还关联温暖、女性
气质、低地位等社会感知【Cheng, Yu & Jurafsky，ACL 2025，arXiv 2502.13259；
研04】。以下三条任一成立即停手并向用户说明：功能文体（API 文档/法律/规范
公文）；用户未抱怨 AI 味；第 3 轮边际降幅 < 10%。

## 8. 与 tb-deai-style / tb-humanizer 的分工（防重复劳动）

| | tb-deai-style + tb-humanizer | humanizer-zh（本 skill） |
|---|---|---|
| 对象 | AI 与管理教材（专库专用） | 任意中文交付文（通用） |
| 结构 | 二步对：先减法、再注入作者人味 | 五阶段循环流水线 |
| 语料锚 | 教材作者语料三档案 | ai-flavor 研究四档案 + 108 篇实验 |
| 特色 | 密度账本、作者人格三词诀 | 思维链泄露清洗（Stage 4）、语境门控 |
| 优先级 | 教材项目内优先 | 教材项目**不得**调用本 skill |

两把刀不叠跑：通用稿件若属教材项目，标 `[DEAI-RESIDUE]` 退回教材二步对
处理，不在本 skill 内顺手改，防止互相覆盖产出【tb-humanizer §1 同款原则】。

## Sources

研究档案（本 skill 证据基础；路径相对 post/inputs/ai-flavor/）：
- research/02-chinese-vs-english.md — 中文特征词表/句式/公文腔×翻译腔
- research/03-cot-leakage-and-agents.md — 思维链泄露/agent 痕迹/自用图
- research/04-detection-and-humanizer.md — 检测失败史/humanizer 谱系/HumT
- research/05-related-work.md — 相关工作与署名纪律
- experiment/EXPERIMENT-NOTES.md、experiment/findings.md — 108 篇实验（发现 A–E）

外部来源：
- cn-humanizer 词表：github.com/0xtresser/cn-humanizer
- anti-vibe-writing 中文模式库：github.com/weijt606/anti-vibe-writing
- blader/humanizer：github.com/blader/humanizer
- deslop-zh：github.com/ninehills/public-skills
- 虎嗅 DeepSeek 味常用词：163.com/dy/article/K3BNBNUQ051188EA.html
- 光明日报"AI 新八股"（刘明华）：epaper.gmw.cn/gmrb/html/content/202605/17/content_13811.html
- 简圣宇（中国社会科学报）：cssn.cn/skgz/bwyc/202607/t20260703_6057355.shtml
- 搜狐《一眼看穿AI》：sohu.com/a/1014931596_523187
- DeepSeek R1 论文：arxiv.org/abs/2501.12948
- OpenAI o1 hidden CoT（Simon Willison 摘录）：simonwillison.net/2024/Sep/12/openai-o1/
- "Wait"类标记为表面线索：arxiv.org/abs/2605.28305
- 试卷"已深度思考（用时7.41秒）"案例：zujuan.21cnjy.com/question/detail/62760693
- lettabot 思考泄露 issue：github.com/letta-ai/lettabot/issues/530
- GitLab Duo 泄露 issue（work item #2437）：gitlab.com/gitlab-org/modelops
- claude-code 开发史注释 issue：github.com/anthropics/claude-code/issues/85130
- aislop linter：github.com/scanaislop/aislop
- Visual Sketchpad：arxiv.org/abs/2406.09403
- VS Code 思考可视化（heise）：heise.de/en/news/Visual-Studio-Code-1-109-Watch-AI-Models-Think-11166499.html
- Apple《Do LLMs Have an English Accent?》：arxiv.org/abs/2410.15956
- Sadasivan 等 2023：arxiv.org/abs/2303.11150
- JHU humanizer 边界（Rivera Soto 等）：arxiv.org/abs/2505.14608
- Stanford HumT（Cheng, Yu & Jurafsky）：arxiv.org/abs/2502.13259
- 教材前例：ning-embodied-knowledge 库 skills/owned/tb-deai-style、tb-humanizer
