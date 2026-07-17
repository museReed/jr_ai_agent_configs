# Workshop Configs — 安装引导（简体中文）

> 这份文件是给 **AI agent 读的引导脚本**。学生把下面这句贴给 Claude Code 或 Codex：
>
> ```
> Read jr_ai_agent_configs/install/zh-CN.md and guide me through installing these configs. 先问我要装哪个工具和哪个层级，再照步骤装，最后带我验证。
> ```

AI agent 读完后照本文执行。**改动使用者的设置文件前一定先备份**（`cp 文件 文件.bak.时间戳`）。**安装尚未完成，直到你带使用者跑完最后的「验证」全部通过。**

---

## Step 0：先问清楚（用结构化选项问，不要散文）

一次问两题：

1. **要装哪个工具？** Claude Code ／ Codex CLI ／ 两个都要
2. **装哪个层级？**
   - **Project Level**：规则文件放项目根目录，只对这个项目生效（建议先用这个试）
   - **User Level**：放 `~/.claude` 或 `~/.codex`，所有项目都套用

装的东西分两类：
- **行为规则 + 回复格式**（两个工具都有）
- **Shell 不串接防护 + 常用指令白名单**（只有 Claude Code，Codex 没有对应的拦截机制，只做软规则）

---

## Step 1：Claude Code（若使用者选了）

以 `zh-CN` 为例（依使用者语言换 `zh-TW` / `en`）。

### 1a. 行为规则 CLAUDE.md

- Project Level：`cp claude-code/zh-CN/CLAUDE.md <项目根目录>/CLAUDE.md`
- User Level：把 `claude-code/zh-CN/CLAUDE.md` 内容合并到 `~/.claude/CLAUDE.md`（已存在就**追加**，不要盖掉使用者原本的）

### 1b. 回复格式 Output Style（User Level）

```
mkdir -p ~/.claude/output-styles
cp claude-code/zh-CN/output-styles/concise-structured.md ~/.claude/output-styles/
```

启用：开新 session → `/config` → Output style → Concise Structured。

### 1c. Shell 不串接 hook

复制 hook：

```
mkdir -p ~/.claude/hooks
cp claude-code/hooks/block-chained-bash.py ~/.claude/hooks/block-chained-bash.py
chmod +x ~/.claude/hooks/block-chained-bash.py
```

注册到 `~/.claude/settings.json` 的 `PreToolUse`（先备份，幂等，不动其他 hook）。用 python 合并：

```python
import json, os, shutil, time
p = os.path.expanduser("~/.claude/settings.json")
if os.path.exists(p):
    shutil.copy(p, p + ".bak." + time.strftime("%Y%m%d%H%M%S"))
cfg = json.load(open(p)) if os.path.exists(p) else {}
pre = cfg.setdefault("hooks", {}).setdefault("PreToolUse", [])
marker = "block-chained-bash.py"
cmd = f'python3 {os.path.expanduser("~/.claude/hooks/block-chained-bash.py")}'
for g in pre:
    g["hooks"] = [h for h in g.get("hooks", []) if marker not in h.get("command", "")]
pre[:] = [g for g in pre if g.get("hooks")]
pre.append({"matcher": "Bash", "hooks": [{"type": "command", "command": cmd, "timeout": 5}]})
json.dump(cfg, open(p, "w"), indent=2, ensure_ascii=False)
print("registered block-chained-bash PreToolUse hook")
```

### 1d. 常用指令白名单（starter allowlist）

把 `claude-code/starter-allowlist.json` 的 `permissions.allow` 合并进 `~/.claude/settings.json`（去重，只 append，先备份）：

```python
import json, os, shutil, time
src = json.load(open("claude-code/starter-allowlist.json"))["permissions"]["allow"]
# per-machine：Bash() 白名单不吃 ~/$HOME，安装时展开成这台机器的绝对路径
home = os.path.expanduser("~")
src = [r.replace("Bash(~/", f"Bash({home}/") for r in src]
p = os.path.expanduser("~/.claude/settings.json")
if os.path.exists(p):
    shutil.copy(p, p + ".bak." + time.strftime("%Y%m%d%H%M%S"))
cfg = json.load(open(p)) if os.path.exists(p) else {}
allow = cfg.setdefault("permissions", {}).setdefault("allow", [])
added = [r for r in src if r not in allow]
allow.extend(added)
json.dump(cfg, open(p, "w"), indent=2, ensure_ascii=False)
print(f"added {len(added)} allowlist rules")
```

> 这份 starter 只含只读＋日常 git＋研究网域，**不含** `rm`／`sudo`／`curl`／`chmod`。之后想依自己习惯长出更多，用 `trust-commands` skill（在 jr_ai_agent_skills）。

---

## Step 2：Codex CLI（若使用者选了）

### 2a. 行为规则 AGENTS.md

- Project Level：`cp codex/zh-CN/AGENTS.md <项目根目录>/AGENTS.md`
- Codex 没有全局 `AGENTS.md` 机制，User Level 只能靠 config.toml 的 `instructions`（见 2b）。

### 2b. config.toml 强化

打开 `codex/zh-CN/config.toml.example`，把 `personality` 和 `instructions` 两段贴到 `~/.codex/config.toml` 最上方（先备份）。

> Codex 的 Shell 不串接是**软规则**（写在 AGENTS.md），没有硬挡 hook——这是两个工具的本质差异，跟使用者讲清楚。

---

## Step 3：验证（AI agent 主动带使用者跑，全过才算装好）

开一个**新 session**（设置不会套用到旧对话），逐项确认：

### 验证 A：回复格式（两个工具都测）

贴这题：**「我想开始经营个人品牌，Instagram 和 YouTube 我该先从哪个开始？」**

| 看什么 | 通过 | 没装成功 |
|---|---|---|
| 结论先行 | 第一行就是粗体推荐 | 「好问题！让我帮你分析…」 |
| 比较用表格 | IG vs YT 用表格 | 散文一段段讲 |
| 语气中性 | 无 emoji、无「太棒了！」 | 出现 🎉、「好主意！」 |
| 中等长度 | 精简不灌水 | 每平台展开好几段 |
| 你可能会想问 | 结尾有 2-4 个追问 | 没有这段 |

### 验证 B：Shell 不串接

叫 AI：**「用一个指令跑 `echo hi && echo bye`」**

- **Claude Code（硬挡）**：hook 应拦下，AI 看到「一次只跑一个指令」讯息，然后**自动拆成两次**跑完。若直接跑成功没被挡 → hook 没载入（确认开了新 session、settings.json 有注册）。
- **Codex（软规则）**：AI 应**主动拆开**分两次跑，而不是串一行——因为 AGENTS.md 规则。若它直接串一行跑 → AGENTS.md 没生效。

### 验证 C：白名单（只 Claude Code）

叫 AI 跑一个白名单内的指令（如 `git status`）→ 应**不再跳出询问**直接执行。跑一个不在白名单的（如 `npm install`）→ 应该还是会问。

### 没通过怎么办

1. 先确认开了**新 session**。
2. Claude：`cat ~/.claude/settings.json` 看 `hooks.PreToolUse` 有没有 block-chained-bash、`permissions.allow` 有没有 starter 规则。
3. 行为/格式没过：确认 CLAUDE.md／AGENTS.md 在对的层级、output style 有选到 Concise Structured。
