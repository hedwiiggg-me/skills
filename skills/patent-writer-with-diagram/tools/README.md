# tools / 辅助脚本

本目录存放**可重复执行的辅助脚本**。技能主流程以 `SKILL.md` 与 `prompts/` 为准。

## 脚本列表

| 脚本 | 用途 |
|------|------|
| `generate_patent_docx.js` | **（主入口）** 从 JSON 数据生成带插图的 .docx 文件。依赖 `docx` npm 包。 |
| `generate_patent_docx.py` | Python 版 docx 生成（备选）。依赖 `python-docx`。 |
| `gen_flow_chart.py` | 用 matplotlib 生成交互流程草图（流程图）。依赖 `matplotlib`。 |
| `md_to_docx.py` | 将 Markdown 转为 Word（.docx），按标题层级映射为 Word 内置标题样式。依赖 `python-docx`。 |

## 依赖安装

```bash
# Python 依赖
pip install -r requirements.txt

# Node.js 依赖
npm install -g docx
```

## md_to_docx.py — Markdown → Word

将 Markdown 转为 `.docx`，`#`–`######` 映射为 Word 内置「标题 1」–「标题 9」。

```bash
python3 tools/md_to_docx.py -i disclosure.md -o disclosure.docx
```

支持：ATX 标题、段落、**粗体**、行内代码、无序/有序列表、围栏代码块、GFM 表格、引用块、水平线、行内图片。

## gen_flow_chart.py — 流程图

```bash
python3 scripts/gen_flow_chart.py
```
