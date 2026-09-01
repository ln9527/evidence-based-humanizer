# 研究笔记 04｜检测的失败与消除方案的谱系

> 研究执行：多智能体联网检索，2026-08-31。

---

## A. AI 检测：原理、失败史与误伤

**核心结论**：检测器盯统计特征（低困惑度、句间均匀），人闻"味"靠语感与语体错位——两者系统性错位。检测史就是一部失败史，且误伤集中在"语言受限的人"身上。

### 关键发现

| 发现 | 证据 | 来源 | 置信度 |
|---|---|---|---|
| 原理：GPTZero 两指标——perplexity（文本对模型的"意外程度"）+ burstiness（句间波动）；两值都高更可能出自人手 | GPTZero 官方解释页 | gptzero.me/news/perplexity-and-burstiness-what-is-it/ | high |
| OpenAI 自家分类器 2023-02 上线（真阳性率仅26%、假阳性9%），2023-07-20 以"low rate of accuracy"下架；2025-04 起转向不可见 Unicode 字符水印（官方称覆盖 chatgpt.com 约99%文本输出） | TechCrunch 2023-07-25；OpenAI 水印公告 | techcrunch.com/2023/07/25/openai-scuttles-ai-written-text-detector-over-low-rate-of-accuracy/ | high |
| Turnitin 2023-04 上线宣称 98% 准确率/1% 误报，范德堡等高校同年 8 月禁用（大规模使用下 1% 误报必误伤大量学生） | Vanderbilt 官方声明 2023-08-16；UBC 同月不启用 | vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-... | high |
| 误伤实锤：Liang 等 2023（Patterns），7 款检测器把 **61%+ 的非母语 TOEFL 作文误判为 AI**（母语作文准确率>91%）；且"提高burstiness"式简单提示即可让漏检率接近100%；作者解释：检测器把"简单、可预测的语言"当 AI 信号，恰与非母语写作特征重合 | Patterns（Cell Press） | sciencedirect.com/science/article/pii/S2666389923001307 | high |
| 中文检测的"玄学化"：纯原创论文被判"AI创作"；学生知网 AI 率被测出 86.8%、被迫"少写术语多说口水话"降重；同篇论文跨平台 AI 率相差可达 32%；光明日报 2026-07 讨论"AI防线"利弊 | 大众网 2026-05-10；搜狐；光明日报 | dzwww.com/xinwen/shehuixinwen/202605/t20260510_17717814.htm | high |
| 人 vs 机器的感知错位：盲测中非专业读者区分 AI/人写诗歌的正确率不高于随机，且 AI 诗在节奏、意象上**评分更高**（Porter & Machery, Scientific Reports 2024-11）；人类检测上限其实很高：19 名标注者跨 9 语言达 87.6%（Wang 等，ACL 2026，16数据集）——人的差距感在于具体性、文化细节与多样性 | Springer；arXiv 2502.11614 | link.springer.com/article/10.1038/s41598-024-76900-1；arxiv.org/abs/2502.11614 | high |

### 可引用例证
- "GPT detectors are biased against non-native English writers"（论文标题本身即可引用）
- "知网测出AI率86.8%？学生被迫'反智'降重：少写术语，多说口水话"（报道标题）
- "换个平台就相差 32%，AI 论文检测成玄学"（公众号标题）

---

## B. Humanizer 工具与 skill 全景（消除方案）

**核心结论**：Anthropic 官方 skills 仓库并无 humanizer（坊间误传）；真正的爆款是社区 blader/humanizer（3.9万星，基于维基百科 35 种 AI 痕迹模式两遍改写）；中文圈已自成生态（Humanizer-zh 1.6万星等）；商业 humanizer 只改统计签名骗检测器，独立评测 bypass 率 0%–93% 分歧巨大。

### 工具谱系表（成文时可直接做成对照表）

| 方案 | 类型 | 原理 | 针对的味型 | 规模/来源 |
|---|---|---|---|---|
| blader/humanizer | Claude skill | 按维基百科 WikiProject AI Cleanup"Signs of AI writing"35种模式两遍改写：先脱稿重写，再按模式核对；不改事实、可匹配用户语声 | 模板句式、高频词、意义拔高、强行三连、em dash 滥用、聊天残留 | 39,207★，2026-01，Wired/Verge/Ars 报道（github.com/blader/humanizer） |
| op7418/Humanizer-zh | 中文 skill | blader 版汉化（作者：歸藏） | 同上，中文语境 | 16,378★（github.com/op7418/Humanizer-zh） |
| MrGeDiao/shuorenhua | 中文 skill | 分场景（chat/status/docs/public-writing）×三档力度；保事实、保术语、不用机械同义词替换、防"表演感" | 语体错位、过度润色 | 1,315★（github.com/MrGeDiao/shuorenhua） |
| 0xtresser/cn-humanizer | 中文词表+规则 | 18种中文AI模式（意义拔高/空洞归纳/排比堆砌/"的"字连珠/机器人开场/鸡汤收尾）+100+高频词分级表+12条翻译腔规则；README 附改写前后对比 | 空洞感、高频词、翻译腔 | 13★（github.com/0xtresser/cn-humanizer） |
| weijt606/anti-vibe-writing | 中文四层清单 | 词汇/句式/结构/语气四层去味，附弱/强对照例句 | 排比、四字堆砌、同义词循环 | 110★ |
| ninehills/deslop-zh | prompt 减法 | 四原则："自然>风格化、减法优先、保语义>去AI味、场景决定策略"；速查清单：删"这说明/可以看出"收尾、删"随着…的发展"开头 | 空洞感、模板结构 | github.com/ninehills/public-skills |
| Undetectable.ai / HIX Bypass / QuillBot humanizer | 商业 SaaS | 调整用词/句式/文体**统计签名**以骗过检测器（目标是"不可检测"，不是"写得更好"） | 只针对检测器特征，不解决空洞感/语体错位 | 独立评测 bypass 率 0%–93% 分歧（fast.io/resources/undetectable-ai-review-2026/） |
| aislop / ai-slop-detect | 代码侧 linter | 扫描叙述性注释、吞异常、死代码等 agent 遗留 | 编码智能体过程痕迹 | github.com/scanaislop/aislop |

### blader/humanizer 35 模式示例（可引用）
- 语言模式#10"强行三连"（Forced groups of three）："innovation, inspiration, and insights" → 改法：**按含义需要决定用几个**。
- cn-humanizer 改写对比——改写前："值得注意的是，这一技术不仅赋能了传统行业的数字化转型，更为创新型企业打造了全方位的智能化解决方案。综上所述……让我们拭目以待。" 改写后："大语言模型这两年确实火。写代码、做客服、翻译文档，能干的事越来越多。"

---

## C. 学术视角：去 AI 味的根本困难

| 发现 | 证据 | 来源 | 置信度 |
|---|---|---|---|
| 改写攻击让检测器失效：DIPPER（11B改写模型）把 DetectGPT 准确率 70.3%→4.6%（1%误报率下），同时绕过水印/GPTZero/OpenAI分类器，且不改变语义；检索式防御可找回 80–97%，但依赖集中式基础设施 | Krishna 等，NeurIPS 2023，arXiv 2303.13408 | arxiv.org/abs/2303.13408 | high |
| 水印脆弱性有争议：Kirchenbauer 团队 ICLR 2024 认为改写文本倾向泄漏原文 n-gram，积累足够 token 仍可检出（强人工改写后平均800 token 可检） | arXiv 2306.04634 | arxiv.org/abs/2306.04634 | high |
| Model collapse：Shumailov 等 Nature 2024——无差别用 AI 文本再训练，"tails of the original content distribution disappear"（分布尾部不可逆消失）——AI 味被数据回流固化的结构性风险 | Nature 631:755–759（2024-07-24） | nature.com/articles/s41586-024-07566-y | high |
| AI 味可测可调：Stanford HumT 指标+DumT 解码可系统性调低拟人度——**但用户在许多场景反而更不喜欢"像人"的输出**；拟人语气关联温暖、女性气质、低地位等社会感知 | Cheng, Yu & Jurafsky，ACL 2025，arXiv 2502.13259 | arxiv.org/abs/2502.13259 | high |
| AI 味的部分根源：偏好数据的"典型性偏差"（标注者偏爱眼熟文本）→ mode collapse；Verbalized Sampling 提示法可让创意写作多样性提升 1.6–2.1 倍——生成端可缓解，但属结构性 | arXiv 2510.01171（Stanford，2025-10） | arxiv.org/abs/2510.01171 | high |
| 人类检测上限 87.6%，且**人类并不总是偏好人写文本**（无法确认来源时） | Wang 等，ACL 2026，arXiv 2502.11614 | arxiv.org/abs/2502.11614 | high |

### 成文论点素材（消除篇的三个"坏消息"）
1. **检测不可靠** → "消除"的第一性目标不是骗过检测器。
2. **味有结构性根源**（RLHF 偏好平均化、典型性偏差、数据回流）→ 逐词替换式 humanizer 治标。
3. **用户未必想要"人味"** → 大多数场景用户要的不是"像人"，而是"有用+不别扭"。"去AI味"的终极形态不是把AI文本改得像人，而是把人的东西（判断、具体经验、风险承担）放进去。
