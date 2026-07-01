# jr_ai_agent_configs

AI Agent 回覆規則與 Output Style 設定檔，適用於 **Claude Code** 和 **Codex CLI**。

Workshop 教材用，讓 AI agent 的回覆風格一致：結論先行、表格比較、白話原則、中等長度。

## 檔案結構

```
├── claude-code/                          # Claude Code 專用
│   ├── zh-TW/
│   │   ├── CLAUDE.md                     # 行為規則
│   │   └── output-styles/
│   │       └── concise-structured.md     # 回覆格式
│   ├── zh-CN/
│   │   ├── CLAUDE.md
│   │   └── output-styles/
│   │       └── concise-structured.md
│   └── en/
│       ├── CLAUDE.md
│       └── output-styles/
│           └── concise-structured.md
│
├── codex/                                # Codex CLI 專用
│   ├── zh-TW/
│   │   ├── AGENTS.md                     # 行為規則 + 完整 Output Style
│   │   └── config.toml.example           # config 強化提醒
│   ├── zh-CN/
│   │   ├── AGENTS.md
│   │   └── config.toml.example
│   └── en/
│       ├── AGENTS.md
│       └── config.toml.example
```

## 兩個平台的差異

| | Claude Code | Codex CLI |
|---|---|---|
| **行為規則** | `CLAUDE.md` → 專案根目錄 | `AGENTS.md` → 專案根目錄 |
| **回覆格式** | `output-styles/concise-structured.md` → `~/.claude/output-styles/` | 已合併在 `AGENTS.md` 裡（Codex 沒有獨立的 output-style 機制） |
| **強化設定** | `/config` → Output style → Concise Structured | `~/.codex/config.toml` 加 `instructions` 一行 |

## 快速安裝

### Claude Code

```bash
# 選你的語言（zh-TW / zh-CN / en），以 zh-TW 為例

# 1. 行為規則 → 專案根目錄
cp claude-code/zh-TW/CLAUDE.md /path/to/your/project/CLAUDE.md

# 2. 回覆格式 → 全域 output-styles
mkdir -p ~/.claude/output-styles
cp claude-code/zh-TW/output-styles/concise-structured.md ~/.claude/output-styles/

# 3. 啟用：開新 session → /config → Output style → Concise Structured
```

### Codex CLI

```bash
# 選你的語言（zh-TW / zh-CN / en），以 zh-TW 為例

# 1. 行為規則（含完整 Output Style）→ 專案根目錄
cp codex/zh-TW/AGENTS.md /path/to/your/project/AGENTS.md

# 2. 強化設定 → 把 config.toml.example 裡的 instructions 那行
#    加到你的 ~/.codex/config.toml 最上方
cat codex/zh-TW/config.toml.example
# 然後手動把 instructions = "..." 那行貼進 ~/.codex/config.toml
```

## 客製化

這些是起點，你可以根據需求調整：

- **領域術語表** — 定義你的領域裡特定詞彙代表什麼
- **回覆語言** — 中文／英文／混用
- **深度偏好** — 調整長度描述讓回覆更詳細或更精簡
- **角色設定** — 教練、顧問、助手等

## 參考資源

- [Claude Code Best Practices (Official)](https://code.claude.com/docs/en/best-practices)
- [Output Styles Documentation (Official)](https://code.claude.com/docs/en/output-styles)
- [awesome-claude-md](https://github.com/josix/awesome-claude-md) — 精選 CLAUDE.md 範例集
- [claude-md-templates](https://github.com/abhishekray07/claude-md-templates) — 各技術棧模板

## License

MIT
