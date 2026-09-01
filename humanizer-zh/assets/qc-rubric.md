# qc-rubric — 终检评分表 + HumT 停手规则 + 教材二步对互补说明

配 humanizer-zh Stage 5 使用。三项内容：①终检评分表（交稿前逐项打勾）；
②HumT 警告——何时**不要**继续"人味化"；③与 tb-deai-style / tb-humanizer
（教材专用二步对）的互补与路由。

---

## ① 终检评分表（四项全过才交稿）

### A. 事实零改动 diff

- [ ] 逐 hunk 对比改写前后：数字、引语、出处、案例事实一字不动
- [ ] 疑似必要的事实级改动已标 `[NUM-CHECK]` 转人工，未落盘
- [ ] 建议性删除（>2 句论证性段落）已标 `[DEL-CHECK]`，未直接删
- [ ] UI 残留数字（"用时 X 秒"类）确属过程痕迹而非内容事实（红线2 唯一
      豁免通道）

### B. Stage 1 重跑对比（达标线，方向性指标）

| 指标 | 达标线 | 依据 |
|---|---|---|
| 总标记词 | ≤ 4.0/千字 | 实验最淡档：glm-5.3 为 3.70、gemini-2.5-nothink 为 3.96【实验】 |
| 主导味型类 | 较基线降幅 ≥ 60% | 主导类是本轮主攻对象 |
| 五类单类 | 均 ≤ 1.5/千字 | 防止按下葫芦浮起瓢（改写引入新味） |
| 语体错位 | 不超出目标场合基线（zh-register-map） | 发现C：跨文体差 3–8 倍，错位才是主罪 |

- [ ] 已输出前后五类分表对比
- [ ] 未达标已按轮次预算回到 Stage 1（第 3 轮后无条件停）
- **绝对值免责**：n=3/格、社区词表非金标准、抒情词在营销语境部分是文体
  需要——绝对值仅方向性参考【实验·局限】。正式判定以"语体对口 + 主导类
  降幅"为准。

### C. before/after 报告完整

- [ ] 轮次记录（含每轮主导味型变化）
- [ ] 删除统计按 Stage 2 规则分组计数
- [ ] `[DEL-CHECK]` / `[NUM-CHECK]` / 豁免清单齐备
- [ ] 报告本身用平实中文：无套话、无排比、无升华（报告是本 skill 门面）

### D. 声明照录

- [ ] 报告末尾附 SKILL.md §7.d 声明原文（目标是"读起来像人写的"，不是
      骗过检测器；风格指纹洗不掉）

---

## ② HumT 警告：何时停手（Stanford ACL 2025）

**核心发现**：Stanford HumT 指标 + DumT 解码可系统性调低拟人度——**但用户
在许多场景反而更不喜欢"像人"的输出**；拟人语气关联温暖、女性气质、低地位
等社会感知【Cheng, Yu & Jurafsky，ACL 2025，arXiv 2502.13259；研04】。另有
互证：人类并不总是偏好人写文本（盲测无法确认来源时）【Wang 等，ACL 2026，
arXiv 2502.11614；研04】。

**停手条件（任一成立即停，并向用户说明）**：
1. **功能文体**：API 文档、法律文书、规范公文——这些场合"稳定、可预期"
   本身是需求，人味化反而降可信度；
2. **用户未抱怨**：没人反馈"像 AI"时，主动人味化是在替读者做主——先问；
3. **第 3 轮边际降幅 < 10%**：继续改的期望收益低于引入新味（"反 AI 味的
   AI 味"）的风险【研05·沈志荣】；
4. **作者本意就是浓意象**：朋友圈/文学场合的"星辰/温柔"可能是作者风格，
   不是残留（小红书误伤案例：自写文案被老板判"你太依赖AI"【研02】）。

**检测器免责（向用户交底的三条证据）**：
- 改写攻击使检测器与水印 AUROC 趋随机【Sadasivan 等 2023《Can AI-Generated
  Text be Reliably Detected?》，UMD】；
- humanizer 攻击骗过标准检测器，但**洗不掉风格指纹**：few-shot 风格检测器
  仍能识别改写文本【Rivera Soto 等，JHU 2025，arXiv 2505.14608】；
- 检测器误伤集中于语言受限者：61%+ 非母语 TOEFL 作文被误判【Liang 等
  2023；研04】；中文侧知网 86.8% 误判与跨平台 32% 落差【研04】。商业
  humanizer 独立评测 bypass 率 0%–93% 分歧巨大——"过检测"本身不是稳定
  目标【研04】。

---

## ③ 与 tb-deai-style / tb-humanizer 的互补说明

同库中已有**教材专用二步对**（ning-embodied-knowledge 库）：tb-deai-style
（第一步，减法：四层检测删 AI 指纹）→ tb-humanizer（第二步，加法：注入
作者思维秩序与态度，署名/记账/认账人格）。两者语料锚是**单日单课单受众的
教材作者语料三档案**，带密度账本与教材体例豁免。

| | tb-deai-style → tb-humanizer | humanizer-zh |
|---|---|---|
| 定位 | 教材专库二步对（先减后加） | 通用中文五阶段循环 |
| 语料锚 | 教材作者语料（讲堂逐字稿） | ai-flavor 四研究档案 + 108 篇实验 |
| 改写方向 | 注入特定作者人格 | 校准到目标场合的通用"人味" |
| 特色机制 | 密度账本、`[JUDG/CASE/DEL-CHECK]` 通道 | Stage 4 思维链泄露清洗、语境门控、厂牌先验 |
| 独有红线 | 教材体例组件禁改 | 检测器免责声明必须照录 |

**路由规则**：
1. AI 与管理教材项目 → 走教材二步对，**不调用本 skill**；
2. 教材稿在通用检查中发现残留 → 标 `[DEAI-RESIDUE]` 退回教材对处理，
   两把刀不叠跑（防互相覆盖产出，同 tb-humanizer §1 原则）；
3. 其他一切中文交付文 → 本 skill；
4. 本 skill 处理后的教材外稿件若需"作者人格级"人味（署名判断、详略
   不对称、敢不收圆），可参考 tb-humanizer 六原则的**思路**（非其密度
   账本——那是作者语料专属），但本 skill 不自动执行第二步注入。

---

## 出处

- 【研04】post/inputs/ai-flavor/research/04-detection-and-humanizer.md
  （HumT/DumT、用户未必想要人味、检测误伤史、商业 humanizer bypass 分歧、
  "把人的东西放进去"结论）
- 【研05】post/inputs/ai-flavor/research/05-related-work.md（Sadasivan、
  JHU Rivera Soto、沈志荣"反AI味的AI味"、署名纪律）
- 【研02】post/inputs/ai-flavor/research/02-chinese-vs-english.md（小红书
  误伤案例）
- 【实验】post/inputs/ai-flavor/experiment/（最淡档基线 3.70/3.96、发现C、
  局限）
- HumT：arxiv.org/abs/2502.13259（Cheng, Yu & Jurafsky，ACL 2025）
- Wang 等（人类检测上限与偏好）：arxiv.org/abs/2502.11614
- Sadasivan 等 2023：arxiv.org/abs/2303.11150
- JHU（Rivera Soto 等）：arxiv.org/abs/2505.14608
- Liang 等（TOEFL 误伤）：sciencedirect.com/science/article/pii/S2666389923001307
- 教材二步对：ning-embodied-knowledge/skills/owned/tb-deai-style/SKILL.md、
  tb-humanizer/SKILL.md
