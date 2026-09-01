# 研究笔记 05｜相关工作定位（Prior Art）：四根柱子，别人都提出过什么

> 研究执行：7 个联网研究子智能体按柱子穷举，2026-08-31。
> 用途：确保文章诚实定位——哪些观点是别人的（必须给署名），哪些是我们的增量（可以主张）。
> 结论先行：**四根柱子的"零件"都有先行者；但三个"组装件"是本文增量**（三阶段机制分期、中文量化实验、思维开关对照+分型×工具矩阵）。

---

## 〇、重要更正（成文时必须避免的错误）

| 传言 | 核查结果 |
|---|---|
| Colin Fraser《ESCAPING PICKLE RANCH》分析AI文风 | **查无此文**（HN/Bing/DuckDuckGo/Wayback/作者Medium全集均无）。真身是 Fraser 2023-01-30《ChatGPT: Automatic, Expensive BS at Scale》——引用请用真身 |
| NYT 有 "Bot or Not" 测验 | 实际是 NYT 2026-03-09 交互测验《Who's a Better Writer: A.I. or Humans?》（54% 读者偏好 AI 文段） |
| "讣告里 delve 研究" | 不存在研究，只有 Futurism 等媒体报道 |
| Anthropic 官方 humanizer skill | 不存在；爆款 blader/humanizer 是第三方（Siqi Chen，2026-01-18 建仓） |

---

## 一、支柱①谱系变迁：零件全有先例，三阶段分期无先例

### 已有工作（按时间）
| 谁 | 何时 | 提出了什么 | 来源 |
|---|---|---|---|
| Emily Bender、Timnit Gebru 等（FAccT 2021） | 2021-03 | **"随机鹦鹉"**：LM 按概率拼接语言形式而不指涉意义——"高级接龙"判断的学术母体 | dl.acm.org/doi/10.1145/3442188.3445922 |
| janus（LessWrong） | 2023-01~03 | **mode collapse**：RLHF 使输出向高概率陈词滥调坍缩（GPT-4 颜色词分布图）；后有反驳帖，引用需标注争议 | lesswrong.com/posts/t9svvNPNmFf5Qa3TA |
| Colin Fraser（数据科学家） | 2023-01-30 | LLM 是"不知疲倦的胡扯者"：AI 助手腔来自 **RLHF 把套话概率调高**（非训练数据自然存在）——AI 腔成因论最早讲透的文章 | medium.com/@colin.fraser/chatgpt-automatic-expensive-bs-at-scale-a113692b13d5 |
| Ted Chiang（纽约客） | 2023-02-09 | 模糊 JPEG 之喻（已有笔记01） | — |
| Sharma 等（Anthropic 等） | 2023-10-20 | **sycophancy 实证**：人类偏好数据奖励"顺着你说话" | arxiv.org/abs/2310.13548 |
| Kirk 等（Cohere/UCL/Meta，ICLR 2024） | 2023-10 | 实证 RLHF 相对 SFT **显著降低输出多样性**——"对齐使文本趋同"的学术证据 | arxiv.org/abs/2310.06452 |
| Hicks、Humphries、Slater（UCL/Nottingham） | 2024-07 | 论文《ChatGPT is bullshit》：幻觉=Frankfurt 式"对真相漠不关心" | link.springer.com/article/10.1007/s10676-024-09775-5 |
| Juzek、Ward 等 | 2024-12 | 《Why Does ChatGPT "Delve" So Much?》：delve 超量的来源分析（人工标注/RLHF 假说）——词汇污染阶段的学术锚点 | arxiv.org/abs/2412.11385 |
| 田威（科普中国） | 2025-10-17 | **中文最系统的 AI 味理论化**：四特征（官样大词/莫得感情/三段套路公文味/正确的废话）+"工业化生产 vs 手工艺" | thepaper.cn/newsDetail_forward_31802753 |
| Liang 等（普林斯顿/伯克利） | 2025-07-10 | **Machine Bullshit**：Bullshit Index + 四分类（empty rhetoric 等）——"空洞"成为可测量对象 | arxiv.org/abs/2507.07484 |
| Sam Kriss（NYT Magazine） | 2025-12-03 | AI 腔大众化定本：tapestry/liminal、"It's not X, it's Y"、"synthetic earnestness"，并指出**反向污染人类写作** | nytimes.com/2025/12/03/magazine/chatbot-writing-style.html |
| Nathan Lambert（Interconnects） | 2025-11-16 | 《Why AI writing is mid》：**对齐训练结构性摧毁写作声音**（有机制、无分期） | interconnects.ai/p/why-ai-writing-is-mid |
| 沈志荣（潮新闻） | 2026-07-27 | **概念史批判**：AI 味是"旧病新名"——报纸腔→翻译腔→键盘腔→AI味的百年骂史；警告"反AI味的AI味" | tidenews.com.cn/news.html?id=3512842 |
| 黄龙翔（联合早报） | 2026-08-28 | 评《经济学人》：所谓 AI 文风特征（除长破折号）**早已存在于学术/法律/公文写作**，LLM 只是把旧文风变成默认答案 | zaobao.com/forum/views/story20260828-9591292 |
| Jill Lepore（纽约客） | 2026-05-25 | 《The Prehistory of A.I. Slop》：slop 百年史前史（Plot Robot、Auto-Beatnik）——"回顾史"文体已被占领 | newyorker.com/magazine/2026/05/25 |

### "分期演变"的最近先例（都没有完整三阶段）
- **WaPo 数据报道（2025-08）**：328,744 条 gpt-4o 消息（2024.5–2025.7）量化词汇漂移——delve 衰落、core×5、modern>8%（华盛顿邮报 technology/interactive/2025/how-detect-chatgpt-em-dash/）
- **headcore.digital（2026）**："tell 按年代更替"说：2023 delve 旗标 → 2025 崩塌被 core/modern 取代；机制=识别→调训的猫鼠循环
- **Ransomnews（2026-08-21）**：**"tell 约 18 个月过期"**周期律（21,442 篇 arXiv 摘要；delve 较 2024 峰值 -94%）
- **钛媒体（2025-06-30）**：中文"两代 AI 味"对比（ChatGPT式 vs DeepSeek式）；把 delve 归因 RLHF 非洲标注员（《卫报》2024-04）
- **中国社会科学报（2026-07-03）**：接龙+RLHF 的共时机制归因（无时间分期、不涉及推理世代）

### ✅ 本文增量（支柱①）
**"接龙→对齐→推理"三阶段机制分期，公开文献中未发现完整先例。** 已有的是：词表分期（headcore/Ransomnews）、两代对比（钛媒体）、共时机制（社科报/Lambert）、史前史（Lepore）。本文首次把"味的变迁"绑定到**训练范式变迁**（自回归→RLHF 对齐→推理范式）并给出每阶段的成因归因。

---

## 二、支柱②中英对比：检测基准与"口音"研究成熟，整合叙事是我们的

| 谁 | 何时 | 提出了什么 |
|---|---|---|
| Macko、Moro、Uchendu 等（KInIT/PSU，EMNLP 2023） | 2023-12 | **MULTITuDE**：11 语言（含中文）×8 LLM 检测基准；检测器对未见语言泛化差；领域自认英语中心 |
| Wang、Mansurov 等（MBZUAI，EACL 2024） | 2024-03 | **M4** 基准（资源论文奖）：跨域/跨模型/跨语言泛化难 |
| Guo 等（Apple） | 2024-10 | 《Do LLMs Have an English Accent?》：法语/中文输出带**英语中心词汇语法模式**（自然度指标+对齐缓解） |
| Volansky、Ordan、Wintner（海法大学）；Rabinovich 等 | 2015-2017 | **translationese detection**：92 特征证明翻译腔是可计算的独立语体——"AI味=新翻译腔"的现成方法论（早于 LLM 十年） |
| Berber Sardinha（PUC-SP，Applied Corpus Linguistics） | 2024-04 | **Biber 多维分析首次系统用于 AI 文本**：AI 文本在语体维度系统性偏移——"语体错位"的学术先例 |
| yage.ai 博主 | 2026-04-18 | 强论题：**"AI味很大程度上就是翻译腔"**（"接住"=catch、"锋利"=sharp），含套路词表与修改手册 |
| 社科院简圣宇 | 2026-07-03 | 中文"官腔/套话/八股"定性（已有笔记02） |
| Zaitsu & Jin（Frontiers in AI）；ユアブライト；Qiita | 2026-06 | 日语旁证：六 LLM 日语"指纹"可检测；humanizer-jp 产品；651 词"AIっぽい日本語"词表 |
| arXiv 2503.04369 | 2025-03 | SFT 监督训练造成 translationese 偏差——AI 味与翻译腔**同源**的机制证据 |

### ✅ 本文增量（支柱②）
单点研究全齐（检测基准/英语口音/翻译腔/语体偏移），但**"英文 LinkedIn 腔 vs 中文公文腔×翻译腔"的双味型对照叙事**、以及用自建实验（发现 C/D：文体错位 3–8 倍、社区词表在默认输出零出现）来对照中文社区词表的迷信，是本文的整合增量。

---

## 三、支柱③思维链外显：研究线成熟，"痕迹进成稿"的写作视角是我们的

| 谁 | 何时 | 提出了什么 |
|---|---|---|
| Lanham 等（Anthropic） | 2023-07 | **CoT 忠实性首测**：外显推理≠真实计算（arXiv 2307.13702）——该研究线学术原点 |
| OpenAI（o1 模型卡） | 2024-09 | hidden CoT + "Thought for X seconds" 产品化（已有笔记03） |
| Zvi Mowshowitz | 2025-01-22 | 《On DeepSeek's r1》："读思维链、扔答案"——可见 CoT 被当核心价值与可读人格 |
| Nathan Lambert | 2025-01-21 | "Wait/自我纠错"是 RL 涌现行为；**"冗长 CoT 文体"单列为研究对象** |
| Marjanović、Patel、Adlakha 等 | 2025-04 | **DeepSeek-R1 Thoughtology**（arXiv 2504.07128）：思考痕迹的系统分类学（自我验证/犹豫语/脱轨/"aha"）——**与本文"痕迹类型学"重叠度最高的学术工作** |
| Michelle Quirk（Psychology Today） | 2025-04 | "AI Cognitive Theater"：看 AI 思考=认知剧场 |
| THiNK（arXiv 2505.20184） | 2025-05 | 认知科学"出声思维法"（think-aloud）正式移植到 LLM 推理评测 |
| "Reasoning Theater"（arXiv 2603.05488） | 2026-03 | CoT 是可与真实信念解耦的表演层 |
| Richard Coyne（爱丁堡大学荣休教授） | 2026-07-21 | **戈夫曼"前台/后台"框架**解释 AI 外显思考：可见思维链=把后台搬上前台 |
| Anthropic / OpenAI / GitLab / lettabot / 试卷案例 | 2025-2026 | 忠实性、监控、产品泄露（已有笔记03） |

### ✅ 本文增量（支柱③）
学术线聚焦"忠实性/监控/评测"；本文的增量是**写作与文体视角**：①把思维链外显作为 AI 味的"第三代来源"纳入文风变迁史；②"草稿与成稿边界被模型弄混"的写作史论断；③**思维开关对照实验**（同一模型开/关思维，成稿标记词 +57%、抒情腔翻倍）——这个对照在中文世界未见报告；④"给自己画图"（Sketchpad 自用思考 → 思考图被当插图）的过程痕迹视角。

---

## 四、支柱④检测与消除：综述与攻防全齐，"分型×工具矩阵"是我们的

| 谁 | 何时 | 提出了什么 |
|---|---|---|
| Sadasivan 等（UMD） | 2023-03 | **《Can AI-Generated Text be Reliably Detected?》**：改写攻击使检测器与水印 AUROC 趋随机——"检测不可靠"叙事源头 |
| Tang 等；Kumarage 等；arXiv 2410.14677 | 2023-10/2024 | 检测综述三连：方法框架；**Detection/Attribution/Characterization 三任务**；评测集质量缺陷致性能虚高 |
| Krishna 等（NeurIPS 2023） | 2023-03 | DIPPER 改写攻击（已有笔记04） |
| Jovanović 等（ETH，ICML 2024） | 2024-05 | **Watermark Stealing**：可伪造他人水印——水印信任前提被瓦解 |
| Esmaeilpour 等；Wang 等（ICLR 2025）；AuthorMist | 2024-2025 | humanizing 攻击系列前作 |
| Cheng、Sadasivan 等（UMD，NeurIPS 2025） | 2025-06 | **《Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text》**——学术"humanizing"旗舰；该方向**无独立综述**（可主张） |
| DAMAGE（ACL 2025 GenAI Detect workshop） | 2025 | 防御侧回应 |
| Rivera Soto 等（JHU） | 2025-05（v3 2026-06） | **humanizer 有效性的学术边界**：攻击骗过标准检测器，但**洗不掉风格指纹**（few-shot 风格检测器仍识别）——arXiv 2505.14608 |
| GPTZero | 2024-10 | AI Vocabulary：50 个最高频 AI 词，按月更新（早于 humanizer 浪潮一年） |
| Pangram Labs | 2025-02 | AI Phrases 分类体系（含多语种版本与逐条走查系列） |
| Wikipedia WikiProject AI Cleanup | 2023-12-04 创建（编者 Ca；Chaotic Enby 发起项目） | **《Signs of AI writing》**：现约 65-78 条目、2051 次修订——全球被引用最多的 AI 味特征框架；blader/humanizer 的 35 模式直接继承于此（README 自述） |
| CNET（Reichert）；什么值得买聚合 | 2026-07 | humanizer×检测器实测（英文/中文两条线；中文实测潮 40+ 篇） |
| 界面新闻·镜相工作室 | 2026-07-02 | 出版社编辑的"AI 味把关"困境（郝景芳新书自述 AI 生成占一半） |
|皇甫博媛（华东师大，新闻与写作 2026 年第 3 期） | 2026 | **首篇以"AI味"为核心的中文传播学论文**《"AI味"与"人机感"：社交媒体话语中的机器主体性建构》 |

### ✅ 本文增量（支柱④）
- "按 AI 味类型映射消除工具"的**严格对照矩阵未发现先例**（最接近：harshaneel/humanize 的"九个杠杆"检测文献映射、中文实操文的成因→对策清单）——本文的"三代味型 × 三层药方 × 失效边界"矩阵可主张增量
- 中文 108 篇量化实验（含**同模型思维开关对照**）填补"中文 delve 空白"
- 面向公众号读者的**机制-识别-消除**三层整合叙事本身

---

## 五、成文时的署名纪律（写进正文的位置建议）

1. **引子/第一节**：提 Bender"随机鹦鹉"与 Fraser/Frankfurt"胡扯"论——"高级接龙"不是我发明的词，但把三阶段接起来是。
2. **第二节**：delve 研究归 Kobak；词表框架归 Wikipedia Signs of AI writing（顺带纠正"官方 humanizer"误传）。
3. **第三节**：CoT 忠实性归 Lanham 2023；R1 文风分析引 Lambert/Zvi/Thoughtology；戈夫曼后台框架引 Coyne——本文贡献是"把它接进写作史+中文案例+对照实验"。
4. **第四节**：英语口音归 Apple；语体错位学术先例归 Berber Sardinha；翻译腔论引 yage.ai 与 Volansky 谱系。
5. **第五节**：检测不可能性归 Sadasivan；"humanizer 洗不掉风格指纹"引 JHU 2025——这是"消除篇"泼冷水的关键引用。
6. **第六节**：humanizer 谱系表标注各方案来源（blader=维基 35 模式）；实验数据标注局限。
7. 全文至少一次明说："本文的三个原创点：三阶段机制分期、中文量化小实验、思维开关对照"——把诚实变成公信力。
