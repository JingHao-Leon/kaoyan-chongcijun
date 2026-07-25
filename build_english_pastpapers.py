#!/usr/bin/env python3
"""Extract the original Use of English and Reading sections into a study page."""
from pathlib import Path
from html import escape
import subprocess

ROOT = Path(__file__).resolve().parent
PDF_ROOT = ROOT.parents[1] / "11408_zhenti" / "yingyu1"
OUT = ROOT / "english_pastpapers.html"

cards = []
for year in range(2014, 2025):
    pdf = PDF_ROOT / f"yingyu1_{year}.pdf"
    if not pdf.exists():
        continue
    result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, errors="ignore")
    text = result.stdout
    if not text.strip():
        body = "该年份 PDF 为图片版，暂时无法可靠提取文字。请直接打开原始 PDF 查看。"
    else:
        start = text.find("Section I")
        end = text.find("Section III")
        if start < 0:
            start = 0
        if end < 0:
            end = len(text)
        body = text[start:end].strip()
        if year == 2017 and "Financial regulators in Britain" in body:
            body = "你提供的 2017 PDF 内容与 2019 Text 1 重复，暂不作为 2017 原文依据。\n\n" + body
        if len(body) > 180000:
            body = body[:180000] + "\n\n[文本过长，完整内容请打开原始 PDF]"
    link = f"../../11408_zhenti/yingyu1/yingyu1_{year}.pdf"
    cards.append(f'<details><summary>{year} 年英语一：完形 + 阅读 + 新题型原文</summary><p><a href="{link}" target="_blank">打开该年度原始 PDF ↗</a></p><pre>{escape(body)}</pre></details>')

html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>历年英语一真题原文库 | 考研冲刺君</title><link rel="stylesheet" href="assets/style.css"><style>
body{background:#fafbfc;color:#151824;font-family:Inter,-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}.paper-wrap{max-width:1180px;margin:0 auto;padding:42px 24px 80px}.paper-wrap h1{font-size:34px;margin:14px 0 8px}.paper-wrap>p{color:#818798;margin:0 0 24px}.paper-note{padding:14px 16px;background:#fff8e9;border:1px solid #f3ddb1;color:#876522;border-radius:10px;font-size:13px;margin-bottom:20px}.paper-note a,.paper-wrap details a{color:#4566e8}.paper-wrap details{background:#fff;border:1px solid #e7e9ef;border-radius:12px;margin:12px 0;overflow:hidden}.paper-wrap summary{cursor:pointer;padding:16px 18px;font-weight:800;color:#30374a}.paper-wrap details[open] summary{border-bottom:1px solid #e7e9ef;background:#f7f8fb}.paper-wrap details>p{padding:0 18px;margin:14px 0;font-size:12px}.paper-wrap pre{white-space:pre-wrap;word-break:break-word;max-height:720px;overflow:auto;margin:0;padding:18px;background:#fbfcfe;color:#394154;font:12px/1.75 ui-monospace,SFMono-Regular,Menlo,monospace}.back{color:#4566e8;text-decoration:none;font-size:13px}@media(max-width:700px){.paper-wrap{padding:28px 14px}.paper-wrap h1{font-size:27px}}
</style></head><body><nav class="top-nav"><a href="index.html" class="nav-brand"><span class="logo">🏆</span><span>考研冲刺君</span></a><ul class="nav-links"><li><a href="index.html">首页</a></li><li><a href="english1.html" class="active">英语一</a></li><li><a href="english5000.html">5000词库</a></li></ul></nav><main class="paper-wrap"><a class="back" href="english1.html">← 返回英语一知识体系</a><h1>历年英语一真题原文库</h1><p>按年份展开，查看完形填空、阅读理解和新题型的原文。建议先独立做题，再回到英语一页面看分类解析。</p><div class="paper-note">原文来自工作区提供的历年真题 PDF。2017 文件与 2019 内容重复，2020 文件为图片版，页面已明确标注；完整试卷可打开原始 PDF 查看。</div>__CARDS__</main></body></html>'''.replace("__CARDS__", "".join(cards))
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(cards)} years")
