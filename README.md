<div align="center">

# Skills

> 基于 AgentSkills 标准的技能集合仓库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 技能列表

| 技能 | 描述 | 入口 |
|------|------|------|
| [专利交底书撰写](skills/patent-writer-with-diagram/) | 中国专利申请技术交底书撰写工具，支持发明专利和外观设计专利，内置技术架构图生成能力（SVG+PNG） | `skills/patent-writer-with-diagram/SKILL.md` |

---

## 安装

详见 [INSTALL.md](INSTALL.md)。

---

## 仓库结构

```
skills/
├── README.md                          # 本仓库说明
├── INSTALL.md                         # 通用安装说明
├── LICENSE
├── .gitignore
└── skills/                            # 技能子目录
    └── patent-writer-with-diagram/    # 专利交底书撰写技能
        ├── SKILL.md                   # 入口：触发条件、步骤映射、工具表
        ├── prompts/                   # 分步指令
        ├── tools/                     # 辅助脚本
        ├── references/                # 参考文件（示例、样式、模版）
        ├── scripts/                   # 核心生成脚本
        ├── docs/                      # 技能文档
        ├── examples/                  # 示例
        ├── README.md
        ├── INSTALL.md
        └── requirements.txt
```
