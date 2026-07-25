from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

def replace_all(path, mapping):
    text = path.read_text(encoding='utf-8')
    for old, new in mapping.items():
        if old not in text:
            raise SystemExit(f'{path.name}: missing expected link {old}')
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')

# 数学一正文目录原本沿用 Markdown 自动生成的中文锚点，实际 HTML 使用的是稳定的 _N ID。
replace_all(ROOT / 'math1.html', {
    '#第一部分高等数学': '#_3',
    '#第一章-函数极限连续': '#_4',
    '#第二章-一元函数微分学': '#_14',
    '#第三章-一元函数积分学': '#_16',
    '#第四章-向量代数与空间解析几何': '#_18',
    '#第五章-多元函数微分学': '#_20',
    '#第六章-多元函数积分学': '#_22',
    '#第七章-无穷级数': '#_24',
    '#第八章-常微分方程': '#_26',
    '#第二部分线性代数': '#_28',
    '#第一章-行列式': '#_29',
    '#第二章-矩阵': '#_31',
    '#第三章-向量': '#_37',
    '#第四章-线性方程组': '#_39',
    '#第五章-特征值与特征向量': '#_41',
    '#第六章-二次型': '#_43',
    '#第三部分概率论与数理统计': '#_45',
    '#第一章-随机事件与概率': '#_46',
    '#第二章-一维随机变量及其分布': '#_48',
    '#第三章-多维随机变量及其分布': '#_50',
    '#第四章-数字特征': '#_52',
    '#第五章-大数定律与中心极限定理': '#_54',
    '#第六章-数理统计的基本概念': '#_56',
    '#第七章-参数估计': '#_58',
    '#第八章-假设检验': '#_60',
})

replace_all(ROOT / 'english1.html', {
    '#第一部分阅读理解a40分重中之重': '#a40',
    '#第二部分阅读理解b新题型10分': '#b10',
    '#第三部分完形填空10分': '#10',
    '#第四部分翻译10分': '#10_1',
    '#第五部分写作30分': '#30',
    '#第六部分词汇与语法基础': '#_18',
    '#第七部分备考时间规划与策略': '#_22',
    '#附录': '#_25',
})

# 408 三门课程的“典型例题”目录此前全部指向不存在的占位 ID。
for filename in ('ds.html', 'co.html', 'os.html'):
    path = ROOT / filename
    text = path.read_text(encoding='utf-8')
    count = text.count('<h3>【典型例题解析】</h3>')
    if not count:
        raise SystemExit(f'{filename}: no example headings found')
    state = [0]
    def add_example_id(_):
        state[0] += 1
        return f'<h3 id="examples-{state[0]}">【典型例题解析】</h3>'
    text = text.replace('<h3>【典型例题解析】</h3>', '') if False else text
    text, changed = re.subn(r'<h3>【典型例题解析】</h3>', add_example_id, text)
    if changed != count:
        raise SystemExit(f'{filename}: expected {count} example heading replacements, got {changed}')
    link_state = [0]
    def fix_example_link(_):
        link_state[0] += 1
        return f'href="#examples-{link_state[0]}"'
    text, links = re.subn(r'href="#_examples"', fix_example_link, text)
    if links != count:
        raise SystemExit(f'{filename}: expected {count} example links, got {links}')
    path.write_text(text, encoding='utf-8')

# 计网第六章在内容扩充后重新编号，目录保留的是旧编号。
replace_all(ROOT / 'cn.html', {
    'href="#_30"': 'href="#_2"',
    'href="#_31"': 'href="#_3"',
    'href="#_32"': 'href="#_4"',
    'href="#_33"': 'href="#_5"',
})

# 计划 Markdown 不在静态站目录中；首页的两个入口统一跳到站内的三阶段计划区。
replace_all(ROOT / 'index.html', {
    'href="备考计划/冲刺备考计划.md"': 'href="#plan"',
})

print('navigation repair complete')
