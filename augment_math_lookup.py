from pathlib import Path
import re
from html import escape

p = Path(__file__).resolve().parent / "math1.html"
s = p.read_text(encoding="utf-8")
marker = '<div class="chapter-original-question">'
questions = [
    "2024 选择题1：已知 f(x)=∫₀ˣ e^(cos t)dt，g(x)=∫₀^(sin x) e^(t²)dt，判断 f(x)、g(x) 的奇偶性。答案：C。考点：变限积分与奇偶性。",
    "2024 选择题4：设 f(x) 在 (-1,1) 有定义且 lim(x→0)f(x)=0，判断 f(0)、f′(0) 与 lim f(x)/x、lim f′(x) 的关系。答案：B。考点：导数定义。",
    "2024 解答题17：平面区域 D={(x,y)|1−y²≤x≤1，−1≤y≤1}，计算 ∬ᴅ x/(x²+y²) dσ。考点：二重积分与区域。",
    "2024 选择题2：曲面 Σ：z=1−x²−y² 取上侧，计算 ∬Σ P dy dz+Q dz dx。答案：A。考点：第二类曲面积分与高斯公式。",
    "2024 填空题12：z=f(u,v) 有二阶连续导数，df(1,1)=3du+4dv，y=f(cos x,1+x²)，求 y″(0)。答案：5。考点：多元复合函数求导。",
    "2024 解答题18：f(x,y)=x³+y³−(x+y)²+3，求曲面在 (1,1,1) 处的切平面，并求其在投影区域 D 上的最大值和最小值。考点：全微分、极值。",
    "2024 解答题17：在给定平面区域 D 上计算二重积分。考点：区域分解、换序和积分计算。",
    "2024 解答题20：有向曲线 L 为球面与平面的交线，计算曲线积分。考点：斯托克斯公式与方向。",
    "2024 选择题5：三张平面 πᵢ 的位置关系如图，判断系数矩阵与增广矩阵的秩。答案：B。考点：空间平面与线性方程组。",
    "2024 选择题7：A 为秩 2 的三阶矩阵，Aα=0，且在 α 的正交补上为恒等映射，求 A 的迹。答案：A。考点：矩阵秩、特征值与迹。",
    "2024 选择题6：三个四维向量线性相关但任意两向量无关，判断参数 a,b。答案：D。考点：向量组线性相关。",
    "2024 选择题5：由三张平面的位置关系判断系数矩阵和增广矩阵的秩。答案：B。考点：非齐次线性方程组。",
    "2024 选择题7：已知矩阵秩为 2、零空间含非零向量且在其正交补上为恒等映射，求矩阵的迹。答案：A。考点：特征值与特征向量。",
    "2024 填空题15：实矩阵 A 满足 (αᵀAβ)²≤(αᵀAα)(βᵀAβ)，求参数 a 的范围。考点：二次型与正定性。",
    "2024 填空题16：每次试验成功概率为 p，独立重复三次，已知至少成功一次条件下全部成功的概率为 4/13，求 p。答案：2/3。考点：条件概率。",
    "2024 选择题8：X~N(0,2)、Y~N(−2,2) 且相互独立，若 P{2X+Y<a}=P{X>Y}，求 a。答案：B。考点：正态分布线性组合。",
    "2024 选择题9：X 的密度为 2(1−x),0<x<1；给定 X=x 时 Y 在 (x,1) 上均匀分布，求 cov(X,Y)。答案：D。考点：二维随机变量与协方差。",
    "2024 选择题9：给定条件分布求 cov(X,Y)。答案：D。考点：条件期望与数字特征。",
    "2024 选择题10：X、Y 相互独立且都服从参数为 λ 的指数分布，令 Z=X−Y，判断与 Z 同分布的随机变量。答案：D。考点：随机变量函数分布。",
    "2024 解答题22：总体 X~U(0,θ)，X_(n)=max Xi，Tc=cX_(n)，求 c 使 Tc 为无偏估计并使均方误差最小。考点：点估计与估计量评价。",
    "2024 解答题22：总体 X~U(0,θ)，求参数 θ 的无偏估计与最小均方误差估计。考点：参数估计。",
    "2024 试卷未单独设置假设检验大题；复习本章时结合历年 PDF 中的检验统计量、拒绝域和 p 值原题训练。"
]

blocks = [f'{marker}<details><summary>2024 年对应原题</summary><p>{escape(q)}</p><p><a href="../../11408_zhenti/shuxue1/shuxue1_2024.pdf" target="_blank">打开 2024 数学一原始 PDF ↗</a></p></details></div>' for q in questions]
pattern = re.compile(r'(<h3[^>]*>[^<]*【真题速查】[^<]*</h3>.*?</table>)', re.S)
idx = 0
def repl(m):
    global idx
    if idx >= len(blocks):
        return m.group(1)
    out = m.group(1) + blocks[idx]
    idx += 1
    return out
s2 = pattern.sub(repl, s)
if idx != len(blocks):
    raise SystemExit(f"expected {len(blocks)} lookup tables, found {idx}")
p.write_text(s2, encoding="utf-8")
print(f"augmented {idx} chapter lookups")
