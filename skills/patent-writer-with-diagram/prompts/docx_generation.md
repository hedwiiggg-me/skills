# Docx 文件生成（Step 4）

## 前置检查

在生成文档前，自动检测依赖是否已安装，缺少则自动补齐：

```bash
# Node.js docx 包
node -e "require('docx')" 2>/dev/null \
  && echo "docx 已安装" \
  || (echo "正在安装 docx..." && npm install -g docx)

# Python matplotlib（交互流程图）
python3 -c "import matplotlib" 2>/dev/null \
  && echo "matplotlib 已安装" \
  || (echo "正在安装 matplotlib..." && pip3 install matplotlib)
```

## 生成流程

1. 将已撰写的全部内容整理为完整 JSON
2. 运行 `scripts/generate_patent_docx.js` 生成 .docx

```bash
NODE_PATH=/usr/local/lib/node_modules node scripts/generate_patent_docx.js \
  --input /tmp/patent-data.json \
  --output "$HOME/Desktop/{专利名称}-技术交底书.docx"
```

## JSON 结构

详见 `prompts/template_reference.md` 中的数据模型定义。

关键字段说明：
- `figma_images[].scene_index`：对应 `description_scenes` 数组下标（从0开始），图片紧跟在该场景文字之后
- `tech_scenes`：第4节技术实现的分步描述，发明专利必填
- `arch_images`：技术架构图，通过 `scene_index` 绑定到 `tech_scenes` 对应步骤
- `flow_chart_scenes`：关键交互流程草图，追加在第4节末尾

## 输出文件命名

`{专利名称}-技术交底书.docx`
