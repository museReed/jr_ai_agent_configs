# jr_ai_agent_configs

AI Agent 回覆規則與 Output Style 設定檔，適用於 **Claude Code** 和 **Codex CLI**。

Workshop 教材用，讓 AI agent 的回覆風格一致：結論先行、表格比較、白話原則、中等長度。

## 檔案結構

```
├── zh-TW/                        # 繁體中文
│   ├── CLAUDE.md                  # 行為規則（貼進專案根目錄）
│   └── output-styles/
│       └── concise-structured.md  # 回覆格式（複製到 ~/.claude/output-styles/）
├── zh-CN/                        # 简体中文
│   ├── CLAUDE.md
│   └── output-styles/
│       └── concise-structured.md
└── en/                           # English
    ├── CLAUDE.md
    └── output-styles/
        └── concise-structured.md
```

## 快速安裝

### Claude Code

```bash
# 1. 複製行為規則到專案根目錄（選你的語言）
cp zh-TW/CLAUDE.md /path/to/your/project/CLAUDE.md

# 2. 複製 output style（全域生效）
cp zh-TW/output-styles/concise-structured.md ~/.claude/output-styles/

# 3. 啟用：開新 session → /config → Output style → Concise Structured
```

### Codex CLI

```bash
# 1. 複製行為規則到專案根目錄（Codex 讀 AGENTS.md）
cp zh-TW/CLAUDE.md /path/to/your/project/AGENTS.md

# 2. 在 ~/.codex/config.toml 加強化提醒
#    在檔案頂部加一行：
#    instructions = "嚴格遵守 AGENTS.md 規則"
```

## 兩個檔案的分工

| 檔案 | 控制什麼 | 放哪裡 |
|---|---|---|
| `CLAUDE.md` / `AGENTS.md` | 行為規則：不假設、主動推回、簡單性、計畫先行、output style 摘要 | 專案根目錄 |
| `output-styles/concise-structured.md` | 詳細回覆格式：骨架、長度、結構、語氣、白話原則、預期追問、決策提問 | `~/.claude/output-styles/`（Claude Code 專用） |

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
