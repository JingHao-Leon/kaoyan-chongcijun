from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'website' / '408_chapter_lookup.html'
TEXT = ROOT / 'website' / 'tmp' / 'pdfs' / '408'
IMAGES = ROOT / 'website' / 'images' / 'zhenti_pages'

COURSES = [
    ('ds', '数据结构', ['绪论', '线性表', '栈、队列和数组', '树与二叉树', '图', '查找', '排序']),
    ('co', '计算机组成原理', ['计算机系统概述', '数据的表示和运算', '存储系统', '指令系统', '中央处理器', '总线', '输入输出系统']),
    ('os', '操作系统', ['操作系统概述', '进程管理', '内存管理', '文件管理', '输入输出系统']),
    ('cn', '计算机网络', ['计算机网络体系结构', '物理层', '数据链路层', '网络层', '传输层', '应用层']),
]

def course_for(n):
    if n <= 11: return 'ds'
    if n <= 22: return 'co'
    if n <= 32: return 'os'
    return 'cn'

def chapter_for(n, text):
    t = re.sub(r'\s+', '', text).lower()
    if n <= 11:
        # 先匹配具体结构；“插入”等动作词在链表、树和排序中都会出现，不能抢占分类。
        rules = [(2, r'线性表|链表|顺序表'), (3, r'栈|队列|数组|表达式'), (4, r'二叉|树|哈夫曼|avl|b树'), (5, r'有向图|无向图|深度优先|广度优先|最小.*生成|拓扑|最短路径'), (6, r'查找|折半|kmp|散列|哈希'), (7, r'排序|堆|归并|快速|基数|希尔|插入')]
        return next((i for i, p in rules if re.search(p, t, re.I)), 1)
    if n <= 22:
        rules = [(7, r'中断|dma|i/o|设备|磁盘|接口'), (6, r'总线'), (5, r'流水线|cpu|控制器|冒险'), (4, r'寻址|指令格式|指令系统'), (3, r'cache|tlb|主存|存储|dram|sram|虚拟|页式'), (2, r'补码|浮点|整数|运算|加法|乘法|除法|数据表示')]
        return next((i for i, p in rules if re.search(p, t, re.I)), 1)
    if n <= 32:
        rules = [(5, r'设备|i/o|缓冲'), (4, r'文件|磁盘|目录|inode|空闲|块'), (3, r'内存|页|段|伙伴|置换|地址'), (2, r'进程|线程|调度|死锁|同步|互斥|时间片'), (1, r'中断|异常|系统调用|用户态|内核态')]
        return next((i for i, p in rules if re.search(p, t, re.I)), 1)
    rules = [(6, r'http|dns|smtp|ftp'), (5, r'tcp|udp|滑动窗口|选择重传|校验'), (4, r'ip|路由|分组|子网|icmp'), (3, r'vlan|arp|csma|以太网|mac|帧'), (2, r'调制|信号|带宽|物理层')]
    return next((i for i, p in rules if re.search(p, t, re.I)), 1)

def extract(year):
    path = TEXT / f'408_{year}.txt'
    if not path.exists(): return {}
    raw = path.read_text(encoding='utf-8', errors='ignore')
    matches = list(re.finditer(r'(?m)^\s*([1-4]?\d)\s*[\.．、]', raw))
    out = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
        if not 1 <= n <= 40 or n in out: continue
        end = matches[i+1].start() if i + 1 < len(matches) else len(raw)
        body = raw[m.end():end].strip()
        if len(body) > 15:
            out[n] = (body, raw[:m.start()].count('\f') + 1)
    return out

def image(year, page):
    candidate = IMAGES / f'408_{year}_p{page}.png'
    return candidate.name if candidate.exists() else None

records = {(course, index): [] for course, _, chapters in COURSES for index in range(1, len(chapters)+1)}
missing_years = []
for year in range(2014, 2025):
    questions = extract(year)
    if len(questions) < 25:
        missing_years.append(year)
    for n, (body, page) in questions.items():
        course = course_for(n)
        chapter = chapter_for(n, body)
        records[(course, chapter)].append((year, n, page, body))

sections = []
for course, cname, chapters in COURSES:
    sections.append(f'<h1>{cname}</h1>')
    for index, chapter in enumerate(chapters, 1):
        rows = []
        for year, n, page, body in records[(course, index)]:
            img = image(year, page)
            source = f'../../11408_zhenti/408_{year}.pdf#page={page}'
            original = (f'<img src="images/zhenti_pages/{img}" loading="lazy" alt="{year} 年 408 第 {n} 题所在原卷页">'
                        if img else f'<pre>{escape(body[:600])}</pre>')
            rows.append(f'<details><summary>{year} 年 · 第 {n} 题（原卷第 {page} 页）</summary><p class="tag">归类：{escape(chapter)}</p>{original}<p><a href="{source}" target="_blank">打开该题所在原卷页 ↗</a></p></details>')
        empty = '<p class="empty">当前可提取题面中未检索到这一章节的独立选择题；不按题号硬凑。</p>'
        sections.append(f'<section id="{course}-{index}"><h2>{index}. {escape(chapter)}</h2>{"".join(rows) or empty}</section>')

missing = '、'.join(map(str, missing_years)) or '无'
html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>408 分章分年真题速查 | 考研冲刺君</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f6f7fb;color:#202331;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}}header{{background:#151824;color:#fff;padding:16px 5vw}}header a{{color:#cbd3ff;text-decoration:none}}main{{max-width:1120px;margin:auto;padding:28px 5vw 80px}}h1{{margin-top:40px}}section{{background:#fff;border:1px solid #e2e5ee;border-radius:14px;padding:18px;margin:18px 0}}details{{border-top:1px solid #edf0f5;padding:10px 0}}summary{{cursor:pointer;font-weight:700}}details img{{display:block;width:100%;max-width:820px;margin:10px 0;border:1px solid #e2e5ee;border-radius:8px}}a{{color:#3857d7}}pre{{white-space:pre-wrap;background:#fafbfe;border:1px solid #edf0f5;border-radius:8px;padding:12px;max-height:360px;overflow:auto}}.note{{background:#fff8e7;border:1px solid #f0d28c;padding:14px 16px;border-radius:12px}}.tag{{color:#687083}}.empty{{color:#7a8090}}
</style></head><body><header><strong>考研冲刺君 · 408 真题速查</strong>　<a href="index.html">首页</a></header><main><h1>408 分章分年选择题速查</h1><p>题目依据本地 2014—2024 年 408 PDF 拆分；按题面关键词归入对应章节，原题页和 PDF 链接均保留。</p><div class="note"><b>核验说明：</b>文本可稳定提取的题目已分类展示。{missing} 年的 PDF 是扫描版、损坏或文本层不完整，页面不伪造题目，仍可在原卷入口查看。</div>{''.join(sections)}</main></body></html>'''
OUT.write_text(html, encoding='utf-8')
print(f'wrote {OUT}; records={sum(len(x) for x in records.values())}; limited_text_years={missing}')
