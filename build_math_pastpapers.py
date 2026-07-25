from html import escape
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PDF_ROOT = ROOT.parent / "11408_zhenti" / "shuxue1"
OUT = ROOT / "website" / "math_pastpapers.html"

items = []
for year in range(2014, 2025):
    pdf = PDF_ROOT / f"shuxue1_{year}.pdf"
    if not pdf.exists():
        body = "工作区暂未找到该年份 PDF。"
    else:
        result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True)
        body = result.stdout.decode("utf-8", errors="replace").strip()
        if not body:
            body = "该年份 PDF 为图片版，暂时无法可靠提取文字。请打开下方原始 PDF 查看原题。"
    link = f"../../11408_zhenti/shuxue1/shuxue1_{year}.pdf"
    items.append(f'<details><summary>{year} 年数学一原题</summary><p><a href="{link}" target="_blank">打开该年度原始 PDF ↗</a></p><pre>{escape(body)}</pre></details>')

html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>数学一历年真题原题库 | 考研冲刺君</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f7fb;color:#202331;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}.top{background:#151824;color:#fff;padding:16px 5vw;display:flex;justify-content:space-between;align-items:center}.top a{color:#cbd3ff;text-decoration:none}main{max-width:1100px;margin:0 auto;padding:28px 5vw 80px}h1{font-size:32px;margin:10px 0}.note{background:#fff8e7;border:1px solid #f0d28c;padding:14px 16px;border-radius:12px;margin:18px 0}details{background:#fff;border:1px solid #e2e5ee;border-radius:12px;padding:12px 15px;margin:10px 0}summary{cursor:pointer;font-weight:700}pre{white-space:pre-wrap;max-height:720px;overflow:auto;background:#fafbfe;border:1px solid #edf0f5;border-radius:8px;padding:14px;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,monospace}a{color:#3857d7}@media(max-width:600px){h1{font-size:26px}main{padding-left:16px;padding-right:16px}}
</style></head><body><header class="top"><strong>考研冲刺君 · 数学一真题</strong><nav><a href="index.html">首页</a>　<a href="math1.html">数学一知识体系</a></nav></header><main><p><a href="math1.html">← 返回数学一知识体系</a></p><h1>数学一历年真题原题库</h1><p>本页用于配合数学页面各章节的“真题速查”。先看章节考点，再按年份展开原题；做完后回到知识点分类复盘。</p><div class="note"><b>资料说明：</b>原题来自工作区提供的数学一真题 PDF。部分年份是扫描图片版，无法直接提取文字，但仍保留原始 PDF 入口。</div>''' + ''.join(items) + '''</main></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(items)} years")
