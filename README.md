# 考研冲刺君

面向考研学子的免费知识体系网站：数学一、英语一、408 计算机学科专业基础，知识体系全解 + 图解例题 + 历年真题。

**在线访问（主站，ICP 备案）**：https://zehaowang.xin

**备用地址（GitHub Pages）**：https://jinghao-leon.github.io/kaoyan-chongcijun/

## 内容一览

### 408 计算机学科专业基础（数据结构 / 计组 / OS / 计网）

- `cs408.html` — 四门课知识体系总览页（王道风格：必背考点、核心概念、例题、易错警示、真题速查）
- `ds.html` / `co.html` / `os.html` / `cn.html` — 四科分页，每章结构：
  - **章首**：知识点图解卡（Cache 映射、PV 操作、握手时序、流水线等难点的步骤图）
  - **正文**：完整知识体系讲解
  - **章末**：6 道例题卡（选项对错标注 + 答案 + 解析）+ 历年真题面板
- `408_choice.html` — 2024 年 408 选择题逐题解析
- `408_chapter_lookup.html` — 2014—2024 分章分年真题速查（含原卷页截图）
- `zhenti/` — 历年真题 PDF：408（2014—2024）、数学一、英语一

### 数学一

- `math1.html` — 高数 8 章 + 线代 6 章 + 概率统计 8 章全解，难点章节（多元微分、曲线曲面积分、线性相关、多维分布、抽样分布、参数估计等）配有 16 张图解卡
- `math_chapter_lookup.html` — 分章真题速查
- `math_pastpapers.html` — 历年真题

### 英语一

- `english1.html` — 阅读六大题型方法论、新题型、完形、翻译、大小作文模板
- `english5000.html` — 核心词汇
- `english_pastpapers.html` — 历年真题

## 技术说明

- 纯静态站点（HTML + CSS + 少量原生 JS + KaTeX），无构建依赖，GitHub Pages 直接托管
- 图解卡与例题卡图片由 AI 生成并经人工逐张核对
- 知识体系源文件为 Markdown，经脚本转换为 HTML 后再嵌入图片与真题面板

## 本地预览

```bash
cd website
python3 -m http.server 8080
# 打开 http://localhost:8080
```

## 声明

本站内容仅供学习交流使用，历年真题版权归原命题单位所有。
