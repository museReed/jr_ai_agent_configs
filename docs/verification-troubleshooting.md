# 安裝驗證與常見問題

這份清單整理實際安裝 Claude Code 2.1.211 與 Codex CLI 時容易誤判的地方。驗證必須使用新 session；Output Style 與全域 instructions 都在 session 啟動時載入。

| 現象 | 原因 | 修正方式 |
|---|---|---|
| Claude Code 的 `/config` 沒列出自訂 Output Style | 部分版本的 picker 不顯示已存在的自訂 style | 確認檔案在 `~/.claude/output-styles/`，並直接在 `~/.claude/settings.json` 設定 `"outputStyle": "Concise Structured"` |
| `/output-style` 顯示 Unknown command | 新版可能沒有這個 slash command，會把參數當成 unknown skill | 不依賴此指令；改用 `outputStyle` 設定，然後 `/clear` 或重開 session |
| Style 檔案正確，但第一輪格式不穩定 | 設定可能尚未重新載入，或單次模型輸出沒有完全遵守 | 先 `/clear` 或重開；逐項檢查，不用單一特徵判斷 |
| 貼回來的第一行看不出粗體 | 終端複製常會移除 Markdown 標記 | 以 Claude Code / Codex 畫面中的實際渲染為準 |
| Hook 擋下 `&&` 後 AI 沒自動拆開 | 測試 prompt 若寫「不要拆開」，會和規則衝突 | 只說「請執行 `echo hi && echo bye`」；Claude 應在被擋後拆開，Codex 應事前拆開 |
| `echo` 已在白名單，重新導向仍詢問 | `echo ... > path` 還包含對目標目錄的寫入 | 只信任必要目錄，例如 `~/.ai-session-names/`，不要放寬任意寫入 |
| `git status` 測試只得到 not a git repository | 測試是在 home，而不是 Git repo | 在確定有 `.git` 的專案目錄測試；重點是是否先詢問權限 |
| AI 拒絕測 `npm install` | 當前目錄沒有 `package.json`，AI 在工具呼叫前合理地停止 | 建立空白 `/tmp/claude-permission-test/package.json`，測 `npm install --prefix /tmp/claude-permission-test`，看到詢問後選 No |
| Codex 有表格但沒有「你可能會想問」 | User Level 的 `instructions` 只引用 AGENTS.md，但 Codex 沒有全域 AGENTS.md | 把完整輸出規則直接寫入 `~/.codex/config.toml` 的 `instructions` |
| Codex 沒主動拆 Shell 指令 | User Level config 沒包含 Shell 軟規則 | 在 `instructions` 明寫禁止 `&&`、`||`、`;`，多步拆成多次工具呼叫 |

## 建議驗證流程

1. **回覆格式**：測結論、表格、中性語氣、中等長度與預期追問；粗體以終端畫面判定。
2. **Shell 不串接**：要求執行 `echo hi && echo bye`，不要額外要求「不准拆開」。
3. **Claude allowlist**：在真實 Git repo 測 `git status`；用空白 `/tmp` fixture 測 `npm install` 仍會詢問，並選 No。
4. **寫入目錄權限**：若 session 命名功能詢問，只允許專用資料夾，不新增廣泛的 Bash 或寫入規則。
