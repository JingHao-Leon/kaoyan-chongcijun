from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "website" / "math_chapter_lookup.html"
PDF = ROOT.parent / "11408_zhenti" / "shuxue1"
TEXT = ROOT / "tmp" / "pdfs" / "math1"
IMAGES = ROOT / "website" / "images" / "math_papers"

CHAPTERS = [
    ("函数、极限、连续", "极限、等价无穷小、连续、间断、渐近线和泰勒展开"),
    ("一元函数微分学", "导数、单调性、极值、凹凸性、中值定理"),
    ("一元函数积分学", "不定积分、定积分、反常积分及积分应用"),
    ("向量代数与空间解析几何", "空间直线、平面、距离、夹角和位置关系"),
    ("多元函数微分学", "偏导、全微分、方向导数、条件极值"),
    ("多元函数积分学", "二三重积分、曲线积分、曲面积分及三大公式"),
    ("无穷级数", "数项级数、幂级数、傅里叶级数"),
    ("常微分方程", "一阶、高阶线性和欧拉型微分方程"),
    ("行列式", "行列式的性质、计算和展开"),
    ("矩阵", "矩阵运算、秩、逆矩阵、矩阵方程"),
    ("向量", "线性相关、极大无关组、正交化"),
    ("线性方程组", "齐次与非齐次方程组、解空间"),
    ("特征值与特征向量", "特征值、特征向量与相似对角化"),
    ("二次型", "标准形、合同变换与正定性"),
    ("随机事件与概率", "条件概率、全概率、贝叶斯和独立性"),
    ("一维随机变量及其分布", "分布函数、密度和常见一维分布"),
    ("多维随机变量及其分布", "联合、边缘、条件分布和独立性"),
    ("数字特征", "期望、方差、协方差和相关系数"),
    ("大数定律与中心极限定理", "切比雪夫不等式、依概率收敛和近似正态"),
    ("数理统计基本概念", "总体、样本、统计量和抽样分布"),
    ("参数估计", "矩估计、最大似然、无偏性和置信区间"),
    ("假设检验", "原假设、拒绝域、两类错误和 p 值"),
]

# 只在题面有明确术语时归类；一题可命中多个真实考点，不按题号补位。
RULES = [
    (22, r"假设检验|拒绝域|原假设|备择假设"),
    (21, r"置信区间|最大似然|无偏估计|矩估计|估计量"),
    (19, r"大数定律|中心极限|切比雪夫|依概率"),
    (18, r"协方差|相关系数|Cov|数学期望|方差|EX|DX"),
    (17, r"二维随机变量|多维随机变量|联合分布|边缘分布|条件分布|条件下随机变量"),
    (15, r"随机事件|条件概率|贝叶斯|互不相容|独立"),
    (16, r"概率密度|分布函数|正态分布|泊松分布|指数分布|均匀分布"),
    (14, r"二次型|正定|惯性指数|标准形|合同变换"),
    (13, r"特征值|特征向量|相似对角化"),
    (12, r"线性方程组|方程组"),
    (11, r"向量组|线性无关|线性相关|正交化"),
    (9, r"行列式"),
    (10, r"矩阵|逆矩阵|矩阵方程|\br\s*\("),
    (8, r"微分方程|欧拉方程"),
    (7, r"幂级数|傅里叶|级数"),
    (6, r"二重积分|三重积分|曲线积分|曲面积分|格林|斯托克斯|高斯公式"),
    (5, r"偏导|全微分|方向导数|z\s*=|f\s*\(\s*x\s*,\s*y"),
    (4, r"空间直角|直线|平面|球面|柱面"),
    (3, r"反常积分|不定积分|定积分|积分"),
    (2, r"导数|拐点|极值|单调|凹|切线|可导"),
    (1, r"极限|无穷小|连续|间断|渐近线|泰勒|等价"),
]

def extract(year):
    path = TEXT / f"shuxue1_{year}.txt"
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"(?:【(\d+)】|\n\s*\(?([1-9]|1[0-9]|2[0-2])[】)、.．])", raw))
    questions = {}
    for i, match in enumerate(matches):
        number = int(match.group(1) or match.group(2))
        if number > 22 or number in questions:
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        body = raw[match.end():end].split("【答案】", 1)[0].strip()
        if body:
            questions[number] = (body, raw[:match.start()].count("\f") + 1)
    return questions

def image_name(year, page):
    folder = IMAGES / str(year)
    for name in (f"page-{page}.png", f"page-{page:02d}.png"):
        if (folder / name).exists():
            return name
    return None

def topics_for(body):
    compact = re.sub(r"\s+", " ", body)
    return [chapter for chapter, pattern in RULES if re.search(pattern, compact, re.I)]

by_chapter = {i: [] for i in range(1, 23)}
for year in range(2014, 2025):
    for number, (body, page) in extract(year).items():
        for chapter in topics_for(body):
            by_chapter[chapter].append((year, number, page, body))

sections = []
for index, (name, guide) in enumerate(CHAPTERS, 1):
    entries = by_chapter[index]
    rows = []
    for year, number, page, body in entries:
        image = image_name(year, page)
        pdf = f"../../11408_zhenti/shuxue1/shuxue1_{year}.pdf#page={page}"
        original = (f'<img class="paper-image" src="images/math_papers/{year}/{image}" alt="{year} 年数学一第 {number} 题所在原卷页" loading="lazy">'
                    if image else f'<pre>{escape(body[:520])}</pre>')
        rows.append(f'''<details><summary>{year} 年 · 第 {number} 题（PDF 第 {page} 页）</summary>
          <p class="tag">原题依据：{escape(guide)}</p>{original}
          <p class="source"><a href="{pdf}" target="_blank">打开该题所在原卷页 ↗</a></p>
          <p><b>解题切入：</b>{escape(guide)}。先识别题目条件对应的定义或公式，再根据题型进行运算或论证。</p></details>''')
    empty = '<p class="empty">已核验的可提取题面中，暂未找到这一模块的独立题目；这表示该年未以独立题型出现，不用题号硬凑。</p>'
    sections.append(f'<section id="chapter-{index}" class="chapter"><h2>{index}. {escape(name)}</h2><p class="guide">{escape(guide)}</p>{"".join(rows) if rows else empty}</section>')

html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>数学一分章真题速查 | 考研冲刺君</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f7fb;color:#202331;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}.top{background:#151824;color:#fff;padding:16px 5vw;display:flex;justify-content:space-between;align-items:center}.top a{color:#cbd3ff;text-decoration:none}main{max-width:1120px;margin:0 auto;padding:28px 5vw 80px}h1{font-size:32px;margin:10px 0}h2{margin:28px 0 8px}.note{background:#fff8e7;border:1px solid #f0d28c;padding:14px 16px;border-radius:12px;margin:18px 0}.chapter{background:#fff;border:1px solid #e2e5ee;border-radius:14px;margin:18px 0;padding:18px}.guide{color:#687083;margin-top:0}.chapter details{border-top:1px solid #edf0f5;padding:10px 0}.chapter summary{cursor:pointer;font-weight:700}.chapter details p{margin:7px 0}.source a,.toc a{color:#3857d7}.paper-image{display:block;width:100%;max-width:820px;margin:10px 0;border:1px solid #e2e5ee;border-radius:8px;background:#fff}pre{white-space:pre-wrap;max-height:360px;overflow:auto;background:#fafbfe;border:1px solid #edf0f5;border-radius:8px;padding:12px;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,monospace}.toc{display:flex;flex-wrap:wrap;gap:8px}.toc a{background:#f1f4ff;border-radius:8px;padding:4px 9px;text-decoration:none}.tag{font-size:13px;color:#687083}.empty{color:#7a8090}@media(max-width:600px){h1{font-size:26px}main{padding-left:16px;padding-right:16px}}
</style></head><body><header class="top"><strong>考研冲刺君 · 数学一</strong><nav><a href="index.html">首页</a>　<a href="math1.html">数学一知识体系</a></nav></header><main><p><a href="math1.html">← 返回数学一知识体系</a></p><h1>数学一分章真题速查</h1><p>题目只在其题面明确命中的知识模块内展示。某年没有该模块的独立题时，宁可留空，也不按题号硬塞。</p><div class="note"><b>来源与核验：</b>全部原题来自本地 <code>11408_zhenti/shuxue1</code> 文件夹。每条均保留原卷页链接；公式优先展示原始 PDF 页图。</div><div class="toc">''' + ''.join(f'<a href="#chapter-{i}">{i}. {escape(name)}</a>' for i, (name, _) in enumerate(CHAPTERS, 1)) + '''</div>''' + ''.join(sections) + '''</main></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT}; verified references: {sum(len(x) for x in by_chapter.values())}")
