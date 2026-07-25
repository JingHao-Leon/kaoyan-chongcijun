#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考研冲刺君 - 网站生成脚本 (Notion风格)
"""

import os
import markdown

BASE_DIR = "/Users/ahs/Documents/kimi/workspace/考研冲刺君"
WEBSITE_DIR = os.path.join(BASE_DIR, "website")
ASSETS_DIR = os.path.join(WEBSITE_DIR, "assets")

os.makedirs(WEBSITE_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ============================================================
# Notion 风格 CSS
# ============================================================
CSS = """
/* ============================================
   考研冲刺君 - Notion 风格主题
   特点：白色背景、大量留白、简洁排版
   ============================================ */

:root {
  --bg-page: #ffffff;
  --bg-sidebar: #f7f6f3;
  --bg-hover: #efefef;
  --bg-code: #f7f6f3;
  --bg-callout: #f7f6f3;
  --bg-table-header: #f7f6f3;
  --bg-card: #ffffff;

  --text-title: #37352f;
  --text-body: #37352f;
  --text-gray: #6b6b6b;
  --text-light: #9ca3af;
  --text-link: #2eaadc;
  --text-link-hover: #0d7aac;

  --border: #e3e2e0;
  --border-light: #f0f0f0;

  --accent-red: #e03e3e;
  --accent-orange: #d9730d;
  --accent-yellow: #dfab01;
  --accent-green: #0f7b6c;
  --accent-blue: #2eaadc;
  --accent-purple: #6940a5;
  --accent-pink: #e14790;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', sans-serif;
  background: var(--bg-page);
  color: var(--text-body);
  line-height: 1.6;
  overflow-x: hidden;
}

/* ============================================
   顶部导航
   ============================================ */
.top-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 44px;
  background: var(--bg-page);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  z-index: 1000;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-title);
  text-decoration: none;
}

.nav-brand .logo { font-size: 18px; }

.nav-links {
  display: flex;
  gap: 2px;
  list-style: none;
}

.nav-links a {
  color: var(--text-gray);
  text-decoration: none;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}

.nav-links a:hover {
  color: var(--text-title);
  background: var(--bg-hover);
}

.nav-links a.active {
  color: var(--text-title);
  background: var(--bg-hover);
  font-weight: 600;
}

/* ============================================
   主布局
   ============================================ */
.main-layout {
  display: flex;
  margin-top: 44px;
  min-height: calc(100vh - 44px);
}

/* ============================================
   侧边栏 (Notion风格)
   ============================================ */
.sidebar {
  width: 240px;
  height: calc(100vh - 44px);
  position: fixed;
  left: 0; top: 44px;
  background: var(--bg-sidebar);
  overflow-y: auto;
  padding: 8px 0 40px;
  z-index: 100;
  font-size: 14px;
}

.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: #d1d1d1; border-radius: 2px; }

.sidebar-title {
  padding: 8px 16px 6px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-light);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.toc-list { list-style: none; padding: 0; }
.toc-list li { margin: 0; }

.toc-list a {
  display: block;
  padding: 4px 16px;
  color: var(--text-gray);
  text-decoration: none;
  font-size: 13px;
  transition: all 0.1s;
  line-height: 1.5;
  border-radius: 3px;
  margin: 0 4px;
}

.toc-list a:hover {
  color: var(--text-title);
  background: rgba(55, 53, 47, 0.06);
}

.toc-list a.active {
  color: var(--text-title);
  background: rgba(55, 53, 47, 0.08);
  font-weight: 500;
}

.toc-list .toc-h1 { font-weight: 600; font-size: 14px; }
.toc-list .toc-h2 { padding-left: 20px; }
.toc-list .toc-h3 { padding-left: 32px; font-size: 12px; }
.toc-list .toc-h4 { padding-left: 44px; font-size: 12px; color: var(--text-light); }

/* ============================================
   内容区
   ============================================ */
.content {
  margin-left: 240px;
  flex: 1;
  max-width: 900px;
  padding: 40px 80px 120px;
}

/* ============================================
   标题 (Notion风格)
   ============================================ */
h1 {
  font-size: 40px;
  font-weight: 700;
  margin: 0 0 4px;
  color: var(--text-title);
  line-height: 1.2;
  letter-spacing: -0.5px;
}

h2 {
  font-size: 30px;
  font-weight: 600;
  margin: 48px 0 8px;
  color: var(--text-title);
  line-height: 1.3;
  letter-spacing: -0.3px;
  padding-bottom: 3px;
}

h3 {
  font-size: 24px;
  font-weight: 600;
  margin: 32px 0 8px;
  color: var(--text-title);
  line-height: 1.3;
}

h4 {
  font-size: 20px;
  font-weight: 600;
  margin: 24px 0 6px;
  color: var(--text-title);
  line-height: 1.3;
}

h5 {
  font-size: 16px;
  font-weight: 600;
  margin: 16px 0 4px;
  color: var(--text-title);
}

h1 a.anchor, h2 a.anchor, h3 a.anchor, h4 a.anchor {
  color: var(--text-light);
  text-decoration: none;
  margin-left: 6px;
  opacity: 0;
  font-weight: 400;
  transition: opacity 0.15s;
}
h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor { opacity: 1; }

/* ============================================
   段落和文本
   ============================================ */
p {
  margin: 6px 0;
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-body);
}

strong { font-weight: 600; color: var(--text-title); }

em { font-style: italic; color: var(--text-gray); }

/* ============================================
   引用块 (Notion callout风格)
   ============================================ */
blockquote {
  margin: 12px 0;
  padding: 12px 16px 12px 18px;
  background: var(--bg-callout);
  border-left: 3px solid #37352f;
  border-radius: 3px;
  color: var(--text-body);
}

blockquote p { margin: 4px 0; font-size: 15px; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

/* 特殊引用块 */
blockquote.alert-warning { border-left-color: var(--accent-orange); background: #fdf5e8; }
blockquote.alert-danger { border-left-color: var(--accent-red); background: #fdf2f2; }
blockquote.alert-success { border-left-color: var(--accent-green); background: #f0f7f5; }
blockquote.alert-info { border-left-color: var(--accent-blue); background: #eef7fb; }

/* ============================================
   代码块 (Notion风格)
   ============================================ */
pre {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 16px 20px;
  overflow-x: auto;
  margin: 12px 0;
  font-family: 'SFMono-Regular', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
}

code {
  font-family: 'SFMono-Regular', 'Fira Code', 'JetBrains Mono', Consolas, monospace;
  background: var(--bg-code);
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 14px;
  color: var(--accent-red);
  border: 1px solid var(--border-light);
}

pre code {
  background: transparent;
  padding: 0;
  border: none;
  color: var(--text-body);
  font-size: 14px;
}

/* ============================================
   表格 (Notion简洁表格)
   ============================================ */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 14px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid var(--border);
}

th {
  background: var(--bg-table-header);
  color: var(--text-title);
  font-weight: 600;
  text-align: left;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}

td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border-light);
  vertical-align: top;
}

tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

/* ============================================
   列表
   ============================================ */
ul, ol { margin: 8px 0 8px 24px; }
li { margin: 4px 0; font-size: 15px; }

/* 任务列表 */
ul li input[type="checkbox"] {
  margin-right: 6px;
}

/* ============================================
   水平线
   ============================================ */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 24px 0;
}

/* ============================================
   数学公式
   ============================================ */
.katex-display {
  margin: 12px 0;
  overflow-x: auto;
}

/* ============================================
   链接
   ============================================ */
a {
  color: var(--text-link);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.15s;
}
a:hover { border-bottom-color: var(--text-link); }

/* 内容区内部链接 */
.content a { word-break: break-word; }

/* ============================================
   标签/徽章
   ============================================ */
.badge {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 500;
  margin-right: 4px;
}

/* ============================================
   主页样式 (Notion风格)
   ============================================ */
.hero {
  text-align: left;
  padding: 60px 80px 40px;
  max-width: 900px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 48px;
  font-weight: 700;
  color: var(--text-title);
  margin-bottom: 8px;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 18px;
  color: var(--text-gray);
  margin-bottom: 4px;
  font-weight: 400;
}

.hero-stats {
  display: flex;
  gap: 48px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.stat-item { text-align: left; }

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-title);
  letter-spacing: -0.5px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-light);
  margin-top: 2px;
}

/* 卡片网格 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  padding: 0 80px 48px;
  max-width: 900px;
  margin: 0 auto;
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px 20px;
  text-decoration: none;
  color: var(--text-title);
  transition: all 0.2s;
  cursor: pointer;
}

.card:hover {
  background: var(--bg-sidebar);
  border-color: #c1c1c1;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.card-icon {
  font-size: 28px;
  margin-bottom: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text-title);
}

.card-desc {
  font-size: 14px;
  color: var(--text-gray);
  line-height: 1.5;
}

.card-meta {
  display: flex;
  gap: 12px;
  margin-top: 14px;
  font-size: 12px;
  color: var(--text-light);
}

/* ============================================
   回到顶部
   ============================================ */
.back-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  background: var(--bg-page);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-gray);
  font-size: 16px;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 500;
  transition: all 0.15s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.back-to-top:hover {
  background: var(--bg-hover);
  color: var(--text-title);
}

/* ============================================
   页脚
   ============================================ */
footer {
  text-align: center;
  padding: 32px;
  border-top: 1px solid var(--border);
  color: var(--text-light);
  font-size: 13px;
  max-width: 900px;
  margin: 0 auto;
}

/* ============================================
   内容页附加样式
   ============================================ */
.page-header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.page-header h1 {
  font-size: 40px;
  font-weight: 700;
  color: var(--text-title);
}

.page-header .page-meta {
  font-size: 14px;
  color: var(--text-light);
  margin-top: 8px;
}

/* emoji前缀的标题 */
h2[data-emoji]::before,
h3[data-emoji]::before {
  content: attr(data-emoji) " ";
}

/* 分节符 */
.section-divider {
  height: 1px;
  background: var(--border);
  margin: 32px 0;
}

/* ============================================
   响应式
   ============================================ */
@media (max-width: 1024px) {
  .sidebar { display: none; }
  .content { margin-left: 0; padding: 24px; }
  .card-grid { grid-template-columns: 1fr; padding: 0 24px 32px; }
  .hero { padding: 40px 24px 24px; }
  .hero h1 { font-size: 32px; }
}

@media (max-width: 768px) {
  .top-nav { padding: 0 12px; }
  .nav-links { display: none; }
  .hero-stats { flex-direction: column; gap: 16px; }
  .content { padding: 16px; }
  h1 { font-size: 28px; }
  h2 { font-size: 22px; }
  h3 { font-size: 18px; }
}

/* ============================================
   打印
   ============================================ */
@media print {
  .top-nav, .sidebar, .back-to-top { display: none !important; }
  .content { margin-left: 0; max-width: none; padding: 24px; }
  body { background: white; color: black; }
}
"""

# 写入CSS文件
css_path = os.path.join(ASSETS_DIR, "style.css")
with open(css_path, "w", encoding="utf-8") as f:
    f.write(CSS)

print(f"✅ Notion风格 CSS 写入: {css_path}")

# ============================================================
# HTML 模板 (Notion风格)
# ============================================================

def make_html(title, body_html, toc_html, active_nav=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | 考研冲刺君</title>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters: [
    {{left: '$$', right: '$$', display: true}},
    {{left: '$', right: '$', display: false}}
  ]}});"></script>
</head>
<body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">
    <span class="logo">🏆</span>
    <span>考研冲刺君</span>
  </a>
  <ul class="nav-links">
    <li><a href="index.html" class="{'active' if active_nav == 'home' else ''}">首页</a></li>
    <li><a href="math1.html" class="{'active' if active_nav == 'math' else ''}">数学一</a></li>
    <li><a href="english1.html" class="{'active' if active_nav == 'english' else ''}">英语一</a></li>
    <li><a href="cs408.html" class="{'active' if active_nav == 'cs408' else ''}">408专业课</a></li>
  </ul>
</nav>

<div class="main-layout">
  <aside class="sidebar">
    <div class="sidebar-title">目录</div>
    <ul class="toc-list">
      {toc_html}
    </ul>
  </aside>
  <main class="content">
    {body_html}
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
  // 回到顶部按钮
  document.querySelector('.back-to-top').style.display = window.scrollY > 500 ? 'flex' : 'none';
}});
</script>
</body>
</html>"""

# ============================================================
# Markdown 转 HTML
# ============================================================

def md_to_html(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'toc',
    ])
    html_body = md.convert(md_text)

    toc_html = ""
    for header in md.toc_tokens:
        level = header['level']
        text = header['name']
        anchor = header['id']
        indent_class = f"toc-h{level}"
        toc_html += f'<li><a href="#{anchor}" class="{indent_class}">{text}</a></li>\n'

    return html_body, toc_html


# ============================================================
# 生成各科HTML
# ============================================================

subjects = [
    ("数学一知识体系全解", os.path.join(BASE_DIR, "数学一/数学一知识体系全解.md"), "math1.html", "math"),
    ("英语一知识体系全解", os.path.join(BASE_DIR, "英语一/英语一知识体系全解.md"), "english1.html", "english"),
    ("408知识体系全解", os.path.join(BASE_DIR, "408专业课/408知识体系全解.md"), "cs408.html", "cs408"),
]

for title, md_path, out_name, nav_key in subjects:
    print(f"正在转换: {title} ...")
    body, toc = md_to_html(md_path)
    html = make_html(title, body, toc, active_nav=nav_key)
    out_path = os.path.join(WEBSITE_DIR, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ 完成: {out_path}")

# ============================================================
# 生成主页 (Notion风格)
# ============================================================

home_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>考研冲刺君 | 考研知识体系全解</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">
    <span class="logo">🏆</span>
    <span>考研冲刺君</span>
  </a>
  <ul class="nav-links">
    <li><a href="index.html" class="active">首页</a></li>
    <li><a href="math1.html">数学一</a></li>
    <li><a href="english1.html">英语一</a></li>
    <li><a href="cs408.html">408专业课</a></li>
  </ul>
</nav>

<div class="main-layout">
  <aside class="sidebar">
    <div class="sidebar-title">导航</div>
    <ul class="toc-list">
      <li><a href="#overview" class="toc-h2">项目概览</a></li>
      <li><a href="#subjects" class="toc-h2">三科知识体系</a></li>
      <li><a href="#schedule" class="toc-h2">备考三阶段规划</a></li>
      <li><a href="#daily" class="toc-h2">每日时间安排</a></li>
      <li><a href="#materials" class="toc-h2">核心资料推荐</a></li>
    </ul>
  </aside>

  <main class="content">

<div class="hero" id="overview">
  <h1>考研冲刺君</h1>
  <p class="hero-subtitle">数学一 · 英语一 · 408计算机学科专业基础</p>
  <p class="hero-subtitle">知识体系全解 · 真题驱动 · 冲刺名校</p>
  <div class="hero-stats">
    <div class="stat-item">
      <div class="stat-number">8,938</div>
      <div class="stat-label">行知识体系</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">33</div>
      <div class="stat-label">套历年真题</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">400+</div>
      <div class="stat-label">冲刺目标分</div>
    </div>
  </div>
</div>

<div class="section-divider"></div>

<h2 id="subjects">三科知识体系</h2>

<div class="card-grid">
  <a href="math1.html" class="card">
    <div class="card-icon">📐</div>
    <div class="card-title">数学一</div>
    <div class="card-desc">高等数学、线性代数、概率论与数理统计。极限七大方法、中值定理、格林高斯斯托克斯、矩阵对角化、参数估计...</div>
    <div class="card-meta">
      <span>150分</span>
      <span>2,604行</span>
      <span>22章</span>
    </div>
  </a>

  <a href="english1.html" class="card">
    <div class="card-icon">📝</div>
    <div class="card-title">英语一</div>
    <div class="card-desc">阅读六大题型方法论、新题型技巧、完形填空五步法、翻译拆分法、大小作文模板、2000核心词汇...</div>
    <div class="card-meta">
      <span>100分</span>
      <span>1,875行</span>
      <span>7大板块</span>
    </div>
  </a>

  <a href="cs408.html" class="card">
    <div class="card-icon">💻</div>
    <div class="card-title">408专业课</div>
    <div class="card-desc">数据结构、计算机组成原理、操作系统、计算机网络。算法代码模板、Cache综合题、PV操作、TCP拥塞控制...</div>
    <div class="card-meta">
      <span>150分</span>
      <span>4,189行</span>
      <span>4门课程</span>
    </div>
  </a>
</div>

<div class="section-divider"></div>

<h2 id="schedule">备考三阶段规划</h2>

<h3>第一阶段：基础夯实期（3-6月）</h3>
<table>
  <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
  <tr><td>3-4月</td><td>高数一轮</td><td>背单词+长难句</td><td>数据结构一轮</td></tr>
  <tr><td>4-5月</td><td>线代+高数复习</td><td>早年阅读精读</td><td>计算机组成原理</td></tr>
  <tr><td>5-6月</td><td>概率论一轮</td><td>阅读精读</td><td>操作系统+计网</td></tr>
</table>

<h3>第二阶段：强化突破期（7-9月）</h3>
<table>
  <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
  <tr><td>7月</td><td>高数强化+大量刷题</td><td>阅读专项突破</td><td>数据结构+计组强化</td></tr>
  <tr><td>8月</td><td>线代+概率强化</td><td>完型+新题型+翻译</td><td>OS+计网强化</td></tr>
  <tr><td>9月</td><td>真题套卷(05-15)</td><td>作文模板+真题二刷</td><td>408真题(09-15)</td></tr>
</table>

<h3>第三阶段：冲刺模考期（10-12月）</h3>
<table>
  <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
  <tr><td>10月</td><td>真题二刷(16-24)</td><td>全真模拟</td><td>真题二刷+模拟</td></tr>
  <tr><td>11月</td><td>模拟卷(李林6+4)</td><td>作文默写</td><td>模拟题+查漏补缺</td></tr>
  <tr><td>12月</td><td>错题回顾+公式默写</td><td>考前保温</td><td>重点背诵+错题</td></tr>
</table>

<div class="section-divider"></div>

<h2 id="daily">每日时间安排</h2>

<table>
  <tr><th>时间段</th><th>内容</th></tr>
  <tr><td>8:00-10:00</td><td><strong>数学</strong>（黄金时间，头脑最清醒）</td></tr>
  <tr><td>10:20-12:00</td><td><strong>408专业课</strong></td></tr>
  <tr><td>14:00-15:30</td><td><strong>英语</strong>（适应考试时间）</td></tr>
  <tr><td>15:50-17:30</td><td>数学/408 做题</td></tr>
  <tr><td>19:00-21:00</td><td><strong>政治</strong></td></tr>
  <tr><td>21:00-22:00</td><td>复盘 / 背单词 / 整理错题</td></tr>
</table>

<div class="section-divider"></div>

<h2 id="materials">核心资料推荐</h2>

<h3>数学一</h3>
<ul>
  <li><strong>教材</strong>：同济高数、同济线代、浙大概率论</li>
  <li><strong>辅导书</strong>：张宇/武忠祥/汤家凤 强化讲义（选一个跟到底）</li>
  <li><strong>习题</strong>：660题 + 880题 + 真题</li>
  <li><strong>模拟卷</strong>：李林6+4套卷（必做！）、张宇8+4</li>
</ul>

<h3>英语一</h3>
<ul>
  <li><strong>单词</strong>：红宝书 / 墨墨背单词APP</li>
  <li><strong>真题</strong>：黄皮书 / 考研真相</li>
  <li><strong>作文</strong>：王江涛高分写作 / 潘赟九宫格</li>
  <li><strong>长难句</strong>：田静句句真研</li>
</ul>

<h3>408专业课</h3>
<ul>
  <li><strong>教材</strong>：王道四本单科书（必买！）</li>
  <li><strong>习题</strong>：王道课后选择题 + 大题</li>
  <li><strong>真题</strong>：王道历年真题解析</li>
  <li><strong>模拟题</strong>：王道模拟卷</li>
</ul>

<h3>政治</h3>
<ul>
  <li><strong>强化</strong>：徐涛/腿姐 强化课</li>
  <li><strong>习题</strong>：肖秀荣1000题</li>
  <li><strong>冲刺</strong>：肖八（选择题）+ 肖四（全背！）</li>
  <li><strong>时政</strong>：肖秀荣形势与政策</li>
</ul>

<div class="section-divider"></div>

<blockquote>
<p><strong>使用指南</strong></p>
<p>知识体系文档是你的"备考圣经"——第一轮通读建框架，第二轮配合做题查缺补漏，第三轮只看重点和易错点。</p>
<p>真题至少做3遍：第一遍按科目了解题型，第二遍按年份模拟考试，第三遍只看错题。</p>
</blockquote>

<footer>
  <p>🏆 考研冲刺君 · 一战必成硕</p>
  <p style="margin-top: 6px;">目标：清华大学计算机科学与技术</p>
</footer>

  </main>
</div>

</body>
</html>"""

home_path = os.path.join(WEBSITE_DIR, "index.html")
with open(home_path, "w", encoding="utf-8") as f:
    f.write(home_html)

print(f"\n✅ Notion风格网站生成完成!")
print(f"主页: {home_path}")

for name in ['index.html', 'math1.html', 'english1.html', 'cs408.html', 'assets/style.css']:
    path = os.path.join(WEBSITE_DIR, name)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  {name}: {size/1024:.1f} KB")
