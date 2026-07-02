# 技术架构图生成（Step 3）

**⚠️ 强制约束：只要专利类型为"发明"，必须生成技术架构图。不允许以任何理由跳过此步骤。**

## 规则

- 技术步骤多（3步以上）→ 每步一张架构图
- 技术相对单一 → 一张综合架构图
- 用户明确说不需要 → 跳过

## 样式规范

加载 `references/diagram-style.md` 获取颜色、字体、箭头的完整 SVG 规范。
布局规则参考 `references/diagram-layout.md`。

## 强制约束

使用 **Python list 方法逐行构建 SVG**，禁止直接拼接长字符串：

```python
python3 << 'EOF'
lines = []
lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 620" width="1200" height="620">')
lines.append('<style>text{font-family:"PingFang SC","Microsoft YaHei","Helvetica Neue",Arial,sans-serif;}</style>')
# ... 逐行添加
lines.append('</svg>')
with open('/tmp/diag_stepN.svg', 'w') as f:
    f.write('\n'.join(lines))
EOF
```

## 布局原则

- 按功能分区（输入层 / 计算层 / 判断层 / 输出层），每区用圆角矩形背景区分
- 节点全部使用中文标签，副标签用浅色小字补充说明
- 箭头颜色语义化：蓝=主流程、绿=成功路径、红=失败/降级、橙=补充条件、紫=索引/写入
- 判断节点用菱形（`<polygon>`），存储节点用圆角矩形加深色边框
- 每张图底部必须包含图例（当使用 2 种以上箭头颜色时）
- 所有箭头标签必须加白色背景矩形，防止与连线重叠

## SVG → PNG 转换

```bash
# 方式1：sharp（Node.js）
NODE_PATH=/usr/local/lib/node_modules node -e "
const sharp=require('sharp'),fs=require('fs');
sharp(fs.readFileSync('/tmp/diag_stepN.svg'),{density:180}).png().toFile('/tmp/arch_stepN.png');
"

# 方式2：rsvg-convert
rsvg-convert -w 1920 /tmp/diag_stepN.svg -o /tmp/arch_stepN.png
```

生成后将图片路径填入 JSON 的 `arch_images` 数组。
