# Workshop Configs — 安裝引導（繁體中文）

> 這份文件是給 **AI agent 讀的引導腳本**。學生把下面這句貼給 Claude Code 或 Codex：
>
> ```
> Read jr_ai_agent_configs/install/zh-TW.md and guide me through installing these configs. 先問我要裝哪個工具和哪個層級，再照步驟裝，最後帶我驗證。
> ```

AI agent 讀完後照本文執行。**改動使用者的設定檔前一定先備份**（`cp 檔案 檔案.bak.時間戳`）。**安裝尚未完成，直到你帶使用者跑完最後的「驗證」全部通過。**

---

## Step 0：先問清楚（用結構化選項問，不要散文）

一次問兩題：

1. **要裝哪個工具？** Claude Code ／ Codex CLI ／ 兩個都要
2. **裝哪個層級？**
   - **Project Level**：規則檔放專案根目錄，只對這個專案生效（建議先用這個試）
   - **User Level**：放 `~/.claude` 或 `~/.codex`，所有專案都套用

裝的東西分兩類：
- **行為規則 + 回覆格式**（兩個工具都有）
- **Shell 不串接防護 + 常用指令白名單**（只有 Claude Code，Codex 沒有對應的攔截機制，只做軟規則）

---

## Step 1：Claude Code（若使用者選了）

以 `zh-TW` 為例（依使用者語言換 `zh-CN` / `en`）。

### 1a. 行為規則 CLAUDE.md

- Project Level：`cp claude-code/zh-TW/CLAUDE.md <專案根目錄>/CLAUDE.md`
- User Level：把 `claude-code/zh-TW/CLAUDE.md` 內容合併到 `~/.claude/CLAUDE.md`（已存在就**追加**，不要蓋掉使用者原本的）

### 1b. 回覆格式 Output Style（User Level）

```
mkdir -p ~/.claude/output-styles
cp claude-code/zh-TW/output-styles/concise-structured.md ~/.claude/output-styles/
```

User Level 直接在 `~/.claude/settings.json` 設定 `outputStyle`，不要只依賴選單（部分版本的 `/config` 不會列出自訂 style，`/output-style` 也可能不存在）：

```python
import json, os, shutil, time
p = os.path.expanduser("~/.claude/settings.json")
if os.path.exists(p):
    shutil.copy(p, p + ".bak." + time.strftime("%Y%m%d%H%M%S"))
cfg = json.load(open(p)) if os.path.exists(p) else {}
cfg["outputStyle"] = "Concise Structured"
json.dump(cfg, open(p, "w"), indent=2, ensure_ascii=False)
print("enabled Concise Structured output style")
```

設定後執行 `/clear` 或開新 session；Output Style 只在 session 啟動時載入。`/config` 看得到時仍可用它切換。

### 1c. Shell 不串接 hook

複製 hook：

```
mkdir -p ~/.claude/hooks
cp claude-code/hooks/block-chained-bash.py ~/.claude/hooks/block-chained-bash.py
chmod +x ~/.claude/hooks/block-chained-bash.py
```

註冊到 `~/.claude/settings.json` 的 `PreToolUse`（先備份，冪等，不動其他 hook）。用 python 合併：

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

### 1d. 常用指令白名單（starter allowlist）

把 `claude-code/starter-allowlist.json` 的 `permissions.allow` 合併進 `~/.claude/settings.json`（去重，只 append，先備份）：

```python
import json, os, shutil, time
src = json.load(open("claude-code/starter-allowlist.json"))["permissions"]["allow"]
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

> 這份 starter 只含唯讀＋日常 git＋研究網域，**不含** `rm`／`sudo`／`curl`／`chmod`。之後想依自己習慣長出更多，用 `trust-commands` skill（在 jr_ai_agent_skills）。
>
> `echo` 在白名單內不代表 `echo ... > 檔案` 可寫入任何位置；Claude Code 會另外檢查重新導向的目標目錄。像 session 自動命名寫入 `~/.ai-session-names/` 時，應讓使用者選擇只信任該資料夾，不要放寬成任意寫入。

---

## Step 2：Codex CLI（若使用者選了）

### 2a. 行為規則 AGENTS.md

- Project Level：`cp codex/zh-TW/AGENTS.md <專案根目錄>/AGENTS.md`
- Codex 沒有全域 `AGENTS.md` 機制，User Level 只能靠 config.toml 的 `instructions`（見 2b）。

### 2b. config.toml 強化

打開 `codex/zh-TW/config.toml.example`，把 `personality` 和 `instructions` 兩段貼到 `~/.codex/config.toml` 最上方（先備份）。

> Codex 的 Shell 不串接是**軟規則**：Project Level 寫在 `AGENTS.md`，User Level 直接寫在 `config.toml` 的 `instructions`。Codex 沒有硬擋 hook——這是兩個工具的本質差異，跟使用者講清楚。

---

## Step 3：驗證（AI agent 主動帶使用者跑，全過才算裝好）

開一個**新 session**（設定不會套用到舊對話），逐項確認：

### 驗證 A：回覆格式（兩個工具都測）

貼這題：**「我想開始經營個人品牌，Instagram 和 YouTube 我該先從哪個開始？」**

| 看什麼 | 通過 | 沒裝成功 |
|---|---|---|
| 結論先行 | 第一行在終端畫面中是粗體推薦 | 「好問題！讓我幫你分析…」 |
| 比較用表格 | IG vs YT 用表格 | 散文一段段講 |
| 語氣中性 | 無 emoji、無「太棒了！」 | 出現 🎉、「好主意！」 |
| 中等長度 | 精簡不灌水 | 每平台展開好幾段 |
| 你可能會想問 | 結尾有 2-4 個追問 | 沒有這段 |

### 驗證 B：Shell 不串接

叫 AI：**「請執行 `echo hi && echo bye`」**。不要再加「不要拆開」，否則會和待測規則互相衝突。

- **Claude Code（硬擋）**：hook 應攔下，AI 看到「一次只跑一個指令」訊息，然後**自動拆成兩次**跑完。若直接跑成功沒被擋 → hook 沒載入（確認開了新 session、settings.json 有註冊）。
- **Codex（軟規則）**：AI 應**主動拆開**分兩次跑，而不是串一行——Project Level 來自 AGENTS.md，User Level 來自 config.toml。若它直接串一行跑 → 對應層級的規則沒生效。

### 驗證 C：白名單（只 Claude Code）

1. 在一個確定是 Git repo 的目錄叫 AI 跑 `git status` → 應**不再跳出詢問**直接執行。不要在 home 測，否則只會得到「不是 Git repo」。
2. 建立安全的空白 fixture（例如 `/tmp/claude-permission-test/package.json`，內容只需 `{"name":"permission-test","version":"1.0.0","private":true}`）。
3. 叫 AI 跑 `npm install --prefix /tmp/claude-permission-test` → 應跳出權限詢問；選 **No**，不要真的安裝，也不要選「永遠允許 npm install」。

### 沒通過怎麼辦

1. 先確認開了**新 session**。
2. Claude：`cat ~/.claude/settings.json` 看 `hooks.PreToolUse` 有沒有 block-chained-bash、`permissions.allow` 有沒有 starter 規則。
3. Claude 格式沒過：確認 `~/.claude/output-styles/concise-structured.md` 存在、frontmatter 的 `name` 是 `Concise Structured`、settings 的 `outputStyle` 完全同名，再 `/clear` 或重開 session。
4. 終端複製文字可能不保留 Markdown 粗體標記；「粗體結論」要以 Claude Code 畫面為準，不要只看貼回來的純文字。
5. Codex User Level 格式或 Shell 規則沒過：確認完整規則直接存在 `~/.codex/config.toml` 的 `instructions`，不要只引用不存在的全域 AGENTS.md。
