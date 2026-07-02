# 本技能目录结构说明

## 设计原则

- **`SKILL.md`**：入口与编排；具体写法分散在 **`prompts/`**，由执行方在运行时用 **`Read`** 加载，避免单文件过长。
- **`tools/`**：可选脚本扩展，与编排解耦。
- **`scripts/`**：核心生成脚本（docx 生成、流程图生成）。
- **`references/`**：样式规范、模版结构、案例参考。
- **`outputs/`**：用户产出，由 `.gitignore` 忽略。

## 目录一览

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 触发条件、工具映射、步骤顺序、`prompts/` 索引 |
| `prompts/intake.md` | Step 1：信息采集 |
| `prompts/disclosure_builder.md` | Step 2：撰写各章节 |
| `prompts/figma_workflow.md` | Step 2a：Figma 配图 |
| `prompts/svg_arch_diagram.md` | Step 3：技术架构图 |
| `prompts/docx_generation.md` | Step 4：Docx 生成 |
| `prompts/template_reference.md` | 交底书章节细则与 JSON 数据模型 |
| `references/diagram-style.md` | SVG 架构图颜色、字体、箭头规范 |
| `references/diagram-layout.md` | 架构图布局规则 |
| `references/examples.md` | 写作案例参考 |
| `scripts/generate_patent_docx.js` | JSON → .docx（Node.js） |
| `scripts/generate_patent_docx.py` | JSON → .docx（Python 备选） |
| `scripts/gen_flow_chart.py` | matplotlib 流程图生成 |
| `tools/md_to_docx.py` | Markdown → Word 转换 |
| `tools/README.md` | 工具说明 |

## 环境变量 `CLAUDE_SKILL_DIR`

在 Claude Code、Cursor 等环境中，常由平台将 **`CLAUDE_SKILL_DIR`** 设为技能根目录，即包含 `SKILL.md` 的目录。`${CLAUDE_SKILL_DIR}/prompts/...` 即解析到此路径。
