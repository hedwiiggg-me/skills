# Figma 配图流程（Step 2a）

**⚠️ 强制约束：只要用户提供了 Figma 链接，必须完成关键帧图片的下载和插入，否则任务不得视为完成。不允许以任何理由跳过插图步骤。**

## 配图原则

- **每帧 = 一张图 = 一个交互状态**。必须真正下载图片到本地并验证文件存在后，才能写入 JSON、生成 docx。
- 不能只做文字分析，图片必须实际插入 Word 文档。
- **工具分工**：Figma MCP 负责解析设计结构和交互状态语义；Figma Personal Access Token + API 负责将图片下载到本地。两者缺一不可。

## 执行步骤

### 1. 检查 Figma MCP

尝试调用 `mcp__figma-remote-mcp__get_design_context`，如果工具不存在，停止流程并提示用户安装。

### 2. 解析 Figma 链接

从 URL 中提取 `fileKey` 和 `nodeId`（格式转换：URL 中的 `1-2` → API 用 `1:2`）。

### 3. 用 MCP 解析设计结构

调用 `mcp__figma-remote-mcp__get_design_context` 获取目标节点的子帧结构和交互状态信息。

### 4. 确认 Figma Personal Access Token

```bash
# 优先读取本地缓存
TOKEN=$(cat ~/.figma_token 2>/dev/null)
```

- 若 `~/.figma_token` 存在且非空，直接使用
- 若不存在，提示用户提供并保存到 `~/.figma_token`

### 5. 获取子节点列表

```bash
curl -s "https://api.figma.com/v1/files/{fileKey}/nodes?ids={nodeId}" \
  -H "X-Figma-Token: {token}"
```

取 `children` 中 type 为 `FRAME`/`GROUP`/`COMPONENT` 的子节点 id 和 name。

### 6. 分析每帧交互状态

常见状态：默认态、悬停态、激活态/选中态、加载态、空态、错误态、完成态、展开/收起态、拖拽态/吸附态。

每个子帧独立保留为独立图片，**不要把多个状态合并**。帧名称即状态描述。

### 7. 批量获取图片 URL 并逐个下载

```bash
curl -s "https://api.figma.com/v1/images/{fileKey}?ids={id1},{id2}&format=png&scale=2" \
  -H "X-Figma-Token: {token}"
curl -L -s "{url1}" -o /tmp/figma_img_1.png
curl -L -s "{url2}" -o /tmp/figma_img_2.png
```

- 图片 URL 有效期极短，获取后**立即逐个下载**
- 下载后用 `ls -lh` 验证文件大小 > 0

### 8. 生成图文标注

每张图生成：
- `caption`：`图N：{帧名称} — {状态描述}`
- `annotations`：简明扼要的说明，描述状态触发条件、视觉呈现

**每帧对应 `figma_images` 数组中一个独立对象**，严格一一对应。
