<div align="center">

# 专利交底书撰写 Skill

> 从产品描述到**可交付的技术交底书**：信息采集、Figma 配图、技术架构图、自动生成 Word。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../LICENSE)

</div>

## 功能特性

| 能力 | 说明 |
|------|------|
| **信息采集** | 引导填写专利名称、类型、发明人、联系人等必填信息 |
| **正文撰写** | 按标准模版结构撰写第1-4节 |
| **Figma 配图** | 从 Figma 设计稿下载关键帧图片插入文档 |
| **技术架构图** | SVG 架构图生成 + PNG 转换（发明专利必须） |
| **Docx 生成** | 自动生成带插图的 .docx 文件 |

## 安装

### Claude Code

```bash
# 克隆到 .claude/skills 子目录
mkdir -p .claude/skills
git clone <本仓库 URL> .claude/skills/skills-collection
```

### Cursor

将本目录链接到 Cursor skills 路径：

```bash
ln -s $(pwd)/skills/patent-writer-with-diagram ~/.cursor/skills/patent-writer-with-diagram
```

## 依赖

```bash
# Node.js docx 包（docx 生成）
npm install -g docx

# Python 包（流程图备选）
pip install -r requirements.txt
```

## 使用

在 Agent 中用自然语言描述需求即可，例如：
- "写个专利技术交底书"
- "帮我申请专利"
- "把这套交互方案写成专利文档"
