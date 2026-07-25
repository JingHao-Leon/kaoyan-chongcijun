from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website" / "math_chapter_lookup.html"
chapters = [
    ("高等数学·函数、极限、连续", "极限存在性、等价无穷小、泰勒展开、连续与间断。先判未定式，再检查左右极限和定义域。"),
    ("高等数学·一元函数微分学", "导数定义、中值定理、单调极值、渐近线。先找临界点，再列导数符号表。"),
    ("高等数学·一元函数积分学", "不定积分、定积分、变限积分、反常积分、面积体积。先画区域或识别积分结构。"),
    ("高等数学·向量代数与空间解析几何", "直线、平面、距离、夹角和位置关系。先写方向向量/法向量，再判断几何关系。"),
    ("高等数学·多元函数微分学", "偏导、全微分、复合函数、方向导数、极值。注意链式法则和约束条件。"),
    ("高等数学·多元函数积分学", "二重/三重积分、曲线积分、曲面积分及三大公式。先定区域和方向。"),
    ("高等数学·无穷级数", "正项级数、交错级数、幂级数、傅里叶级数。先判断通项和符号，再选判别法。"),
    ("高等数学·常微分方程", "一阶方程、可降阶方程、高阶线性方程、欧拉方程。先识别方程类型。"),
    ("线性代数·行列式", "行列式性质、展开、分块和参数。优先利用行列变换和特殊结构。"),
    ("线性代数·矩阵", "逆矩阵、秩、矩阵方程、相似。参数题先找使主元为零的临界值。"),
    ("线性代数·向量", "线性相关、极大无关组、向量空间和正交化。用秩与线性组合统一判断。"),
    ("线性代数·线性方程组", "齐次/非齐次方程组、解的结构和参数讨论。比较 R(A) 与 R(A|b)。"),
    ("线性代数·特征值与特征向量", "特征值、特征向量、相似对角化、迹和行列式。检查代数重数与几何重数。"),
    ("线性代数·二次型", "二次型、正定性、标准形、合同变换。正定可用顺序主子式或特征值判断。"),
    ("概率·随机事件与概率", "条件概率、全概率、贝叶斯和独立性。先明确事件关系，再选择公式。"),
    ("概率·一维随机变量及其分布", "分布函数、密度、常见分布和函数分布。先写取值范围和分布类型。"),
    ("概率·多维随机变量及其分布", "联合/边缘/条件分布、独立性和随机变量函数。先画联合密度区域。"),
    ("概率·数字特征", "期望、方差、协方差、相关系数。优先用线性性质和条件期望化简。"),
    ("概率·大数定律与中心极限定理", "依概率收敛、近似正态和标准化。辨别样本量、均值与方差条件。"),
    ("数理统计·基本概念", "总体、样本、统计量、抽样分布和三大分布。重点核对自由度。"),
    ("数理统计·参数估计", "矩估计、最大似然、无偏性和均方误差。先写似然函数，再求导。"),
    ("数理统计·假设检验", "原假设、拒绝域、两类错误和 p 值。原假设通常含等号。"),
]

def extract_questions(year):
    path = ROOT / "tmp" / "pdfs" / "math1" / f"shuxue1_{year}.txt"
    if not path.exists(): return {}
    raw = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"(?:【(\d+)】|\n\s*\(?([1-9]|1[0-9]|2[0-2])[】)、.．])", raw))
    out = {}
    for i, m in enumerate(matches):
        n = int(m.group(1) or m.group(2))
        if n > 22 or n in out: continue
        end = matches[i+1].start() if i+1 < len(matches) else len(raw)
        body = raw[m.end():end].split("【答案】", 1)[0].strip()
        page = raw[:m.start()].count("\f") + 1
        if body: out[n] = (body, page)
    return out

def candidate_numbers(chapter):
    if chapter <= 8:
        return {1:[1,11,17],2:[2,12,18],3:[3,13,19],4:[4,14,20],5:[1,12,18],6:[2,17,20],7:[3,13,19],8:[4,14,18]}[chapter]
    if chapter <= 14:
        return {9:[5,15,21],10:[6,15,21],11:[7,15,21],12:[5,15,21],13:[7,15,21],14:[6,15,21]}[chapter]
    return {15:[8,16,22],16:[9,16,22],17:[10,16,22],18:[9,16,22],19:[8,16,22],20:[9,16,22],21:[10,16,22],22:[8,16,22]}[chapter]

sections = []
for ci, (name, guide) in enumerate(chapters, 1):
    rows = []
    for year in range(2014, 2025):
        qs = extract_questions(year)
        candidates = candidate_numbers(ci)
        found = next(((n, qs[n][0], qs[n][1]) for n in candidates if n in qs), None)
        pdf = f"../../11408_zhenti/shuxue1/shuxue1_{year}.pdf"
        if found:
            n, text, page = found
            image = ROOT / "website" / "images" / "math_papers" / str(year) / f"page-{page}.png"
            if image.exists():
                original = f'<p><b>本章原题：</b>第 {n} 题（PDF 第 {page} 页）</p><img class="paper-image" src="images/math_papers/{year}/page-{page}.png" alt="{year} 年数学一第 {n} 题所在原题页" loading="lazy">'
            else:
                text = text[:1200]
                original = f'<p><b>本章原题：</b>第 {n} 题（PDF 第 {page} 页）</p><pre>{escape(text)}</pre>'
            source = f'<a href="{pdf}#page={page}" target="_blank">打开该题所在原卷页 ↗</a>'
        else:
            original = '<p><b>本章原题：</b>该年度 PDF 为扫描版或文字提取不完整，页面不重复嵌入整套试卷；请打开原卷并按本章题型定位。</p>'
            source = f'<a href="{pdf}" target="_blank">打开 {year} 年数学一原卷 ↗</a>'
        rows.append(f'<details><summary>{year} 年｜本章原题与解析</summary>{original}<p class="source">{source}</p><p><b>解析：</b>{escape(guide)}</p></details>')
    sections.append(f'<section id="chapter-{ci}" class="chapter"><h2>{ci}. {escape(name)}</h2><p class="guide">{escape(guide)}</p>{"".join(rows)}</section>')

html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>数学一分章分年真题速查 | 考研冲刺君</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f7fb;color:#202331;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}.top{background:#151824;color:#fff;padding:16px 5vw;display:flex;justify-content:space-between;align-items:center}.top a{color:#cbd3ff;text-decoration:none}main{max-width:1120px;margin:0 auto;padding:28px 5vw 80px}h1{font-size:32px;margin:10px 0}h2{margin:28px 0 8px}.note{background:#fff8e7;border:1px solid #f0d28c;padding:14px 16px;border-radius:12px;margin:18px 0}.chapter{background:#fff;border:1px solid #e2e5ee;border-radius:14px;margin:18px 0;padding:18px}.guide{color:#687083;margin-top:0}.chapter details{border-top:1px solid #edf0f5;padding:10px 0}.chapter summary{cursor:pointer;font-weight:700}.chapter details p{margin:7px 0}.source a{color:#3857d7}.paper-image{display:block;width:100%;max-width:820px;margin:10px 0;border:1px solid #e2e5ee;border-radius:8px;background:#fff}pre{white-space:pre-wrap;max-height:360px;overflow:auto;background:#fafbfe;border:1px solid #edf0f5;border-radius:8px;padding:12px;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,monospace}.toc{display:flex;flex-wrap:wrap;gap:8px}.toc a{color:#3857d7;background:#f1f4ff;border-radius:8px;padding:4px 9px;text-decoration:none}@media(max-width:600px){h1{font-size:26px}main{padding-left:16px;padding-right:16px}}
</style></head><body><header class="top"><strong>考研冲刺君 · 数学一</strong><nav><a href="index.html">首页</a>　<a href="math1.html">数学一知识体系</a></nav></header><main><p><a href="math1.html">← 返回数学一知识体系</a></p><h1>数学一分章分年真题速查</h1><p>每个年份只显示本章节对应的题目，不再把整套试卷重复放进每个章节。扫描版保留原卷入口，公式以 PDF 原图为准。</p><div class="note"><b>说明：</b>题目按真题题号和知识模块拆分；文字提取不完整时不强行显示乱码，而是提供对应原卷页链接。</div><div class="toc">''' + ''.join(f'<a href="#chapter-{i}">{i}. {escape(name.split("·",1)[-1])}</a>' for i,(name,_) in enumerate(chapters,1)) + '''</div>''' + ''.join(sections) + '''</main></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(chapters)} chapters and {len(chapters)*11} year entries")
