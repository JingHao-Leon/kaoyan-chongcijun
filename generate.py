#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
考研冲刺君 - 网站生成脚本
将Markdown知识体系文档转换为精美的HTML网站
"""

import os
import re
import markdown

BASE_DIR = "/Users/ahs/Documents/kimi/workspace/考研冲刺君"
WEBSITE_DIR = os.path.join(BASE_DIR, "website")
ASSETS_DIR = os.path.join(WEBSITE_DIR, "assets")

os.makedirs(WEBSITE_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ============================================================
# CSS 主题
# ============================================================
CSS = r"""
:root {
  --bg-primary: #0f1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #1c2128;
  --bg-code: #0d1117;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --accent: #58a6ff;
  --accent-hover: #79b8ff;
  --accent-glow: rgba(88, 166, 255, 0.15);
  --border: #30363d;
  --border-light: #21262d;
  --success: #3fb950;
  --warning: #d29922;
  --danger: #f85149;
  --info: #58a6ff;
  --math-bg: rgba(88, 166, 255, 0.05);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  font-size: 15px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.8;
  overflow-x: hidden;
}

/* 顶部导航 */
.top-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 56px;
  background: rgba(15, 17, 23, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
}

.nav-brand .logo { font-size: 1.4rem; }

.nav-links {
  display: flex;
  gap: 4px;
  list-style: none;
}

.nav-links a {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.nav-links a:hover, .nav-links a.active {
  color: var(--accent);
  background: var(--accent-glow);
}

/* 主布局 */
.main-layout {
  display: flex;
  margin-top: 56px;
  min-height: calc(100vh - 56px);
}

/* 侧边栏 */
.sidebar {
  width: 280px;
  height: calc(100vh - 56px);
  position: fixed;
  left: 0; top: 56px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 16px 0;
  z-index: 100;
}

.sidebar::-webkit-scrollbar { width: 6px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

.sidebar-title {
  padding: 0 20px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.toc-list { list-style: none; padding: 0; }
.toc-list li { margin: 0; }

.toc-list a {
  display: block;
  padding: 6px 20px 6px 24px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85rem;
  border-left: 2px solid transparent;
  transition: all 0.15s;
  line-height: 1.5;
}

.toc-list a:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.toc-list a.active {
  color: var(--accent);
  border-left-color: var(--accent);
  background: var(--accent-glow);
}

.toc-list .toc-h2 { padding-left: 24px; font-weight: 500; }
.toc-list .toc-h3 { padding-left: 40px; font-size: 0.8rem; }
.toc-list .toc-h4 { padding-left: 56px; font-size: 0.78rem; color: var(--text-muted); }

/* 内容区 */
.content {
  margin-left: 280px;
  flex: 1;
  max-width: 900px;
  padding: 40px 48px 80px;
}

/* 标题 */
h1 { font-size: 2.4rem; font-weight: 800; margin: 0 0 24px; color: var(--text-primary); border-bottom: 2px solid var(--accent); padding-bottom: 12px; }
h2 { font-size: 1.7rem; font-weight: 700; margin: 48px 0 20px; color: var(--text-primary); padding-bottom: 8px; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.3rem; font-weight: 600; margin: 32px 0 16px; color: var(--accent); }
h4 { font-size: 1.1rem; font-weight: 600; margin: 24px 0 12px; color: var(--text-secondary); }
h5 { font-size: 1rem; font-weight: 600; margin: 16px 0 8px; color: var(--text-muted); }

h1 a.anchor, h2 a.anchor, h3 a.anchor, h4 a.anchor {
  color: var(--text-muted);
  text-decoration: none;
  margin-left: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}
h1:hover a.anchor, h2:hover a.anchor, h3:hover a.anchor, h4:hover a.anchor { opacity: 1; }

/* 段落和文本 */
p { margin: 12px 0; }

strong { color: var(--accent-hover); font-weight: 600; }

em { color: var(--warning); font-style: italic; }

/* 引用块 */
blockquote {
  margin: 16px 0;
  padding: 12px 20px;
  background: var(--bg-secondary);
  border-left: 4px solid var(--accent);
  border-radius: 0 8px 8px 0;
  color: var(--text-secondary);
}

blockquote p { margin: 6px 0; }
blockquote p:first-child { margin-top: 0; }
blockquote p:last-child { margin-bottom: 0; }

/* 特殊引用块 */
blockquote.alert-warning { border-left-color: var(--warning); background: rgba(210, 153, 34, 0.08); }
blockquote.alert-danger { border-left-color: var(--danger); background: rgba(248, 81, 73, 0.08); }
blockquote.alert-success { border-left-color: var(--success); background: rgba(63, 185, 80, 0.08); }
blockquote.alert-info { border-left-color: var(--info); background: var(--accent-glow); }

/* 代码块 */
pre {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  overflow-x: auto;
  margin: 16px 0;
  font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
}

code {
  font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
  background: var(--bg-code);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.88em;
  color: var(--accent-hover);
  border: 1px solid var(--border-light);
}

pre code {
  background: transparent;
  padding: 0;
  border: none;
  color: var(--text-primary);
}

/* 代码高亮 */
.code-keyword { color: #ff7b72; }
.code-string { color: #a5d6ff; }
.code-comment { color: #8b949e; font-style: italic; }
.code-number { color: #79c0ff; }
.code-function { color: #d2a8ff; }
.code-type { color: #ffa657; }

/* 表格 */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 0.9rem;
  border-radius: 8px;
  overflow: hidden;
}

th {
  background: var(--bg-tertiary);
  color: var(--accent);
  font-weight: 600;
  text-align: left;
  padding: 10px 14px;
  border-bottom: 2px solid var(--accent);
}

td {
  padding: 8px 14px;
  border-bottom: 1px solid var(--border-light);
}

tr:hover td { background: var(--bg-tertiary); }

/* 列表 */
ul, ol { margin: 12px 0 12px 24px; }
li { margin: 6px 0; }

/* 水平线 */
hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 32px 0;
}

/* 数学公式 */
.katex-display {
  background: var(--math-bg);
  border-radius: 8px;
  padding: 12px 16px;
  margin: 16px 0;
  overflow-x: auto;
}
.katex { font-size: 1.05em; }

/* 链接 */
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* 标签/徽章 */
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  margin-right: 6px;
}
.badge-frequency { background: rgba(210, 153, 34, 0.2); color: var(--warning); }
.badge-difficulty { background: rgba(248, 81, 73, 0.2); color: var(--danger); }
.badge-score { background: rgba(88, 166, 255, 0.2); color: var(--accent); }

/* 主页样式 */
.hero {
  text-align: center;
  padding: 80px 40px 60px;
  background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-bottom: 1px solid var(--border);
}

.hero h1 {
  font-size: 3rem;
  font-weight: 800;
  border: none;
  margin-bottom: 16px;
  background: linear-gradient(135deg, var(--accent) 0%, #a371f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary);
  margin-bottom: 32px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-top: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--accent);
}

.stat-label {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* 卡片 */
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 48px;
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px 28px;
  text-decoration: none;
  color: var(--text-primary);
  transition: all 0.3s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: 0 8px 32px rgba(88, 166, 255, 0.12);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.card-meta {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* 搜索 */
.search-box {
  position: relative;
  width: 240px;
}

.search-box input {
  width: 100%;
  padding: 8px 14px 8px 36px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.9rem;
  outline: none;
}

.search-box input:focus { border-color: var(--accent); }

.search-box::before {
  content: "🔍";
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.9rem;
  opacity: 0.6;
}

/* 回到顶部 */
.back-to-top {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 50%;
  color: var(--accent);
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 500;
  transition: all 0.2s;
}

.back-to-top:hover {
  background: var(--accent);
  color: white;
}

/* 响应式 */
@media (max-width: 1024px) {
  .sidebar { display: none; }
  .content { margin-left: 0; padding: 24px; }
  .card-grid { grid-template-columns: 1fr; padding: 24px; }
  .hero h1 { font-size: 2rem; }
}

@media (max-width: 768px) {
  .top-nav { padding: 0 12px; }
  .nav-links { display: none; }
  .hero-stats { flex-direction: column; gap: 24px; }
  .content { padding: 16px; }
  h1 { font-size: 1.8rem; }
  h2 { font-size: 1.4rem; }
}

/* 打印 */
@media print {
  .top-nav, .sidebar, .back-to-top { display: none !important; }
  .content { margin-left: 0; max-width: none; }
  body { background: white; color: black; }
}
"""

# 写入CSS文件
css_path = os.path.join(ASSETS_DIR, "style.css")
with open(css_path, "w", encoding="utf-8") as f:
    f.write(CSS)

print(f"CSS 写入: {css_path}")

# ============================================================
# HTML 模板
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
    <div class="sidebar-title">📑 目录导航</div>
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
    if (h.getBoundingClientRect().top <= 100) current = h.id;
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
    """读取Markdown文件并转换为HTML"""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 使用markdown库转换
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'toc',
    ])
    html_body = md.convert(md_text)

    # 生成目录
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
# 生成主页
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

<div class="hero">
  <h1>考研冲刺君</h1>
  <p class="hero-subtitle">数学一 + 英语一 + 408 计算机学科专业基础</p>
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

<div class="card-grid">
  <a href="math1.html" class="card">
    <div class="card-icon">📐</div>
    <div class="card-title">数学一</div>
    <div class="card-desc">高等数学 + 线性代数 + 概率论与数理统计。极限7大方法、中值定理、三大公式、矩阵对角化、参数估计...</div>
    <div class="card-meta">
      <span>⭐ 150分</span>
      <span>2,604行</span>
      <span>22章</span>
    </div>
  </a>

  <a href="english1.html" class="card">
    <div class="card-icon">📝</div>
    <div class="card-title">英语一</div>
    <div class="card-desc">阅读六大题型方法论、新题型技巧、完形填空五步法、翻译拆分法、大小作文模板、2000核心词汇...</div>
    <div class="card-meta">
      <span>⭐ 100分</span>
      <span>1,875行</span>
      <span>7大板块</span>
    </div>
  </a>

  <a href="cs408.html" class="card">
    <div class="card-icon">💻</div>
    <div class="card-title">408专业课</div>
    <div class="card-desc">数据结构 + 计算机组成原理 + 操作系统 + 计算机网络。算法代码模板、Cache综合题、PV操作、TCP拥塞控制...</div>
    <div class="card-meta">
      <span>⭐ 150分</span>
      <span>4,189行</span>
      <span>4门课程</span>
    </div>
  </a>
</div>

<div style="max-width: 900px; margin: 0 auto; padding: 0 48px 80px;">
  <h2 style="text-align: center; margin-top: 0;">📅 备考三阶段规划</h2>

  <h3>🔹 第一阶段：基础夯实期（3-6月）</h3>
  <table>
    <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
    <tr><td>3-4月</td><td>高数一轮</td><td>背单词+长难句</td><td>数据结构一轮</td></tr>
    <tr><td>4-5月</td><td>线代+高数复习</td><td>早年阅读精读</td><td>计算机组成原理</td></tr>
    <tr><td>5-6月</td><td>概率论一轮</td><td>阅读精读</td><td>操作系统+计网</td></tr>
  </table>

  <h3>🔹 第二阶段：强化突破期（7-9月）</h3>
  <table>
    <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
    <tr><td>7月</td><td>高数强化+大量刷题</td><td>阅读专项突破</td><td>数据结构+计组强化</td></tr>
    <tr><td>8月</td><td>线代+概率强化</td><td>完型+新题型+翻译</td><td>OS+计网强化</td></tr>
    <tr><td>9月</td><td>真题套卷(05-15)</td><td>作文模板+真题二刷</td><td>408真题(09-15)</td></tr>
  </table>

  <h3>🔹 第三阶段：冲刺模考期（10-12月）</h3>
  <table>
    <tr><th>时间</th><th>数学一</th><th>英语一</th><th>408</th></tr>
    <tr><td>10月</td><td>真题二刷(16-24)</td><td>全真模拟</td><td>真题二刷+模拟</td></tr>
    <tr><td>11月</td><td>模拟卷(李林6+4)</td><td>作文默写</td><td>模拟题+查漏补缺</td></tr>
    <tr><td>12月</td><td>错题回顾+公式默写</td><td>考前保温</td><td>重点背诵+错题</td></tr>
  </table>

  <h3>⏰ 每日时间安排</h3>
  <table>
    <tr><th>时间段</th><th>内容</th></tr>
    <tr><td>8:00-10:00</td><td><strong>数学</strong>（黄金时间）</td></tr>
    <tr><td>10:20-12:00</td><td><strong>408专业课</strong></td></tr>
    <tr><td>14:00-15:30</td><td><strong>英语</strong>（适应考试时间）</td></tr>
    <tr><td>15:50-17:30</td><td>数学/408做题</td></tr>
    <tr><td>19:00-21:00</td><td><strong>政治</strong></td></tr>
    <tr><td>21:00-22:00</td><td>复盘/背单词/错题</td></tr>
  </table>
</div>

<footer style="text-align: center; padding: 40px; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem;">
  <p>🏆 考研冲刺君 · 一战必成硕</p>
  <p style="margin-top: 8px;">目标：清华大学计算机科学与技术</p>
</footer>

</body>
</html>"""

home_path = os.path.join(WEBSITE_DIR, "index.html")
with open(home_path, "w", encoding="utf-8") as f:
    f.write(home_html)

print(f"\n✅ 网站生成完成!")
print(f"主页: {home_path}")
print(f"数学一: {os.path.join(WEBSITE_DIR, 'math1.html')}")
print(f"英语一: {os.path.join(WEBSITE_DIR, 'english1.html')}")
print(f"408: {os.path.join(WEBSITE_DIR, 'cs408.html')}")
print(f"CSS: {css_path}")

# 列出文件大小
for name in ['index.html', 'math1.html', 'english1.html', 'cs408.html', 'assets/style.css']:
    path = os.path.join(WEBSITE_DIR, name)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  {name}: {size/1024:.1f} KB")
