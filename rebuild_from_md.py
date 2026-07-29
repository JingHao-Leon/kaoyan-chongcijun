#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从更新后的 Markdown 知识体系重建网站课程页面。
保留现有站点模板（导航/侧栏/KaTeX/交互脚本），只重建内容区与侧栏目录，
并把旧页面中的配图按标题位置回迁到新页面。

用法（需用含 markdown 库的 Python 运行）：
  "$DAIMON_USER_PYTHON" rebuild_from_md.py [math|english|cs408|408split|all]
"""
import os, re, sys, json
import markdown

BASE = "/Users/ahs/Documents/kimi/workspace/考研冲刺君"
WEB = os.path.join(BASE, "website")

MD_MATH = os.path.join(BASE, "数学一/数学一知识体系全解.md")
MD_ENG = os.path.join(BASE, "英语一/英语一知识体系全解.md")
MD_408 = os.path.join(BASE, "408专业课/408知识体系全解.md")

# ------------------------------------------------------------ Markdown 转换
def convert(md_text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
    body = md.convert(md_text)
    return body, md.toc_tokens

def flatten_tokens(tokens):
    """toc_tokens 是按层级嵌套的，拍平为文档顺序列表。"""
    out = []
    def walk(ts):
        for t in ts:
            out.append(t)
            walk(t.get("children", []))
    walk(tokens)
    return out

def toc_html(tokens, max_level=2):
    items = [
        f'<li><a href="#{t["id"]}" class="toc-h{t["level"]}">{t["name"]}</a></li>'
        for t in flatten_tokens(tokens) if t["level"] <= max_level
    ]
    return "\n      ".join(items)

def _norm(s):
    return re.sub(r"[\s\-–—_*:：()（）,，、.。]+", "", re.sub(r"<[^>]+>", "", s)).lower()

def repair_anchors(body, tokens):
    """把 md 自带目录里的中文锚点链接重映射到转换后的真实 id（_N）。"""
    name2id = {}
    for t in flatten_tokens(tokens):
        name2id.setdefault(_norm(t["name"]), t["id"])
    def repl(m):
        href = m.group(1)
        if href.startswith("_"):
            return m.group(0)
        key = _norm(href)
        nid = name2id.get(key)
        if not nid:
            # 前缀兜底：md 目录锚点可能省略标题括号后缀（如 #第八章-假设检验）
            for name, tid in name2id.items():
                if name.startswith(key) and len(key) >= 4:
                    nid = tid
                    break
        return f'href="#{nid}"' if nid else m.group(0)
    return re.sub(r'href="#([^"]+)"', repl, body)

# ------------------------------------------------------------ 配图回迁
HEAD_RE = r"<h[1-3][^>]*>(.*?)</h[1-3]>"
IMG_RE = r'<div style="text-align:center[^>]*><img src="images/[^"]+"[^>]*></div>'

def scrape_images(html_path):
    """从现有页面抓取自由配图（排除真题面板内图片）。
    返回 [(所属章h2规范化文本|None, 所属标题规范化文本|None, img_div)]。
    同时记录章(h2)与最近标题(h1/h2/h3)，回插时双重定位，避免同名标题串章。"""
    if not os.path.exists(html_path):
        return []
    text = open(html_path, encoding="utf-8").read()
    m = re.search(r'<main class="content">(.*?)</main>', text, re.S)
    if not m:
        return []
    content = m.group(1)
    # 剔除真题嵌入面板，避免把面板里的图当成自由配图
    content = re.sub(r'<div class="chapter-original-question">.*?</details></div>', "", content, flags=re.S)
    content = re.sub(r'<details class="chapter-inline-papers">.*?</details>', "", content, flags=re.S)
    content = re.sub(r"<!-- 408-PAPERS-START -->.*?<!-- 408-PAPERS-END -->", "", content, flags=re.S)
    items, cur_head, cur_ch = [], None, None
    for t in re.finditer(r"<h([1-3])[^>]*>(.*?)</h\1>|" + IMG_RE, content, re.S):
        if t.group(2) is not None:
            level, text_h = t.group(1), _norm(t.group(2))
            cur_head = text_h
            if level == "2":
                cur_ch = text_h
        elif "math_papers/" not in t.group(0):
            items.append((cur_ch, cur_head, t.group(0)))
    return items

def reinsert_images(body, items):
    """把配图插回新页面：页首图（无标题锚点）插到 h1 之后；
    其余要求「章(h2)与标题」同时匹配才插入，防止同名 h3 跨章错位。"""
    restored = 0
    for chapter, heading, img in items:
        if img in body:
            continue
        if heading is None:
            m = re.search(r"<h1[^>]*>.*?</h1>", body, re.S)
            if m:
                body = body[: m.end()] + "\n" + img + body[m.end():]
                restored += 1
            continue
        cur_ch = None
        for m in re.finditer(r"<h([1-3])[^>]*>(.*?)</h\1>", body, re.S):
            level, text_h = m.group(1), _norm(m.group(2))
            if level == "2":
                cur_ch = text_h
            if text_h == heading and (chapter is None or cur_ch == chapter):
                body = body[: m.end()] + "\n" + img + body[m.end():]
                restored += 1
                break
    return body, restored

# ------------------------------------------------------------ 页面模板
NAV = [
    ("index.html", "首页", "home"),
    ("math1.html", "数学一", "math"),
    ("english1.html", "英语一", "english"),
    ("ds.html", "数据结构", "ds"),
    ("co.html", "计组", "co"),
    ("os.html", "OS", "os"),
    ("cn.html", "计网", "cn"),
    ("llm_architectures.html", "LLM 架构", "llm"),
]

# ------------------------------------------------------------ SEO（AEO/GEO）
SEO_BASE = "https://zehaowang.xin"
SEO_TODAY = "2026-07-29"
SEO_PUBLISHED = "2026-07-01"
SEO_META = {
    "math1.html": "数学一知识体系全解：高等数学、线性代数、概率论与数理统计 22 章完整讲解，难点图解、例题解析与历年真题速查。",
    "english1.html": "考研英语一知识体系全解：阅读六大题型方法论、完形与翻译技巧、大小作文模板、5000 核心词汇与历年真题原文库。",
    "cs408.html": "408 计算机学科专业基础知识体系全解：数据结构、计算机组成原理、操作系统、计算机网络四门课考点、例题与真题速查。",
    "ds.html": "408 数据结构全解：线性表、栈队列、树、图、查找、排序 7 章知识体系，每章知识点图解 + 6 道例题卡 + 历年真题。",
    "co.html": "408 计算机组成原理全解：数据表示、存储系统、指令系统、CPU、总线、I/O 7 章知识体系，知识点图解 + 例题卡 + 历年真题。",
    "os.html": "408 操作系统全解：进程管理、内存管理、文件管理、I/O 管理 5 章知识体系，知识点图解 + 例题卡 + 历年真题。",
    "cn.html": "408 计算机网络全解：体系结构、物理层、数据链路层、网络层、传输层、应用层 6 章知识体系，知识点图解 + 例题卡 + 历年真题。",
}

def seo_head(out_name, title):
    desc = SEO_META.get(out_name)
    if not desc:
        return ""
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": title,
        "description": desc, "inLanguage": "zh-CN",
        "mainEntityOfPage": f"{SEO_BASE}/{out_name}",
        "datePublished": SEO_PUBLISHED, "dateModified": SEO_TODAY,
        "author": {"@type": "Organization", "name": "考研冲刺君", "url": SEO_BASE},
        "publisher": {"@type": "Organization", "name": "考研冲刺君", "url": SEO_BASE},
    }, ensure_ascii=False)
    return (f'<meta name="description" content="{desc}">\n'
            f'<link rel="canonical" href="{SEO_BASE}/{out_name}">\n'
            f'<link rel="alternate" type="application/rss+xml" title="考研冲刺君更新" href="feed.xml">\n'
            f'<meta property="article:modified_time" content="{SEO_TODAY}T00:00:00+08:00">\n'
            f'<script type="application/ld+json">{ld}</script>')

SEO_DATE_NOTE = ('<p class="update-note" style="margin-top:28px;padding-top:12px;'
                 'border-top:1px dashed #d0d4dc;color:#8a8f98;font-size:12.5px;">'
                 '最后更新：2026-07-29 · 考研冲刺君团队整理 · 内容持续维护</p>')

def render_page(title, body, toc, active, course=True, out_name=""):
    nav_links = "\n".join(
        f'    <li><a href="{href}" class="{"active" if key == active else ""}">{label}</a></li>'
        for href, label, key in NAV
    )
    course_scripts = ""
    if course:
        course_scripts = ('<script defer src="assets/chapter-mode.js"></script>'
                          '<script defer src="assets/interactive-labs.js"></script>')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 考研冲刺君</title>
{seo_head(out_name, title)}
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters: [
    {{left: '$$', right: '$$', display: true}},
    {{left: '$', right: '$', display: false}}
  ]}});"></script>
<script defer src="assets/navigation.js"></script>{course_scripts}</head>
<body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">
    <span class="logo">🏆</span>
    <span>考研冲刺君</span>
  </a>
  <ul class="nav-links">
{nav_links}
  </ul>
</nav>

<div class="main-layout">
  <aside class="sidebar">
    <div class="sidebar-title">目录</div>
    <ul class="toc-list">
      {toc}
    </ul>
  </aside>
  <main class="content">
{body}
{SEO_DATE_NOTE if seo_head(out_name, title) else ""}
  </main>
</div>

<button class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">↑</button>

<script>
// 目录高亮
document.addEventListener('scroll', function() {{
  const headings = document.querySelectorAll('h1[id], h2[id], h3[id], h4[id]');
  const tocLinks = document.querySelectorAll('.toc-list a');
  let current = '';
  headings.forEach(h => {{
    if (h.getBoundingClientRect().top <= 80) current = h.id;
  }});
  tocLinks.forEach(a => {{
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  }});
  document.querySelector('.back-to-top').style.display = window.scrollY > 500 ? 'flex' : 'none';
}});
</script>
</body>
</html>
"""

# ------------------------------------------------------------ 构建
def build(md_text, out_name, title, active, course=True, carry_images=True, prepend_h1=None, toc_depth=2):
    old = os.path.join(WEB, out_name)
    images = scrape_images(old) if carry_images else []
    body, tokens = convert(md_text)
    toc = toc_html(tokens, toc_depth)
    if prepend_h1:
        body = f'<h1 id="top">{prepend_h1}</h1>\n' + body
        toc = f'<li><a href="#top" class="toc-h1">{prepend_h1}</a></li>\n      ' + toc
    body = repair_anchors(body, tokens)
    body, n_img = reinsert_images(body, images)
    html = render_page(title, body, toc, active, course, out_name=out_name)
    with open(old, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[build] {out_name}: {len(html)//1024} KB, 回迁配图 {n_img}/{len(images)} 张")

def build_math():
    build(open(MD_MATH, encoding="utf-8").read(), "math1.html", "数学一知识体系全解", "math")

def build_english():
    build(open(MD_ENG, encoding="utf-8").read(), "english1.html", "英语一知识体系全解", "english")

def build_cs408():
    build(open(MD_408, encoding="utf-8").read(), "cs408.html", "408知识体系全解", "", course=False)

SPLITS = [
    ("ds.html", "408 数据结构", "ds", "# 第一部分：数据结构"),
    ("co.html", "408 计算机组成原理", "co", "# 第二部分：计算机组成原理"),
    ("os.html", "408 操作系统", "os", "# 第三部分：操作系统"),
    ("cn.html", "408 计算机网络", "cn", "# 第四部分：计算机网络"),
]

def build_408split():
    text = open(MD_408, encoding="utf-8").read()
    marks = [(name, text.find(h)) for _, _, _, h in SPLITS for name, h in [(h[0], h[1])]]
    starts = [(h, text.find(h)) for _, _, _, h in SPLITS]
    appendix = text.find("## 附录：")
    for i, (out, title, active, header) in enumerate(SPLITS):
        start = starts[i][1]
        end = starts[i + 1][1] if i + 1 < len(starts) else (appendix if appendix > 0 else len(text))
        assert start >= 0 and end > start, f"split boundary broken for {out}"
        part = text[start:end]
        # 去掉分部标题行，用自定义 h1 替代
        part = re.sub(r"^# 第[一二三四]部分：[^\n]*\n", "", part, count=1)
        build(part, out, title, active, prepend_h1=title, toc_depth=3)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("math", "all"):
        build_math()
    if which in ("english", "all"):
        build_english()
    if which in ("cs408", "all"):
        build_cs408()
    if which in ("408split", "all"):
        build_408split()
    print("done.")
