from pathlib import Path
import re

p = Path(__file__).resolve().parent / "math1.html"
s = p.read_text(encoding="utf-8")
# 2024 试卷页码：1-4题在第1页，5-10题第2页，11-16题第3页，17-19题第4页，20-22题第5页。
pages = [1, 1, 4, 1, 3, 4, 4, 5, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 5, 5, None]
pattern = re.compile(r'(<div class="chapter-original-question"><details><summary>)(2024 年对应原题)(</summary>).*?(</details></div>)', re.S)
idx = 0
def repl(m):
    global idx
    page = pages[idx]
    idx += 1
    if page is None:
        summary = "2021 年对应原题"
        content = '<p>该章在 2024 年没有单独对应题目，补充展示 2021 年假设检验真题原图。</p><img src="images/math_papers/2021/page-2.png" alt="2021年数学一假设检验原题" loading="lazy">'
    else:
        summary = "2024 年对应原题原图"
        content = f'<p>以下为 PDF 原题页面截图，公式和选项保持原貌，避免文字提取造成方框或公式错位。</p><img src="images/math_papers/2024/page-{page}.png" alt="2024年数学一原题第{page}页" loading="lazy">'
    link = '<p><a href="../../11408_zhenti/shuxue1/shuxue1_2024.pdf" target="_blank">打开原始 PDF ↗</a></p>'
    return m.group(1) + summary + m.group(3) + content + link + m.group(4)
s2 = pattern.sub(repl, s)
if idx != len(pages):
    raise SystemExit(f"expected {len(pages)} blocks, found {idx}")
style = '<style>.chapter-original-question img{display:block;max-width:100%;width:760px;margin:12px 0;border:1px solid #e2e5ee;border-radius:8px;background:#fff}.chapter-original-question p{color:#687083;font-size:13px}</style>'
s2 = s2.replace('</head>', style + '</head>', 1)
p.write_text(s2, encoding="utf-8")
print(f"replaced {idx} extracted texts with original page images")
