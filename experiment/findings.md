# 小实验结果：多模型中文 AI 味量化

有效样本 108 篇（7+2 档位 × 4 题型 × 3 次；剔除过短 0 条、空/报错 67 条）

## 模型排名（按 AI味标记词 每千字，降序）

| 模型 | 样本 | 标记词/千字 | 公文黑话 | 衔接套话 | 意义拔高 | 抒情腔 | 句长CV | 句均长 |
|---|---|---|---|---|---|---|---|---|
| gemini-3.7-flash | 12 | 10.35 | 0.0 | 1.74 | 0.28 | 6.9 | 0.61 | 31.64 |
| claude-sonnet-5 | 12 | 7.91 | 0.0 | 2.95 | 0.81 | 3.76 | 0.5 | 30.31 |
| deepseek-v4-flash | 12 | 6.34 | 0.0 | 0.31 | 0.61 | 4.81 | 0.47 | 25.95 |
| gemini-2.5-flash | 12 | 6.21 | 0.0 | 1.33 | 0.78 | 3.54 | 0.39 | 29.85 |
| gpt-5.6-terra | 12 | 5.24 | 0.0 | 1.68 | 0.0 | 3.28 | 0.46 | 27.05 |
| claude-haiku-4.5 | 12 | 4.29 | 0.0 | 1.18 | 1.44 | 1.68 | 0.42 | 24.47 |
| claude-sonnet-4.5 | 12 | 4.01 | 0.0 | 0.89 | 0.0 | 2.35 | 0.43 | 28.12 |
| gemini-2.5-flash-nothink | 12 | 3.96 | 0.0 | 1.07 | 0.91 | 1.79 | 0.42 | 30.62 |
| glm-5.3-flash | 12 | 3.7 | 0.0 | 1.57 | 0.0 | 1.84 | 0.51 | 25.23 |

## 句式模式（每千字）

| 模型 | 不仅…而且 | 不是…而是 | 让我们 | 拭目以待 | 在…时代 | 随着…的发展 | 排比三连 |
|---|---|---|---|---|---|---|---|
| gemini-3.7-flash | 0.81 | 0.0 | 0.0 | 0.0 | 0.3 | 0.59 | 0.0 |
| claude-sonnet-5 | 0.91 | 0.23 | 0.0 | 0.0 | 0.0 | 0.41 | 1.54 |
| deepseek-v4-flash | 0.0 | 2.05 | 0.45 | 0.0 | 0.0 | 0.0 | 1.45 |
| gemini-2.5-flash | 0.64 | 0.63 | 0.19 | 0.0 | 0.0 | 0.0 | 1.36 |
| gpt-5.6-terra | 0.0 | 0.0 | 0.0 | 0.0 | 0.29 | 0.84 | 1.68 |
| claude-haiku-4.5 | 0.38 | 1.32 | 0.0 | 0.0 | 0.0 | 0.0 | 1.9 |
| claude-sonnet-4.5 | 0.0 | 0.76 | 0.0 | 0.0 | 0.51 | 0.0 | 1.59 |
| gemini-2.5-flash-nothink | 1.6 | 0.88 | 0.0 | 0.0 | 0.21 | 0.0 | 3.4 |
| glm-5.3-flash | 0.0 | 0.86 | 0.0 | 0.0 | 0.0 | 0.53 | 3.85 |

## 题型 × 模型 明细（标记词/千字）

| 模型 :: 题型 | 标记词/千字 | 句长CV |
|---|---|---|
| gemini-3.7-flash :: marketing | 20.87 | 0.37 |
| deepseek-v4-flash :: marketing | 13.69 | 0.55 |
| gpt-5.6-terra :: marketing | 13.11 | 0.5 |
| claude-sonnet-5 :: viewpoint | 12.64 | 0.34 |
| gemini-2.5-flash :: marketing | 9.74 | 0.44 |
| gemini-3.7-flash :: viewpoint | 9.18 | 0.9 |
| gemini-2.5-flash-nothink :: marketing | 8.43 | 0.4 |
| claude-sonnet-4.5 :: marketing | 8.39 | 0.41 |
| claude-sonnet-5 :: marketing | 8.31 | 0.53 |
| glm-5.3-flash :: marketing | 7.34 | 0.54 |
| gemini-3.7-flash :: casual | 6.73 | 0.77 |
| gpt-5.6-terra :: viewpoint | 6.73 | 0.31 |
| claude-sonnet-5 :: casual | 6.72 | 0.65 |
| glm-5.3-flash :: viewpoint | 6.28 | 0.4 |
| claude-haiku-4.5 :: reading | 5.76 | 0.35 |
| deepseek-v4-flash :: casual | 5.55 | 0.46 |
| gemini-2.5-flash :: casual | 5.47 | 0.33 |
| gemini-2.5-flash :: viewpoint | 4.96 | 0.4 |
| claude-haiku-4.5 :: viewpoint | 4.71 | 0.29 |
| gemini-2.5-flash :: reading | 4.69 | 0.37 |
| gemini-3.7-flash :: reading | 4.61 | 0.41 |
| claude-sonnet-5 :: reading | 3.96 | 0.48 |
| deepseek-v4-flash :: viewpoint | 3.76 | 0.54 |
| claude-haiku-4.5 :: casual | 3.7 | 0.44 |
| claude-sonnet-4.5 :: viewpoint | 3.57 | 0.37 |
| claude-sonnet-4.5 :: reading | 3.07 | 0.43 |
| claude-haiku-4.5 :: marketing | 3.0 | 0.59 |
| gemini-2.5-flash-nothink :: casual | 2.98 | 0.48 |
| deepseek-v4-flash :: reading | 2.34 | 0.32 |
| gemini-2.5-flash-nothink :: reading | 2.25 | 0.35 |
| gemini-2.5-flash-nothink :: viewpoint | 2.17 | 0.45 |
| glm-5.3-flash :: reading | 1.18 | 0.46 |
| gpt-5.6-terra :: reading | 1.13 | 0.33 |
| claude-sonnet-4.5 :: casual | 0.99 | 0.52 |
| glm-5.3-flash :: casual | 0.0 | 0.63 |
| gpt-5.6-terra :: casual | 0.0 | 0.69 |