---
name: patent-writer-with-diagram
description: "中国专利申请技术交底书撰写工具，支持发明专利和外观设计专利，内置技术架构图生成能力（SVG+PNG）。当用户描述产品功能、交互设计或技术方案，需要生成专利申请文档或技术交底书时使用。输出标准格式的 .docx 技术交底书文件，含架构图插图。触发词：写专利、申请专利、专利文档、技术交底书、发明专利、外观专利、专利申请。"
version: "2.0.0"
user-invocable: true
argument-hint: "[可选：专利名称或技术主题关键词]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
---

# 专利技术交底书撰写

本技能覆盖 **信息采集** → **撰写各章节** → **Figma 配图** → **技术架构图** → **Docx 生成** 全流程；分步指令在 **`prompts/`**，每步执行前 **`Read`** 对应文件。

## 环境与约定

- **语言**：默认与用户语种一致；专利与法律术语采用行业常用表述。
- **Docx 生成**：JSON → `scripts/generate_patent_docx.js`（Node.js + docx 包），见 `prompts/docx_generation.md`。
- **SVG 架构图**：Python list 逐行构建 SVG，sharp/rsvg-convert 转 PNG，见 `prompts/svg_arch_diagram.md`。

---

## 触发条件

在用户使用以下任一方式时启用本技能：

- 明确提及：写专利、申请专利、专利文档、技术交底书、发明专利、外观专利、专利申请
- 斜杠或简短指令：如 `/patent-writer-with-diagram`、`/专利撰写`
- **迭代模式**：当用户意图明显是在**已有交底书或上一轮输出**上继续工作（改章节、补内容、调整表述等），直接进入对应修改流程，不重复执行"收集信息"步骤。

---

## 工具与数据来源

| 任务 | 建议方式 |
|------|----------|
| 加载分步指令 | **`Read`** → `${CLAUDE_SKILL_DIR}/prompts/*.md`，见下表 |
| 读代码、设计文档、PDF、图片 | 文件读取工具 |
| Figma 设计解析与截图 | `mcp__figma-remote-mcp__get_design_context` + Figma API |
| SVG 架构图生成 | `python3` + sharp/rsvg-convert 转 PNG |
| Docx 生成 | `node scripts/generate_patent_docx.js --input <json> --output <docx>` |
| 联网查新 | WebSearch（Google 学术 / 专利） |

---

## Prompt 文件映射

| 步骤 | 文件 | 用途 |
|------|------|------|
| Step 1 | `prompts/intake.md` | 收集基本信息与核心内容 |
| Step 2 | `prompts/disclosure_builder.md` | 撰写第1-3节正文内容 |
| Step 2a | `prompts/figma_workflow.md` | Figma 配图流程（有 Figma 链接时执行） |
| Step 3 | `prompts/svg_arch_diagram.md` | 生成技术架构图（发明专利必须） |
| Step 4 | `prompts/docx_generation.md` | 生成 .docx 文件 |
| 参考 | `prompts/template_reference.md` | 交底书章节细则与模版 |

---

## 主流程（执行顺序）

1. **`Read`** `intake.md` → 执行 Step 1，收集必填信息
2. **`Read`** `disclosure_builder.md` → 执行 Step 2，撰写各章节内容（含 template_reference.md 作为参考）
3. 若用户提供了 Figma 链接：**`Read`** `figma_workflow.md` → 执行 Figma 配图
4. **`Read`** `svg_arch_diagram.md` → 执行 Step 3，生成技术架构图（发明专利必须）
5. **`Read`** `docx_generation.md` → 执行 Step 4，生成 .docx 文件
6. 交付时输出文件路径并询问是否需要修改

---

## Agent 自用工作流检查清单

```
□ 已按步骤 Read 对应 prompts
□ 基本信息已收集齐全（名称、类型、发明人、联系人）
□ 正文严格按照模版结构撰写，未省略任何子标题
□ 用户提供 Figma 链接时：已完成关键帧下载和插入
□ 发明专利：已完成技术架构图生成
□ 已生成 .docx 文件并交付
□ 已在回复中附权利要求偏向点建议交互
```
