from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parent.parent
html_path = ROOT / "website" / "math1.html"
txt = (ROOT / "tmp" / "pdfs" / "math1" / "shuxue1_2024.txt").read_text(encoding="utf-8", errors="ignore")
blocks = {}
matches = list(re.finditer(r"【(\d+)】", txt))
for i, m in enumerate(matches):
    q = int(m.group(1))
    if q > 22:
        continue
    end = matches[i + 1].start() if i + 1 < len(matches) else len(txt)
    body = txt[m.end():end]
    body = body.split("【答案】", 1)[0].strip()
    blocks[q] = f"【{q}】{body}"

mapping = [1, 4, 17, 2, 12, 18, 17, 20, 5, 7, 6, 5, 7, 15, 16, 8, 9, 9, 10, 22, 22, None]
p = html_path
s = p.read_text(encoding="utf-8")
pattern = re.compile(r'(<div class="chapter-original-question"><details><summary>2024 年对应原题</summary><p>).*?(</p><p><a href="\.\./\.\./11408_zhenti/shuxue1/shuxue1_2024\.pdf")', re.S)
idx = 0
def repl(m):
    global idx
    q = mapping[idx]
    idx += 1
    if q is None:
        text = "本章在 2024 年试卷中没有单独设置对应题目。请打开历年原题库，按本章知识点继续检索相关年份原题。"
    else:
        text = f"2024 年数学一第 {q} 题（PDF 原题）：\n{blocks.get(q, '该题暂未成功提取，请打开原始 PDF。')}"
    return m.group(1) + '<pre style="white-space:pre-wrap;margin:0;background:#fafbfe;padding:12px;border-radius:8px">' + escape(text) + '</pre>' + m.group(2)
s2 = pattern.sub(repl, s)
if idx != len(mapping):
    raise SystemExit(f"expected {len(mapping)} blocks, found {idx}")
p.write_text(s2, encoding="utf-8")
print(f"replaced {idx} chapter summaries with PDF question text")
