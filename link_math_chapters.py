from pathlib import Path
import re

p = Path(__file__).resolve().parent / "math1.html"
s = p.read_text(encoding="utf-8")
pattern = re.compile(r'(<div class="chapter-original-question">.*?</div>)(?!<p class="chapter-all-years-link">)', re.S)
idx = 0
def repl(m):
    global idx
    idx += 1
    return m.group(1) + f'<p class="chapter-all-years-link"><a href="math_chapter_lookup.html#chapter-{idx}">查看本章 2014—2024 全年份原题与解析 →</a></p>'
s = pattern.sub(repl, s)
style = '<style>.chapter-all-years-link{margin:10px 0 18px}.chapter-all-years-link a{color:#3857d7;font-weight:700}</style>'
s = s.replace('</head>', style + '</head>', 1)
p.write_text(s, encoding="utf-8")
print(f"linked {idx} chapter lookups")
