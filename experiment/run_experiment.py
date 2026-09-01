#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中文 AI 味量化小实验（v2，全 OpenRouter）：多模型同题生成中文短文，采集原始语料。

8 个模型档位（用户指定新模型 + 必要对照组）：
  C1 anthropic/claude-sonnet-5        （此前经 Anthropic 直连已完成 12/12，自动跳过）
  D1 deepseek/deepseek-v4-flash       用户指定
  D2 deepseek/deepseek-v4-pro         同厂对照
  Z1 z-ai/glm-5.3                     用户指定
  G1 google/gemini-3.7-flash          最新 Gemini flash
  P1 openai/gpt-5.6-sol               补齐第三家
  X1 google/gemini-2.5-flash          上一代锚点（thinking 默认开）
  X2 google/gemini-2.5-flash          reasoning.enabled=false（同一模型关思维）→ 与 X1 关键对照

4 题型 × 3 次采样；不设 system prompt、不调 temperature（测默认文风）。
输出：raw/responses.jsonl 追加（可断点续跑，按 arm+topic+run 去重）。
"""
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_FILE = HERE / "raw" / "responses.jsonl"
KEY_PATH = Path("/Users/ningli/Dropbox/Ning_Agentic_AI_workflow/claude_code/cc-writing/post/api_openrouter")
API = "https://openrouter.ai/api/v1/chat/completions"

ARMS = [
    {"arm": "claude-sonnet-5", "model": "anthropic/claude-sonnet-5"},
    {"arm": "deepseek-v4-flash", "model": "deepseek/deepseek-v4-flash"},
    {"arm": "glm-5.3-flash", "model": "z-ai/glm-5.3-flash"},
    {"arm": "gemini-3.7-flash", "model": "google/gemini-3.7-flash"},
    {"arm": "gpt-5.6-terra", "model": "openai/gpt-5.6-terra"},
    {"arm": "gemini-2.5-flash", "model": "google/gemini-2.5-flash"},
    {"arm": "gemini-2.5-flash-nothink", "model": "google/gemini-2.5-flash",
     "reasoning": {"enabled": False}},
]

TOPICS = {
    "viewpoint": "写一篇300字左右的短文，谈谈远程办公的利与弊。",
    "reading": "写一篇300字左右的读书心得，主题是余华的小说《活着》。",
    "marketing": "为一款新上市的桂花拿铁写一段200字左右的推广文案。",
    "casual": "写一段发在朋友圈的文字，300字以内，记录周末去爬山。",
}

RUNS = 3
MAX_WORKERS = 5
RETRIES = 3


def already_done():
    done = set()
    if OUT_FILE.exists():
        for line in OUT_FILE.read_text().splitlines():
            try:
                r = json.loads(line)
                # 思考模型可能把 max_tokens 预算烧在 reasoning 上导致正文为空/极短，
                # 因此"完成"判定要求正文 >= 120 字
                if r.get("content") and len(r["content"]) >= 120:
                    done.add((r["arm"], r["topic"], r["run"]))
            except Exception:
                pass
    return done


def call(model, prompt, reasoning=None):
    key = KEY_PATH.read_text().strip()
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "max_tokens": 4000}
    if reasoning is not None:
        payload["reasoning"] = reasoning
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    msg = data.get("choices", [{}])[0].get("message", {})
    usage = data.get("usage", {})
    return {
        "content": msg.get("content") or "",
        "reasoning_present": bool(msg.get("reasoning")),
        "completion_tokens": usage.get("completion_tokens"),
        "completion_tokens_details": usage.get("completion_tokens_details"),
        "usage": usage,
    }


def work(job):
    a, t, r = job
    last = None
    for attempt in range(RETRIES):
        try:
            out = call(a["model"], TOPICS[t], a.get("reasoning"))
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:250]
            last = f"HTTP {e.code}: {body}"
            if e.code in (429, 500, 502, 503, 504, 529) and attempt < RETRIES - 1:
                time.sleep(8 * (attempt + 1))
                continue
            out = {"error": last}
            break
        except Exception as e:  # noqa: BLE001
            last = str(e)
            if attempt < RETRIES - 1:
                time.sleep(8 * (attempt + 1))
                continue
            out = {"error": last}
            break
    rec = {"arm": a["arm"], "model": a["model"], "topic": t, "run": r, **out}
    with OUT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main():
    OUT_FILE.parent.mkdir(exist_ok=True)
    done = already_done()
    jobs = [(a, t, r) for a in ARMS for t in TOPICS for r in range(1, RUNS + 1)
            if (a["arm"], t, r) not in done]
    print(f"total jobs: {len(jobs)} (skipping {len(done)} done)", flush=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(work, j): j for j in jobs}
        for i, fut in enumerate(as_completed(futs), 1):
            rec = fut.result()
            ok = rec.get("content")
            print(f"[{i}/{len(jobs)}] {rec['arm']} {rec['topic']}#{rec['run']} -> "
                  f"{'ok ' + str(len(ok)) + ' chars' if ok else rec.get('error')}", flush=True)

    print("DONE", flush=True)


if __name__ == "__main__":
    main()
