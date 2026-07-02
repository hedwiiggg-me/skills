<div align="center">

# Skills

> 基于 AgentSkills 标准的技能集合仓库 — 让你的 AI Agent 拥有专家级领域能力

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

<br>

技能（Skill）是赋予 AI Agent 专业知识、工作流和工具集成能力的标准化模块。  
每个技能子目录都是一个自包含的 AgentSkills 包，即插即用。

</div>

---

---

## 📝 专利交底书撰写 Skill — 写给用户

把你脑海里的产品方案、交互设计或技术实现，变成**一份可直接提交专利代理人的正式技术交底书（.docx）**。

### 你只需要提供

把你知道的说出来就行，比如：

> "我们做了一个 AI 智能客服系统，用户可以通过自然语言对话查订单、退换货，后台用大模型做意图识别和路由..."

或者扔一个 Figma 链接 + 说清楚功能点。

### 你会拿到什么

| 交付物 | 说明 |
|--------|------|
| **技术交底书 .docx** | 标准格式 Word 文档，含文头信息表、背景、发明要点、交互描述、技术实现 |
| **Figma 配图** | 如果你有 Figma 设计稿，关键帧截图会自动插入文档对应位置，图文交织 |
| **技术架构图** | 发明专利自动生成 SVG 架构图（功能分区、箭头语义化），转为 PNG 插入文档 |
| **交互流程草图** | 可选，matplotlib 生成的步骤流程图 |

### 不需要你会什么

- 不需要懂专利格式 — Agent 会按标准模版走
- 不需要懂 SVG 制图 — 架构图 Agent 自动画
- 不需要操心排版 — 最终产出一个 .docx，拿到就能发

### 一句话

**有想法 → 有产出。中间的事交给 Agent。**

---

## 📋 技能列表

| 技能 | 描述 | 入口 |
|------|------|------|
| [📝 专利交底书撰写](skills/patent-writer-with-diagram/) | 中国专利申请技术交底书撰写工具，支持发明专利和外观设计专利，内置技术架构图生成能力（SVG+PNG） | `skills/patent-writer-with-diagram/SKILL.md` |

> 更多技能陆续添加中...

---

## 🚀 快速开始

### Claude Code

```bash
mkdir -p .claude/skills
git clone git@github.com:hedwiiggg-me/skills.git .claude/skills/skills-collection
```

之后在对话中直接描述需求，Agent 会自动匹配对应技能。

### Cursor

将技能子目录链接到 Cursor 技能路径：

```bash
ln -s $(pwd)/skills/patent-writer-with-diagram ~/.cursor/skills/patent-writer-with-diagram
```

重启 Cursor 后在 **Settings → Rules** 中确认技能已被发现。

---

## 📦 仓库结构

```
skills/
├── README.md                          # 本仓库说明
├── INSTALL.md                         # 通用安装说明
├── LICENSE                            # MIT 开源许可
├── .gitignore
└── skills/                            # 技能子目录（每个技能独立文件夹）
    └── patent-writer-with-diagram/    # 专利交底书撰写技能
        ├── SKILL.md                   # 入口：触发条件、步骤映射、工具表
        ├── prompts/                   # 分步指令（Agent 逐步骤执行）
        ├── tools/                     # 辅助脚本（格式转换、图片处理）
        ├── scripts/                   # 核心生成脚本（docx 生成等）
        ├── references/                # 参考文件（案例、样式规范、模版）
        ├── docs/                      # 技能文档
        └── README.md                  # 技能详细说明
```


<div align="center">

MIT License © [Hedwig](https://github.com/hedwiiggg-me)

</div>
