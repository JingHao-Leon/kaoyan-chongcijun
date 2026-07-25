from pathlib import Path
import re

path = Path(__file__).with_name("math1.html")
html = path.read_text(encoding="utf-8")

old_css = '<style>.chapter-all-years-link{margin:10px 0 18px}.chapter-all-years-link a{color:#3857d7;font-weight:700}</style>'
new_css = '''<style>.chapter-all-years-link{margin:10px 0 18px}.chapter-all-years-link a{color:#3857d7;font-weight:700}.chapter-inline-papers{margin:12px 0 22px;border:1px solid #d9e0f5;border-radius:10px;background:#f8faff;padding:10px 14px}.chapter-inline-papers summary{cursor:pointer;font-weight:700;color:#263a8d}.chapter-inline-papers p{color:#687083;font-size:13px}.chapter-inline-papers iframe{display:block;width:100%;height:680px;border:1px solid #e2e5ee;border-radius:8px;background:#fff}</style>'''
if old_css not in html:
    raise SystemExit("expected stylesheet marker not found")
html = html.replace(old_css, new_css, 1)

pattern = re.compile(r'<p class="chapter-all-years-link"><a href="math_chapter_lookup\.html#chapter-(\d+)">查看本章 2014—2024 全年份原题与解析 →</a></p>')

def panel(match):
    chapter = match.group(1)
    return f'''<details class="chapter-inline-papers">
<summary>展开查看本章 2014—2024 真题速查与原题页</summary>
<p>建议完成上方知识点与本章速查表后，再在此按年份展开真题。题目只在实际命中的考点下展示。</p>
<iframe src="math_chapter_lookup.html#chapter-{chapter}" title="本章分年真题速查" loading="lazy"></iframe>
<p><a href="math_chapter_lookup.html#chapter-{chapter}" target="_blank">在独立页面查看本章真题 ↗</a></p>
</details>'''

html, count = pattern.subn(panel, html)
if count != 22:
    raise SystemExit(f"expected 22 chapter links, replaced {count}")
path.write_text(html, encoding="utf-8")
print(f"embedded {count} chapter paper panels")
