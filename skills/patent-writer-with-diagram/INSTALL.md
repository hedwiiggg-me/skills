# 安装说明

本技能遵循 [AgentSkills](https://agentskills.io) 常见布局：技能子目录内含 `SKILL.md`。

## Claude Code

```bash
mkdir -p .claude/skills
# 克隆整个集合仓库
git clone <本仓库 URL> .claude/skills/skills-collection
# 或使用本地路径将本技能目录复制到 .claude/skills/ 下
cp -r skills/patent-writer-with-diagram .claude/skills/patent-writer-with-diagram
```

## Cursor

将本目录复制到：
- 全局：`~/.cursor/skills/patent-writer-with-diagram/`
- 项目：`<项目根>/.cursor/skills/patent-writer-with-diagram/`

## 依赖

### Node.js（docx 生成）

```bash
# 检查
node -e "require('docx')" 2>/dev/null && echo "已安装" || npm install -g docx
```

### Python（流程图、备选转换）

```bash
pip install -r requirements.txt
```
