# 安装说明

本仓库遵循 [AgentSkills](https://agentskills.io) 约定：每个技能是一个子文件夹，内含根级 `SKILL.md`。

## Claude Code

在 **git 仓库根目录** 下安装：

```bash
mkdir -p .claude/skills
git clone <本仓库 URL> .claude/skills/skills-collection
```

或使用本地路径复制到 `.claude/skills/` 下。

## Cursor

Cursor 支持 [Agent Skills](https://www.cursor.com/docs/context/skills) 约定。将本仓库完整内容放在下列位置之一，重启 Cursor 后在 **Settings → Rules** 中查看是否已被发现。

### 用户主目录（全局，所有项目可用）

| 系统 | 推荐路径 |
|------|----------|
| Windows | `%USERPROFILE%\.cursor\skills\<技能名>\`（即 `C:\Users\<用户名>\.cursor\skills\<技能名>\`） |
| macOS / Linux | `~/.cursor/skills/<技能名>/` |

示例（将本仓库的某个技能链接到 Cursor 全局技能目录）：

```bash
mkdir -p ~/.cursor/skills
ln -s $(pwd)/skills/patent-writer-with-diagram ~/.cursor/skills/patent-writer-with-diagram
```

### 项目目录（仅当前仓库）

将技能子目录放在：

`<项目根>/.cursor/skills/<技能名>/`

### Cursor 兼容路径

为与 Claude Code 迁移一致，Cursor 也会扫描 **`~/.claude/skills/`**、项目内 **`.claude/skills/`** 等路径；详见 Cursor 官方文档与当前版本设置项。

## 各技能依赖

每个技能目录下可能有独立的 `requirements.txt` 和 `package.json`，详见各技能的 `INSTALL.md`。
