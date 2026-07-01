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
│   ├── zh-CN/ ...
│   └── en/ ...
│
├── codex/                                # Codex CLI 專用
│   ├── zh-TW/
│   │   ├── AGENTS.md                     # 行為規則 + 完整 Output Style
│   │   └── config.toml.example           # config 強化設定
│   ├── zh-CN/ ...
│   └── en/ ...
```

## 兩個平台的差異

| | Claude Code | Codex CLI |
|---|---|---|
| **行為規則** | `CLAUDE.md` → 專案根目錄 | `AGENTS.md` → 專案根目錄 |
| **回覆格式** | `output-styles/concise-structured.md` → `~/.claude/output-styles/` | 已合併在 `AGENTS.md` 裡（Codex 沒有獨立的 output-style 機制） |
| **強化設定** | `/config` → Output style → Concise Structured | `~/.codex/config.toml` 加 `personality` + `instructions` |

---

## 安裝前先決定：User Level 還是 Project Level？

設定檔可以放在兩個層級，效果不同：

| 層級 | 放哪裡 | 生效範圍 | 適合什麼情境 |
|---|---|---|---|
| **User Level（全域）** | `~/.claude/` 或 `~/.codex/` | 你電腦上**所有專案**都會套用 | 你希望不管開哪個專案，AI 都用同一套規則回覆 |
| **Project Level（專案）** | 專案根目錄（和 `package.json`、`.git` 同一層） | **只有這個專案**會套用 | 你只想在特定專案裡用，或不同專案想用不同規則 |

### 怎麼選？

- **剛開始用** → 建議先放 **Project Level**，在一個專案裡試看看效果，滿意再推到全域
- **確定喜歡這套規則** → 搬到 **User Level**，所有專案都自動套用

下面的安裝指令會標示每個檔案屬於哪個層級。

---

## 快速安裝

### Claude Code

```bash
# 選你的語言（zh-TW / zh-CN / en），以 zh-TW 為例

# ── Project Level ──
# 行為規則 → 專案根目錄（只對這個專案生效）
cp claude-code/zh-TW/CLAUDE.md /path/to/your/project/CLAUDE.md

# ── User Level ──
# 回覆格式 → 全域 output-styles（所有專案都生效）
mkdir -p ~/.claude/output-styles
cp claude-code/zh-TW/output-styles/concise-structured.md ~/.claude/output-styles/

# 啟用：開新 session → /config → Output style → Concise Structured
```

> **想全域套用行為規則？** 把 `CLAUDE.md` 改放到 `~/.claude/CLAUDE.md`，就不用每個專案都複製一份。

### Codex CLI

```bash
# 選你的語言（zh-TW / zh-CN / en），以 zh-TW 為例

# ── Project Level ──
# 行為規則（含完整 Output Style）→ 專案根目錄（只對這個專案生效）
cp codex/zh-TW/AGENTS.md /path/to/your/project/AGENTS.md

# ── User Level ──
# 強化設定 → 全域 config（所有專案都生效）
# 打開 config.toml.example 看內容，把 personality 和 instructions 兩行
# 貼到你的 ~/.codex/config.toml 最上方
cat codex/zh-TW/config.toml.example
```

> **想全域套用行為規則？** 目前 Codex 沒有全域 `AGENTS.md` 機制，只能靠 `config.toml` 的 `instructions` 做全域提醒，詳細規則仍需每個專案放一份 `AGENTS.md`。

---

## 驗證安裝是否成功

安裝完後開一個新 session，貼上這個問題：

> **「我想開始經營個人品牌，Instagram 和 YouTube 我該先從哪個開始？」**

對照以下 checklist 確認 AI 有遵守規則：

| 驗證項目 | 看什麼 | 沒裝成功的樣子 |
|---|---|---|
| **結論先行** | 第一行就是粗體推薦結論 | 「好問題！讓我幫你分析一下...」 |
| **比較用表格** | IG vs YT 用表格呈現優缺點 | 用散文一段一段講 |
| **語氣中性** | 沒有 emoji、沒有「太棒了！」 | 出現 🎉、「好主意！」 |
| **中等長度** | 回覆精簡，不灌水 | 每個平台展開成好幾段 |
| **你可能會想問** | 結尾有 2-4 個追問建議 | 沒有這個段落 |

5 項都通過 = 安裝成功。如果部分沒通過，先確認有開**新 session**（設定不會套用到舊的對話）。

---

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
