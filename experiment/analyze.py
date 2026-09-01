#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析 run_experiment.py 采集的语料：AI味词频 / 句式 / 统计特征，按模型与题型汇总。

输出：findings.md（人读）+ summary.json（机读）。
"""
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw" / "responses.jsonl"

# 词表来源：cn-humanizer、anti-vibe-writing、社科院/光明日报定性 + 研究笔记03 抒情腔词，
# 并保留少量"中性对照词"（不该有区分度的词）用于 sanity check。
CATEGORIES = {
    "公文黑话": ["赋能", "抓手", "闭环", "深耕", "聚焦", "助力", "痛点", "底层逻辑",
                 "顶层设计", "降本增效", "提质增效", "保驾护航", "新篇章", "全方位", "多维度"],
    "衔接套话": ["值得注意的是", "综上所述", "总而言之", "总的来说", "首先", "其次",
                 "与此同时", "无独有偶", "由此可见"],
    "意义拔高": ["见证", "塑造", "勾勒", "诠释", "彰显", "引领", "变革", "浪潮",
                 "深刻", "深远", "璀璨", "璀璨夺目", "画卷"],
    "抒情腔": ["拓扑", "克莱因瓶", "睫毛", "青苔", "齿轮", "白衬衫", "瞳仁", "涟漪",
               "荡漾", "星辰", "温柔", "治愈", "绽放", "静谧", "诗和远方", "缓缓流淌"],
    "元话语": ["某种意义上", "或许", "也许", "在某种程度上"],
    "中性对照": ["因为", "但是", "可以", "我们", "非常"],
}

PATTERNS = {
    "不仅…而且/更": r"不仅[^。！？]{0,15}(而且|更是|还)",
    "不是…而是": r"不是[^。！？]{0,18}而是",
    "让我们": r"让我们",
    "拭目以待": r"拭目以待",
    "在当今/…时代": r"在(当今|这个|这个充满)?[^。！？]{0,10}(的?时代|今天|背景下)",
    "随着…的发展": r"随着[^。！？]{0,12}的(发展|普及|推进|深入)",
    "排比三连(不是/没有实义的并列)": r"[^。！？，]{2,8}，[^。！？，]{2,8}，[^。！？，]{2,8}，",
}

SENT_SPLIT = re.compile(r"[。！？!?]")
CJK = re.compile(r"[\u4e00-\u9fff]")


def cjk_len(s):
    return len(CJK.findall(s))


def analyze_text(text):
    r = {}
    n = max(cjk_len(text), 1)
    r["cjk_chars"] = n
    r["flag_total"] = 0
    r["cat"] = {}
    for cat, words in CATEGORIES.items():
        c = sum(text.count(w) for w in words)
        r["cat"][cat] = c
        if cat != "中性对照":
            r["flag_total"] += c
    r["pattern"] = {}
    for name, pat in PATTERNS.items():
        r["pattern"][name] = len(re.findall(pat, text))
    sents = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    lens = [cjk_len(s) for s in sents]
    r["sentences"] = len(lens)
    if lens:
        r["sent_mean"] = round(statistics.mean(lens), 1)
        r["sent_stdev"] = round(statistics.stdev(lens), 1) if len(lens) > 1 else 0.0
        r["sent_cv"] = round(r["sent_stdev"] / r["sent_mean"], 2) if r["sent_mean"] else 0
    r["excl"] = text.count("！") + text.count("!")
    r["colon"] = text.count("：") + text.count(":")
    r["emdash"] = text.count("——") + text.count("—")
    # 归一化：每千字
    k = 1000.0 / n
    r["flag_per_1k"] = round(r["flag_total"] * k, 2)
    r["cat_per_1k"] = {c: round(v * k, 2) for c, v in r["cat"].items()}
    r["pattern_per_1k"] = {c: round(v * k, 2) for c, v in r["pattern"].items()}
    return r


def main():
    recs = [json.loads(l) for l in RAW.read_text().splitlines() if l.strip()]
    # 1) 只保留带 arm 的记录；2) 按 (arm, topic, run) 去重，重跑补采后同一组合可能有多条，
    #    保留正文最长的一条；3) 正文 < 100 字的样本视为废样本剔除（思考模型截断产物）
    best = {}
    n_error = 0
    for r in recs:
        if not r.get("arm"):
            continue
        if not r.get("content"):
            n_error += 1
            continue
        key = (r["arm"], r["topic"], r["run"])
        if key not in best or len(r["content"]) > len(best[key]["content"]):
            best[key] = r
    ok = [r for r in best.values() if len(r["content"]) >= 100]
    dropped_short = len(best) - len(ok)
    print(f"records={len(recs)}, valid combos={len(best)}, kept={len(ok)} "
          f"(dropped {dropped_short} short, {n_error} error/no-content)")

    by_model = defaultdict(list)
    by_model_topic = defaultdict(list)
    for r in ok:
        a = analyze_text(r["content"])
        item = {"topic": r["topic"], "run": r["run"], **a}
        by_model[r["arm"]].append(item)
        by_model_topic[(r["arm"], r["topic"])].append(item)

    def agg(items):
        n = len(items)
        out = {"n": n}
        for f in ["cjk_chars", "flag_per_1k", "sent_mean", "sent_stdev", "sent_cv",
                  "excl", "colon", "emdash"]:
            out[f] = round(statistics.mean(x[f] for x in items), 2)
        out["cat_per_1k"] = {
            c: round(statistics.mean(x["cat_per_1k"][c] for x in items), 2)
            for c in CATEGORIES if c != "中性对照"}
        out["pattern_per_1k"] = {
            c: round(statistics.mean(x["pattern_per_1k"][c] for x in items), 2)
            for c in PATTERNS}
        return out

    model_agg = {m: agg(v) for m, v in by_model.items()}
    mt_agg = {f"{m} :: {t}": agg(v) for (m, t), v in by_model_topic.items()}

    lines = ["# 小实验结果：多模型中文 AI 味量化", "",
             f"有效样本 {len(ok)} 篇（7+2 档位 × 4 题型 × 3 次；剔除过短 {dropped_short} 条、空/报错 {n_error} 条）", ""]
    lines += ["## 模型排名（按 AI味标记词 每千字，降序）", "",
              "| 模型 | 样本 | 标记词/千字 | 公文黑话 | 衔接套话 | 意义拔高 | 抒情腔 | 句长CV | 句均长 |",
              "|---|---|---|---|---|---|---|---|---|"]
    for m, a in sorted(model_agg.items(), key=lambda kv: -kv[1]["flag_per_1k"]):
        c = a["cat_per_1k"]
        lines.append(f"| {m} | {a['n']} | {a['flag_per_1k']} | {c['公文黑话']} | {c['衔接套话']} "
                     f"| {c['意义拔高']} | {c['抒情腔']} | {a['sent_cv']} | {a['sent_mean']} |")
    lines += ["", "## 句式模式（每千字）", "",
              "| 模型 | 不仅…而且 | 不是…而是 | 让我们 | 拭目以待 | 在…时代 | 随着…的发展 | 排比三连 |",
              "|---|---|---|---|---|---|---|---|"]
    for m, a in sorted(model_agg.items(), key=lambda kv: -kv[1]["flag_per_1k"]):
        p = a["pattern_per_1k"]
        lines.append(f"| {m} | {p['不仅…而且/更']} | {p['不是…而是']} | {p['让我们']} "
                     f"| {p['拭目以待']} | {p['在当今/…时代']} | {p['随着…的发展']} | {p['排比三连(不是/没有实义的并列)']} |")
    lines += ["", "## 题型 × 模型 明细（标记词/千字）", "",
              "| 模型 :: 题型 | 标记词/千字 | 句长CV |",
              "|---|---|---|"]
    for k_, a in sorted(mt_agg.items(), key=lambda kv: -kv[1]["flag_per_1k"]):
        lines.append(f"| {k_} | {a['flag_per_1k']} | {a['sent_cv']} |")
    (HERE / "findings.md").write_text("\n".join(lines), encoding="utf-8")
    (HERE / "summary.json").write_text(json.dumps({
        "model_agg": model_agg, "model_topic_agg": mt_agg,
        "dropped_short": dropped_short, "errors": n_error},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote findings.md / summary.json")


if __name__ == "__main__":
    main()
