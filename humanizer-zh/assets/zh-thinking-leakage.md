# zh-thinking-leakage — 思维链/Agent 泄露 pattern 库（Stage 4 清洗用）

配 humanizer-zh 主流程使用，是本 skill 最严格的一层。背景：思考本身已成被
设计过的文风产品（"Thought for X seconds"既是 UI 文案也是文体），AI 味正从
"答案的风格"迁移到"过程的痕迹"——第一代怕你看出它是 AI，这一代把草稿纸摆上
桌面，用户看得见、复制粘贴挡不住【研03】。产品级泄露已有实锤（GitLab Duo
work item #2437："Qwen (reasoning) models leak reasoning content into final
answer"；lettabot issue #530："Reasoning/thinking text leaks into cron job
delivery responses"）【研03】。

**总规则**：命中即清，不适用删除测试（过程痕迹对读者信息量为零）。先过豁免
判定：教学展示推理、复盘文档、调试日志等用户明确要"过程"的文体 → 标注
"过程记录"后保留，不计入泄露分。

---

## X1 推理自我修正混入正文

- **正则**：`(?i)\bwait\b[，,。!！]`、`等等[，,]`、`让我(再)?想(一)?想`、
  `我重新(看|审视)了一下`、`刚才(说的|讲得?)(不对|有误)`、`(?i)aha moment`、
  `让我重新组织`。
- **真实案例**："Wait, wait. Wait. That's an aha moment I can flag here."
  ——DeepSeek R1 论文 Table 3 原样收录的中间版 R1-Zero 输出，官方把这类自我
  修正当成果展示【研03；arXiv 2501.12948】。
- **依据**："Wait/hmm/Alternatively"已扩散为跨模型拟人标记，2026-05 论文
  证明这些标记是**表面线索而非真实反思**（压制后多数场景不掉点）【研03；
  arXiv 2605.28305】。QwQ 官方模型卡也承认"Recursive Reasoning Loops：环形
  推理导致冗长无结论的回答"【研03】。
- **清法**：删修正过程，只留修正后的最终表述；正文里不保留"我之前以为…
  后来发现…"的往返（用户要求展示推理的复盘文体除外）。

## X2 UI 残留（思考摘要/用时标记）

- **正则**：`已深度思考[（(]用时[^）)]{1,12}[）)]`、`(深度)?思考用时`、
  `已思考`、`(?i)thought for \d+ ?(seconds?|s)`、`思考完毕`。
- **真实案例**：一道语文试卷的阅读材料**原样保留了"已深度思考（用时 7.41
  秒）"界面文字**——思考痕迹进入正式出版物的中文实锤【研03；21世纪教育网
  组卷页 zujuan.21cnjy.com/question/detail/62760693】。
- **依据**：OpenAI o1 把思维链定义为 hidden CoT，产品上以"Thought for X
  seconds"摘要呈现，且摘要文风被刻意拟人化（"OK""hm""I'm curious about"）
 【研03；o1 模型卡，Simon Willison 摘录】。
- **清法**：整块删（含"用时 X 秒"数字——它是 UI 痕迹不是内容事实，是
  SKILL.md 红线2 的唯一豁免类型）。

## X3 agent 过程独白（"我现在将…"式会话痕迹）

- **正则**：`我现在(将|开始|来)`、`接下来我将`、`让我(们)?(先|来|一步步)`、
  `第[一二三四五1-5]步[，,]`（正文级叙述）、`我(首先|然后|最后)`。
- **依据与诚实标注**：交付文档残留"I will now…"式痕迹的**直接公开案例在
  研究档案中标注为空白**，只有间接证据（HN"会话该不该进 commit"讨论）
 【研03 C 节】——判定从严但不扩大化：标准是"读者需要知道这个过程吗"，
  不需要即清。
- **清法**：过程叙述整段移出交付文；若过程本身是内容（教程步骤），改写为
  面向读者的祈使/说明语态，删第一人称工作流叙述。

## X4 任务清单 checkbox 混入交付文

- **正则**：`^[-*+]\s*\[[ xX]\]`（多行模式）、`✅|⬜|◻️`。
- **依据**：checkbox 是 agent 的任务工作记忆，不是交付内容【研03·agent
  痕迹框架】。
- **清法**：整块移出（移入工作附录或删）；用户明确要求"保留待办"的除外。

## X5 给自己思考用的图表（Mermaid/流程图/提纲图被当插图）

- **正则/标记**：` ```mermaid ` 代码块、`(?i)^\s*(flowchart|graph)\s+(TD|LR)`、
  提纲式节点图（每节点为章节名/关键词无数据）。
- **依据（双层）**：①画图是模型的认知工具——Visual Sketchpad 让多模态模型
  推理时给自己画草稿，数学任务平均提升约 12.7%：图是画给自己的，不是给
  读者的输出【研03；arXiv 2406.09403】；②产品开始把思考期的图直接展示给
  用户——VS Code 1.109 把思考期 Mermaid 渲染进聊天界面（heise 标题
  "Watch AI Models Think"）【研03】。于是出现新载体：**给模型的草稿图被
  当成给读者的插图**——图里不是结论，是它组织思路的过程【研03 D 节】。
- **判定**：图内容是"组织思路的过程"（提纲图、验算图、无数据的决策流程）
  还是"给读者的结论"（含数据/对比/结论）。前者删或降级为附录。
- **附带视觉指纹**（PPT/网页交付时同查）：紫蓝渐变、圆角卡片阵列、无关
  emoji、万能三栏【研03 D 节；vibecoded-design-tells】。

## X6 代码交付物里的叙述性注释

- **正则**：`//\s*(现在|接下来|这里我们|我们先|首先|如前所述)`、
  `#\s*(现在|接下来|这里我们)`、注释中的开发史（"修复了…""上次改的…"）。
- **真实案例**：用户正式要求 Claude Code 默认不把开发历史写进注释——
  "Keep development history out of code comments/docstrings by default
  (put it in git, not the file)"（anthropics/claude-code issue #85130）
 【研03】。
- **依据**：现象普遍到需要工具治理——scanaislop/aislop linter 自述
  "Catch the slop AI coding agents leave in your code: narrative comments,
  swallowed exceptions…"（50+ 规则/8 语言）【研03】。注释甚至成为人机双向
  信道，智能体顺手更新人写给它的注释【研03·HN 讨论】。
- **清法**：删叙述性/开发史注释，保留"是什么"的功能性注释；开发史进
  commit message 或 git，不进文件。

## X7 讨好型元话语与对话残留

- **正则**：`好的[，,]下面是`、`当然可以[，,。]`、这是一个`?非常好?的问题`、
  `你刚刚那句话`、`我帮你轻轻(拧|改)一下`。
- **真实案例**："你刚刚那句话其实已经很接近一句总结式表达了，我帮你轻轻拧
  一下，不改你意思。"（V2EX【研02】）
- **依据**：sycophancy 是偏好数据实证奖励出的行为【Sharma 等 2023，研05】；
  谄媚残留清单见 tb-deai-style L1。
- **清法**：整句删；交付文只保留交付内容。

## X8 内心戏/草稿纸当内容（中文互联网特有变体）

- **标记**：思维链"内心戏"片段被复制进正文当金句/人设；自称模型昵称、
  "我先去吃饭了"式草稿语言。
- **真实案例**：DeepSeek 思维链"内心戏"刷屏（话题号称约 50 亿浏览）、思考中
  "偷偷给用户取外号"事件、衍生"鲸鱼娘"二创 IP（"我先去吃饭了"、自称 DSH、
  "蓝色大肥鱼"）【研03；今日头条/新浪/17173 报道】。官方定性：**"不是觉醒，
  是草稿纸"**【研03】。
- **安全侧旁证**：2026 年 thinking 可见性已成安全问题——"Agentic
  Blabbering"把暴露的冗长推理武器化为钓鱼话术；《Thinking Is Not Telling》
  系统研究 agent 思维信息披露风险【研03；arXiv 2602.07796】。
- **清法**：正文里的"内心戏"段落按草稿处理：删；确有金句价值的内容由作者
  重写为成稿语言（不再是"偷偷说"的口吻）。

---

## 出处

- 【研03】post/inputs/ai-flavor/research/03-cot-leakage-and-agents.md（本库
  主体证据：R1 Table 3 原句、o1 hidden CoT、试卷 7.41 秒案例、GitLab Duo
  #2437、lettabot #530、QwQ 模型卡、内心戏刷屏与"草稿纸"定性、claude-code
  #85130、aislop、Sketchpad、VS Code Mermaid、Agentic Blabbering、"I will
  now"案例空白标注）
- 【研02】post/inputs/ai-flavor/research/02-chinese-vs-english.md（V2EX 讨好型
  元话语原句）
- 【研05】post/inputs/ai-flavor/research/05-related-work.md（Sharma 等
  sycophancy 实证、Thoughtology 思考痕迹分类学）
- DeepSeek R1：arxiv.org/abs/2501.12948
- o1 模型卡摘录：simonwillison.net/2024/Sep/12/openai-o1/
- 表面线索研究：arxiv.org/abs/2605.28305
- 试卷案例：zujuan.21cnjy.com/question/detail/62760693
- lettabot：github.com/letta-ai/lettabot/issues/530
- claude-code：github.com/anthropics/claude-code/issues/85130
- aislop：github.com/scanaislop/aislop
- Visual Sketchpad：arxiv.org/abs/2406.09403
- heise（VS Code 思考可视化）：heise.de/en/news/Visual-Studio-Code-1-109-Watch-AI-Models-Think-11166499.html
- Thinking Is Not Telling：arxiv.org/abs/2602.07796
- 内心戏报道样例：toutiao.com/article/7679996069765399067/；
  sina.cn/news/detail/5330363740064061.html
