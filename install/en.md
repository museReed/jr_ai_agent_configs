# Workshop Configs — Install Guide (English)

> This document is a **guide script for the AI agent to read**. The student pastes the following line to Claude Code or Codex:
>
> ```
> Read jr_ai_agent_configs/install/en.md and guide me through installing these configs. First ask me which tool and which level I want, then install step by step, and finally walk me through verification.
> ```

After reading, the AI agent follows this document. **Always back up the user's config files before changing them** (`cp file file.bak.timestamp`). **The install is not done until you've walked the user through the final "Verification" and everything passes.**

---

## Step 0: Ask first (use structured options, not prose)

Ask two questions at once:

1. **Which tool?** Claude Code / Codex CLI / both
2. **Which level?**
   - **Project Level**: the rules file goes in the project root and applies only to this project (recommended to try first)
   - **User Level**: goes in `~/.claude` or `~/.codex` and applies to all projects

What gets installed falls into two categories:
- **Behavior rules + response format** (both tools have this)
- **Shell no-chaining guard + common-command allowlist** (Claude Code only; Codex has no matching interception mechanism, only a soft rule)

---

## Step 1: Claude Code (if the user chose it)

Using `en` as the example (swap in `zh-TW` / `zh-CN` per the user's language).

### 1a. Behavior rules CLAUDE.md

- Project Level: `cp claude-code/en/CLAUDE.md <project-root>/CLAUDE.md`
- User Level: merge the contents of `claude-code/en/CLAUDE.md` into `~/.claude/CLAUDE.md` (if it already exists, **append** — don't overwrite the user's existing file)

### 1b. Response format Output Style (User Level)

```
mkdir -p ~/.claude/output-styles
cp claude-code/en/output-styles/concise-structured.md ~/.claude/output-styles/
```

Enable: open a new session → `/config` → Output style → Concise Structured.

### 1c. Shell no-chaining hook

Copy the hook:

```
mkdir -p ~/.claude/hooks
cp claude-code/hooks/block-chained-bash.py ~/.claude/hooks/block-chained-bash.py
chmod +x ~/.claude/hooks/block-chained-bash.py
```

Register it to `PreToolUse` in `~/.claude/settings.json` (back up first, idempotent, leaves other hooks untouched). Merge with python:

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

### 1d. Common-command allowlist (starter allowlist)

Merge the `permissions.allow` from `claude-code/starter-allowlist.json` into `~/.claude/settings.json` (dedupe, append only, back up first):

```python
import json, os, shutil, time
src = json.load(open("claude-code/starter-allowlist.json"))["permissions"]["allow"]
# per-machine: Bash() allow rules don't expand ~/$HOME, so resolve to this machine's absolute path at install time
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

> This starter contains only read-only + everyday git + research domains, and **excludes** `rm` / `sudo` / `curl` / `chmod`. When you later want to grow it to fit your own habits, use the `trust-commands` skill (in jr_ai_agent_skills).

---

## Step 2: Codex CLI (if the user chose it)

### 2a. Behavior rules AGENTS.md

- Project Level: `cp codex/en/AGENTS.md <project-root>/AGENTS.md`
- Codex has no global `AGENTS.md` mechanism; at the User Level you can only rely on config.toml's `instructions` (see 2b).

### 2b. config.toml reinforcement

Open `codex/en/config.toml.example` and paste the `personality` and `instructions` sections to the top of `~/.codex/config.toml` (back up first).

> Codex's shell no-chaining is a **soft rule** (written in AGENTS.md), with no hard-blocking hook — this is a fundamental difference between the two tools, so make it clear to the user.

---

## Step 3: Verification (the AI agent proactively walks the user through it; only counts as installed when everything passes)

Open a **new session** (settings don't apply to old conversations) and confirm each item:

### Verification A: Response format (test on both tools)

Paste this question: **"I want to start building a personal brand — should I start with Instagram or YouTube first?"**

| What to check | Pass | Not installed |
|---|---|---|
| Conclusion first | The first line is a bold recommendation | "Great question! Let me analyze it for you…" |
| Comparison uses a table | IG vs YT in a table | Prose, paragraph by paragraph |
| Neutral tone | No emoji, no "Awesome!" | 🎉 appears, "Great idea!" |
| Medium length | Concise, no filler | Several paragraphs per platform |
| You might want to ask | 2-4 follow-ups at the end | This section is missing |

### Verification B: Shell no-chaining

Tell the AI: **"Run `echo hi && echo bye` in one command"**

- **Claude Code (hard block)**: the hook should block it, the AI sees the "run one command at a time" message, then **automatically splits it into two** runs. If it runs successfully without being blocked → the hook didn't load (confirm you opened a new session and that settings.json has the registration).
- **Codex (soft rule)**: the AI should **split it up on its own** and run twice, rather than chaining one line — because of the AGENTS.md rule. If it chains one line directly → AGENTS.md didn't take effect.

### Verification C: Allowlist (Claude Code only)

Have the AI run a command in the allowlist (like `git status`) → it should **no longer prompt** and just execute. Run one not in the allowlist (like `npm install`) → it should still prompt.

### What if it doesn't pass

1. First confirm you opened a **new session**.
2. Claude: `cat ~/.claude/settings.json` and check whether `hooks.PreToolUse` has block-chained-bash and whether `permissions.allow` has the starter rules.
3. Behavior/format didn't pass: confirm CLAUDE.md / AGENTS.md is at the right level and that the output style is set to Concise Structured.
