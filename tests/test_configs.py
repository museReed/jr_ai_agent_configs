import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConfigTests(unittest.TestCase):
    def test_allowlist_is_unique(self):
        data = json.loads((ROOT / "claude-code/starter-allowlist.json").read_text())
        rules = data["permissions"]["allow"]
        self.assertEqual(len(rules), len(set(rules)))
        self.assertIn("Bash(git status:*)", rules)
        self.assertNotIn("Bash(npm install:*)", rules)

    def run_hook(self, command):
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
        return subprocess.run(
            ["python3", str(ROOT / "claude-code/hooks/block-chained-bash.py")],
            input=payload,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_hook_blocks_chaining(self):
        result = self.run_hook("echo hi && echo bye")
        self.assertEqual(result.returncode, 2)
        self.assertIn("一次只跑一個指令", result.stderr)

    def test_hook_allows_pipe_and_quoted_semicolon(self):
        self.assertEqual(self.run_hook("printf 'a;b' | head -1").returncode, 0)

    def test_user_level_codex_configs_are_self_contained(self):
        for locale in ("en", "zh-CN", "zh-TW"):
            text = (ROOT / f"codex/{locale}/config.toml.example").read_text()
            instruction = next(line for line in text.splitlines() if line.startswith("instructions = "))
            self.assertNotIn("AGENTS.md", instruction)
            self.assertIn("&&", instruction)
            self.assertIn("||", instruction)
            self.assertIn("2-4", instruction)


if __name__ == "__main__":
    unittest.main()
