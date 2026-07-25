from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

# 2024 年 1-40 选择题已经有逐题解析；这里按课程章节放回知识点页面。
MAPPING = {
    "ds.html": [[], [(1, "单链表头插操作")], [(2, "栈与后缀表达式")], [(3, "二叉树中序遍历"), (7, "二叉搜索树性质")], [(4, "图的邻接多重表与顶点度")], [(5, "折半查找适用条件"), (6, "KMP 的 nextval")], [(8, "快速排序一趟划分"), (9, "大根堆删除"), (10, "归并排序比较次数"), (11, "败者树")]],
    "co.html": [[(13, "机器指令、汇编指令与微指令")], [(12, "整数表示"), (14, "浮点数精度"), (15, "乘法器")], [(16, "存储层次"), (17, "TLB 标记字段"), (18, "Cache 与地址转换")], [(13, "指令系统层次")], [(19, "流水线数据冒险")], [(20, "总线带宽")], [(21, "中断 I/O"), (22, "DMA")]],
    "os.html": [[(23, "中断与系统调用"), (29, "系统调用接口")], [(24, "进程终止"), (25, "进程切换现场"), (28, "线程资源"), (30, "时间片轮转")], [(27, "伙伴系统")], [(26, "文件空间位图"), (32, "磁盘调度")], [(31, "I/O 缓冲")]],
    "cn.html": [[(33, "端到端吞吐量")], [(34, "数字调制 FSK")], [(35, "VLAN 与 ARP"), (36, "CSMA/CA 与 NAV")], [(37, "选择重传 SR")], [(38, "TCP 连接释放"), (39, "UDP 校验和")], [(40, "HTTP 非持久连接")]],
}

ANCHORS = {
    "ds.html": [f"ds-{i}" for i in range(1, 8)],
    "co.html": [f"co-{i}" for i in range(1, 8)],
    "os.html": [f"os-{i}" for i in range(1, 6)],
    "cn.html": [f"cn-{i}" for i in range(1, 7)],
}

CSS = '''<style>.chapter-408-papers{margin:12px 0 22px;border:1px solid #d9e0f5;border-radius:10px;background:#f8faff;padding:10px 14px}.chapter-408-papers>p{color:#687083;font-size:13px}.chapter-408-papers ul{margin:8px 0;padding-left:22px}.chapter-408-papers a{color:#3857d7;font-weight:700}.chapter-408-papers details{border-top:1px solid #dfe5f2;padding:10px 0}.chapter-408-papers summary{cursor:pointer;font-weight:700;color:#263a8d}.chapter-408-papers img{display:block;max-width:820px;width:100%;margin:10px 0;border:1px solid #e2e5ee;border-radius:8px}.chapter-408-papers pre{white-space:pre-wrap;background:#fff;border:1px solid #e2e5ee;border-radius:8px;padding:12px;max-height:360px;overflow:auto}</style>'''

LOOKUP = (ROOT / '408_chapter_lookup.html').read_text(encoding='utf-8')

def chapter_entries(anchor):
    match = re.search(rf'<section id="{re.escape(anchor)}"><h2>.*?</h2>(.*?)</section>', LOOKUP, re.S)
    if not match:
        return '<p>本章真题正在整理中。</p>'
    return match.group(1)

def make_panel(numbers, anchor):
    links = ''.join(f'<li><a href="408_choice.html#q{n}" target="_blank">2024 年第 {n} 题 · {topic}：原题与逐题解析 ↗</a></li>' for n, topic in numbers)
    if not links:
        links = '<li>2024 年选择题未单独覆盖本章；不按题号硬凑，建议查看历年原卷或本章例题。</li>'
    return f'''<!-- 408-PAPERS-START -->
<div class="chapter-408-papers">
<p><b>逐题真题：</b>先阅读上方知识点，再按年份展开下列原题；每道题均已对应本章节知识点。</p>
<ul>{links}</ul>
<p><a href="408_choice.html" target="_blank">查看 2024 年 408 选择题逐题解析 ↗</a>　|　<a href="../../11408_zhenti/408_2024.pdf" target="_blank">打开 2024 年原始 408 PDF ↗</a></p>
{chapter_entries(anchor)}
<p><a href="408_chapter_lookup.html#{anchor}" target="_blank">在独立页面查看本章 2014—2024 真题 ↗</a>　|　<a href="408_choice.html#all-papers" target="_blank">查看全部 408 原卷入口 ↗</a></p>
</div>
<!-- 408-PAPERS-END -->'''

for filename, panels in MAPPING.items():
    path = ROOT / filename
    html = path.read_text(encoding="utf-8")
    # 支持重新生成：先清除本脚本上一次插入的面板，以及旧版 iframe 面板。
    html = re.sub(r'<!-- 408-PAPERS-START -->.*?<!-- 408-PAPERS-END -->', '', html, flags=re.S)
    html = re.sub(r'<details class="chapter-408-papers">.*?</details>', '', html, flags=re.S)
    if '</head>' not in html:
        raise SystemExit(f"{filename} has no head")
    html = html.replace('</head>', CSS + '</head>', 1)
    pattern = re.compile(r'(<h3\b[^>]*>【真题速查】</h3>(?:\s*<div style="text-align:center[^>]*><img src="images/[^"]+"[^>]*></div>)*\s*<table\b.*?</table>)', re.S)
    state = [0]
    def repl(match):
        if state[0] >= len(panels):
            return match.group(1)
        panel = make_panel(panels[state[0]], ANCHORS[filename][state[0]])
        state[0] += 1
        return match.group(1) + panel
    html = pattern.sub(repl, html)
    if state[0] != len(panels):
        raise SystemExit(f"{filename}: expected {len(panels)} tables, embedded {state[0]}")
    path.write_text(html, encoding="utf-8")
    print(f"{filename}: embedded {state[0]} chapter panels")

# Add stable anchors so the chapter cards can point to the existing 2024 question explanations.
choice = ROOT / '408_choice.html'
html = choice.read_text(encoding='utf-8')
if 'id="q1"' not in html:
    number = [0]
    def anchor(match):
        number[0] += 1
        return f'<details class="q-card" id="q{number[0]}">'
    html, count = re.subn(r'<details class="q-card">', anchor, html)
    if count != 40:
        raise SystemExit(f"408_choice.html: expected 40 question cards, found {count}")
    html = html.replace('<h2>历年真题入口</h2>', '<h2 id="all-papers">历年真题入口</h2>', 1)
    choice.write_text(html, encoding='utf-8')
    print('408_choice.html: added 40 question anchors')
