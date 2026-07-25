from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TXT = ROOT / "tmp" / "pdfs" / "408" / "408_2024.txt"
OUT = ROOT / "website" / "408_choice.html"

raw = TXT.read_text(encoding="utf-8", errors="ignore")
raw = raw.split("二、综合应用题", 1)[0]

answers = "D A A B D A D A B C D B B C D D C B C B A C A A D A A B A C C C B C D B D D C D".split()
topics = [
    ("数据结构·线性表", "逐句追踪指针：q 先摘下，再接到 h->next，因此是把 q 插到链表头部。"),
    ("数据结构·栈与表达式", "先处理括号 z-u，再做乘除，最后与 x 相加；后缀为 xyzu-*v/+。"),
    ("数据结构·二叉树遍历", "中序中 p、v、q 连续，p 不能有右子树，q 不能有左子树，否则两者之间会插入新结点。"),
    ("数据结构·图", "邻接多重表中逐条数与 b、d 相 incident 的边，度分别为 2、4。"),
    ("数据结构·查找", "折半查找要求有序且能随机访问；四种对象中均有一项条件不满足，选 D。"),
    ("数据结构·KMP", "修正 next 值为 [-1,-1,1,-1,-1,1]，最长滑动距离是 5。"),
    ("数据结构·二叉搜索树", "利用左子树小于根、右子树大于根，T 同时落在 K3 的右侧和 K2 的左侧。"),
    ("数据结构·快速排序", "一趟划分只保证枢轴左侧整体不大于右侧，P、Q 内部仍未必有序。"),
    ("数据结构·堆", "删除最大值后把末元素下移调整，再删除新的堆顶并调整，得到 B。"),
    ("数据结构·归并排序", "第一次归并比较 2 次，第二次比较 3 次，总数为 5。"),
    ("数据结构·败者树", "升序多路归并每次要选最小关键字；冠军结点记录其所在归并段号。"),
    ("组成原理·整数表示", "32777 转入 16 位 short 后保留低 16 位并按符号扩展，结果为 -32759。"),
    ("组成原理·指令系统", "CPU 直接执行机器指令和微指令，伪指令与汇编指令需先转换。"),
    ("组成原理·数据表示", "2^20 范围可用 32 位整数精确表示；2^40 量级需双精度浮点数。"),
    ("组成原理·乘法器", "变量乘变量也可用移位加法循环实现，因此 D 的“无法”表述错误。"),
    ("组成原理·存储层次", "主存—外存采用页式管理，不是 Cache 那种直接映射，D 错。"),
    ("组成原理·TLB", "页大小 1KB 得页内偏移 10 位；虚页号 22 位，32 项四路有 8 组，组号 3 位，标记 19 位。"),
    ("组成原理·地址转换", "Cache 缺失由 Cache 控制逻辑检测，不属于 MMU 地址转换本身。"),
    ("组成原理·流水线", "转发不能解决所有冒险，典型 load-use 冒险仍需气泡或调整指令。"),
    ("组成原理·总线带宽", "有效传输按每周期 2 次、64 位计算：420MHz×2×8B=6.72GB/s。"),
    ("组成原理·中断 I/O", "中断屏蔽字主要控制是否屏蔽，不等同于完整确定响应优先级，A 错。"),
    ("组成原理·DMA", "DMA 控制器直接控制设备接口与主存之间的数据通路。"),
    ("操作系统·中断与系统调用", "中断可能在用户态发生，进入处理程序后才切到内核态，因此 A 错。"),
    ("操作系统·进程终止", "是否有子进程取决于具体进程，终止子进程不一定发生。"),
    ("操作系统·进程切换", "切换时要恢复 PC、栈相关寄存器和页表基址，三项都需要。"),
    ("操作系统·文件空间管理", "位图按磁盘块总数固定占用，和当前空闲块数量无关。"),
    ("操作系统·伙伴系统", "伙伴算法只合并大小相同且地址互为伙伴的空闲块。"),
    ("操作系统·线程资源", "同一进程线程共享地址空间和文件描述符，但各自拥有独立栈。"),
    ("操作系统·系统调用", "open 需要按文件名查目录并建立打开文件表项，其他调用使用 fd。"),
    ("操作系统·时间片轮转", "队尾进程先等待其余进程轮转，完成时间为 250ms，周转时间选 C。"),
    ("操作系统·I/O 缓冲", "键盘中断服务例程通常把数据写入内核缓冲区，再由系统调用复制给用户。"),
    ("操作系统·磁盘调度", "按 CSCAN 方向先服务低号请求，扫到 0 后跳到 399，再继续向低号移动并累计距离。"),
    ("计算机网络·吞吐量", "端到端吞吐量受路径最小带宽限制，即瓶颈链路带宽。"),
    ("计算机网络·数字调制", "FSK 用两个不同频率分别表示二进制 0 和 1。"),
    ("计算机网络·VLAN/ARP", "ARP 广播不能跨 VLAN，H4 的表中不会出现不同 VLAN 主机的映射。"),
    ("计算机网络·CSMA/CA", "NAV 覆盖 CTS 后剩余的数据传输、SIFS 和 ACK 时间，按题给时延相加。"),
    ("计算机网络·选择重传", "SR 对每个正确帧独立确认，结合窗口边界逐时刻跟踪序号。"),
    ("计算机网络·TCP 连接释放", "建立连接、分段传输、主动关闭和 TIME-WAIT 均需计入，最后受 2MSL 约束。"),
    ("计算机网络·UDP 校验和", "采用反码加法，最高位产生回卷进位后再取反得到校验和。"),
    ("计算机网络·HTTP", "非持久 HTTP/1.0 每个对象单独建 TCP 连接；页面 1 个加 7 个图片，按 RTT 逐次累加。"),
]

cards = []
for i, (topic, explain) in enumerate(topics, 1):
    cards.append(f'<details class="q-card"><summary>第 {i} 题｜{topic}｜答案 {answers[i-1]}</summary><p><b>考点：</b>{topic.split("·", 1)[1]}</p><p><b>解析：</b>{explain}</p><p class="q-action"><b>做题动作：</b>先圈出题干限定词（错误、至少、不一定、直接），再用本章定义或公式逐项验证。</p></details>')

html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>408选择题真题与解析 | 考研冲刺君</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f6f7fb;color:#202331;font:15px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif}}.top{{background:#151824;color:white;padding:16px 5vw;display:flex;justify-content:space-between;gap:20px;align-items:center}}.top a{{color:#cbd3ff;text-decoration:none}}main{{max-width:1100px;margin:0 auto;padding:28px 5vw 80px}}h1{{font-size:32px;margin:10px 0}}h2{{margin-top:38px}}.note{{background:#fff8e7;border:1px solid #f0d28c;padding:14px 16px;border-radius:12px}}.paper{{background:#fff;border:1px solid #e2e5ee;border-radius:14px;padding:18px;max-height:520px;overflow:auto;white-space:pre-wrap;font:13px/1.65 ui-monospace,SFMono-Regular,Menlo,monospace}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}}details{{background:#fff;border:1px solid #e2e5ee;border-radius:12px;padding:12px 15px}}summary{{cursor:pointer;font-weight:700}}details p{{margin:10px 0 0}}.q-action{{color:#687083;font-size:13px}}.links a{{display:inline-block;margin:6px 8px 6px 0;color:#3857d7}}@media(max-width:600px){{h1{{font-size:26px}}main{{padding-left:16px;padding-right:16px}}}}
</style></head><body><header class="top"><strong>考研冲刺君 · 408 选择题</strong><nav><a href="index.html">首页</a>　<a href="cs408.html">408知识体系</a></nav></header><main><p><a href="cs408.html">← 返回 408 知识体系</a></p><h1>408 选择题真题与逐题解析</h1><p>先按四门科目分类，再逐题看答案、考点和解题动作。本页先加入 2024 年 1—40 题，其他年份 PDF 已列入真题资料区，后续按同样格式补齐。</p><div class="note"><b>使用方法：</b>先独立完成题目，再展开对应题号。答案按公开真题解析资料交叉核对；遇到 PDF 中图表无法提取的题，保留原始 PDF 入口。</div><h2>2024 年原题（1—40）</h2><div class="paper">{escape(raw)}</div><h2>逐题解析</h2><div class="grid">{''.join(cards)}</div><h2>历年真题入口</h2><div class="links">{''.join(f'<a href="../../11408_zhenti/408_{y}.pdf" target="_blank">{y} 年 408 PDF ↗</a>' for y in range(2014,2025))}</div></main></body></html>'''
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(cards)} explanations")
