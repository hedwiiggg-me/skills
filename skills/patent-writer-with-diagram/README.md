<div align="center">

# 📝 专利技术交底书撰写 Skill

> **从产品想法到可交付的专利申请文档 — 全流程 AI 辅助撰写工具**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-docx-339933.svg)](https://nodejs.org/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Figma](https://img.shields.io/badge/Figma-配图-F24E1E.svg)](https://www.figma.com)

<br>

有产品方案或交互设计，但**专利交底书不知道怎么写**？<br>
需要**系统架构图**和**交互截图**，还要**代理人能直接改的 Word 文档**？<br>
Figma 设计稿已经有了，想把**关键帧直接插入专利文档**？

**本 Skill 覆盖从信息采集到生成 .docx 的全流程，一键产出可交付的技术交底书。**

</div>

---

## ✨ 核心能力

### 🎯 支持两种专利类型

| 专利类型 | 说明 |
|----------|------|
| **发明专利** | 完整技术方案描述 + 技术架构图（SVG+PNG）+ 交互流程 |
| **外观设计专利** | 交互行为描述 + 视觉呈现 + 设计思路 |

### 🔧 自动化能力

| 能力 | 说明 |
|------|------|
| **📋 信息智能采集** | 引导式问答，自动补齐专利名称、类型、发明人、联系人等必填信息 |
| **✍️ 正文自动撰写** | 按标准模版结构（背景→发明要点→描述→技术实现）逐节生成 |
| **🎨 Figma 自动配图** | 从 Figma 设计稿自动下载关键帧图片，图文交织插入文档 |
| **📐 技术架构图生成** | SVG 架构图自动生成 + sharp 引擎转 PNG，发明专利强制要求 |
| **📄 Word 自动导出** | Node.js docx 引擎生成带插图的 .docx 文件，可直接提交代理人 |
| **🔄 交互流程图** | 可选 matplotlib 生成关键交互流程图 |

---

## 🎯 适用场景

- **产品经理**：有产品原型和交互设计，需要快速出专利交底书
- **设计师**：Figma 设计稿已完成，需要提取关键帧用于专利申请
- **研发工程师**：有技术方案实现，需要撰写发明专利技术交底书
- **知识产权专员**：协助业务部门将创新点转化为标准专利文档

---

## 🚀 快速开始

### 1. 安装

```bash
# Claude Code — 克隆到技能目录
mkdir -p .claude/skills
git clone git@github.com:hedwiiggg-me/skills.git .claude/skills/skills-collection

# 安装 Node.js 依赖（docx 生成）
npm install -g docx

# 安装 Python 依赖（流程图备选）
pip install -r requirements.txt
```

### 2. 使用

在对话中用自然语言描述需求：

> "帮我写个专利技术交底书，我们做了一个 AI 智能客服系统..."

Agent 会自动执行完整工作流：
1. 引导填写基本信息
2. 按标准模版撰写正文
3. 如有 Figma 链接 → 自动下载配图
4. 发明专利 → 自动生成技术架构图
5. 输出 .docx 文件

---

## 📖 工作流程

### Step 1 — 信息采集
Agent 会引导你补齐专利名称、类型、发明人、联系人信息，以及核心创新点描述。

### Step 2 — 正文撰写
按照标准技术交底书模版，逐节生成：
- **第1节 背景**：问题描述 + 现有方案缺点
- **第2节 发明要点**：核心方案概括 + 优势
- **第3节 描述**：按场景分条描述交互行为
- **第4节 技术实现**：发明专利的技术细节

### Step 2a — Figma 配图（可选）
如果你提供了 Figma 链接，Agent 会：
1. 解析 Figma 设计结构
2. 识别各帧的交互状态
3. 下载关键帧图片
4. 图文交织插入文档

### Step 3 — 技术架构图（发明专利必须）
自动生成 SVG 架构图，按功能分区、箭头颜色语义化，转为 PNG 插入文档。

### Step 4 — 生成 .docx
将所有内容打包为 JSON，调用 docx 引擎一步生成带插图的 Word 文档。

---

## 📁 目录结构

```
patent-writer-with-diagram/
├── SKILL.md                    # 技能入口：触发条件、步骤映射、工具表
├── prompts/                    # 分步指令（Agent 逐步骤执行）
│   ├── intake.md               # Step 1：信息采集
│   ├── disclosure_builder.md   # Step 2：正文撰写
│   ├── figma_workflow.md       # Step 2a：Figma 配图流程
│   ├── svg_arch_diagram.md     # Step 3：技术架构图生成
│   ├── docx_generation.md      # Step 4：Docx 生成
│   └── template_reference.md   # 交底书模版细则与 JSON 数据模型
├── scripts/                    # 核心生成脚本
│   ├── generate_patent_docx.js # JSON → .docx（主引擎，Node.js）
│   ├── generate_patent_docx.py # Python 备选
│   └── gen_flow_chart.py       # matplotlib 流程图
├── tools/                      # 辅助工具
│   ├── md_to_docx.py           # Markdown → Word 转换
│   └── README.md               # 工具使用说明
├── references/                 # 参考文件
│   ├── examples.md             # 案例参考
│   ├── diagram-style.md        # SVG 架构图颜色、字体、箭头规范
│   └── diagram-layout.md       # 架构图布局规则
├── docs/
│   └── skill-structure.md      # 工程结构说明
├── README.md                   # 本文件
├── INSTALL.md                  # 安装说明
└── requirements.txt            # Python 依赖
```

---

## 📋 使用建议

| 场景 | 建议触发词 |
|------|-----------|
| 首次撰写 | "写个专利"、"申请专利"、"技术交底书" |
| 发明专利 | "写个发明专利"、"技术方案想申请专利" |
| 外观设计 | "写个外观专利"、"这套界面想申请专利" |
| 有 Figma 稿 | "Figma 链接是 xxx，帮我写成专利" |
| 修改完善 | "第3节改一下"、"补充一些实施例" |

---

## 🔧 技术栈

- **Node.js** — docx 文档生成引擎（`docx` npm 包）
- **Python 3** — SVG 架构图构建、matplotlib 流程图
- **sharp / rsvg-convert** — SVG → PNG 转换
- **Figma REST API** — 设计稿图片下载
- **Figma MCP** — 设计结构解析

---

## 📄 输出格式

- **Word (.docx)** — 标准技术交底书格式，含插图，可直接提交专利代理人
- **命名规范**：`{专利名称}-技术交底书.docx`

---

## 🤝 贡献

欢迎提交 Issue 或 PR 改进本技能！

---

<div align="center">

MIT License © [Hedwig](https://github.com/hedwiiggg-me)

</div>
