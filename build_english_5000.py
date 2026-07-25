#!/usr/bin/env python3
"""Build a searchable 5000-word English study page from a frequency list."""
from pathlib import Path
from html import escape
from wordfreq import top_n_list, zipf_frequency

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "english5000.html"

words = []
seen = set()
for raw in top_n_list("en", 18000):
    word = raw.lower()
    if not word.isalpha() or not (2 <= len(word) <= 15) or word in seen:
        continue
    # Keep study words rather than names, abbreviations, or internet fragments.
    if not any(c in word for c in "aeiou"):
        continue
    seen.add(word)
    words.append(word)
    if len(words) == 5000:
        break

rows = []
for i, word in enumerate(words, 1):
    level = "核心精背" if i <= 2000 else "扩展识别"
    level_class = "core" if i <= 2000 else "extended"
    rows.append(f'<tr data-word="{escape(word)}"><td>{i:04d}</td><td><strong>{escape(word)}</strong></td><td><span class="level {level_class}">{level}</span></td><td>{zipf_frequency(word, "en"):.1f}</td><td>结合真题语境记录词义与搭配</td></tr>')

html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>考研英语一 5000 词库 | 考研冲刺君</title><link rel="stylesheet" href="assets/style.css"><style>
body{{background:#fafbfc;color:#151824;font-family:Inter,-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}.vocab-wrap{{max-width:1120px;margin:0 auto;padding:42px 24px 80px}}.vocab-head{{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:28px}}.vocab-head h1{{font-size:36px;margin:8px 0}}.vocab-head p{{color:#818798;margin:0}}.back-link{{color:#4566e8;text-decoration:none;font-size:13px}}.vocab-tools{{display:flex;gap:10px;margin-bottom:18px}}.vocab-tools input{{flex:1;padding:13px 16px;border:1px solid #e7e9ef;border-radius:10px;font:inherit;background:#fff}}.vocab-tools select{{border:1px solid #e7e9ef;border-radius:10px;background:#fff;padding:0 12px;color:#596174}}.vocab-summary{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}}.vocab-summary span,.level{{display:inline-block;font-size:11px;border-radius:99px;padding:5px 9px}}.vocab-summary span{{background:#eef1ff;color:#4566e8}}.level.core{{background:#e9f8ef;color:#3a9b6c}}.level.extended{{background:#f0f2f6;color:#717a8e}}.vocab-table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e7e9ef;border-radius:14px;overflow:hidden}}.vocab-table th,.vocab-table td{{padding:12px 15px;border-bottom:1px solid #edf0f4;text-align:left;font-size:13px}}.vocab-table th{{background:#f7f8fb;color:#818798;font-size:11px}}.vocab-table td:first-child,.vocab-table td:nth-child(4){{color:#9aa1b1;width:80px}}.vocab-table tr:hover{{background:#fafbff}}@media(max-width:700px){{.vocab-head{{display:block}}.vocab-head h1{{font-size:28px}}.vocab-tools{{display:block}}.vocab-tools input,.vocab-tools select{{width:100%;height:44px;margin-bottom:8px}}.vocab-table th:nth-child(4),.vocab-table td:nth-child(4),.vocab-table th:nth-child(5),.vocab-table td:nth-child(5){{display:none}}}}
</style></head><body><nav class="top-nav"><a href="index.html" class="nav-brand"><span class="logo">🏆</span><span>考研冲刺君</span></a><ul class="nav-links"><li><a href="index.html">首页</a></li><li><a href="english1.html" class="active">英语一</a></li><li><a href="english1.html#_18">词汇与语法</a></li></ul></nav><main class="vocab-wrap"><div class="vocab-head"><div><a class="back-link" href="english1.html">← 返回英语一知识体系</a><h1>考研英语一 5000 词库</h1><p>前 2000 词建议做到“看到即反应”，后 3000 词先完成识别，再结合真题补充词义和搭配。</p></div><div class="vocab-summary"><span>5000 词</span><span>2000 核心</span><span>3000 扩展</span></div></div><div class="vocab-tools"><input id="search" placeholder="搜索单词，例如 approach / culture"><select id="level"><option value="all">全部词汇</option><option value="core">核心精背</option><option value="extended">扩展识别</option></select></div><table class="vocab-table"><thead><tr><th>序号</th><th>单词</th><th>层级</th><th>频率</th><th>学习提示</th></tr></thead><tbody>{''.join(rows)}</tbody></table></main><script>const input=document.querySelector('#search'),level=document.querySelector('#level');function filter(){{const q=input.value.toLowerCase(),l=level.value;document.querySelectorAll('tbody tr').forEach(row=>{{const hit=row.dataset.word.includes(q),ok=l==='all'||row.querySelector('.level').classList.contains(l);row.hidden=!(hit&&ok)}})}}input.addEventListener('input',filter);level.addEventListener('change',filter);</script></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(words)} words")
