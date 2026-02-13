import json
import os
import shutil
import textwrap
from pathlib import Path


class VNEngine:
    def __init__(self, width=100, padding=2, save_file="save.json"):
        self.width = width
        self.padding = padding
        self.save_path = Path(save_file)
        self.state = self._load()

    # ==============================
    # Core Utilities
    # ==============================

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def wait(self):
        input()

    def _terminal_height(self):
        return shutil.get_terminal_size().lines

    # ==============================
    # Text Formatting
    # ==============================

    def _wrap_center(self, text: str) -> list[str]:
        """Wrap text to width and center it horizontally"""
        cleaned = textwrap.dedent(text).strip()
        wrapped_lines: list[str] = []

        for raw_line in cleaned.splitlines():
            if not raw_line.strip():
                wrapped_lines.append("")
                continue

            wrapped_lines.extend(textwrap.wrap(raw_line, self.width) or [""])

        non_empty_lines = [line for line in wrapped_lines if line.strip()]
        longest_line = max((len(line) for line in non_empty_lines), default=0)
        left_padding = max(0, (self.width - longest_line) // 2)

        return [
            "" if not line.strip() else (" " * left_padding + line)
            for line in wrapped_lines
        ]

    # ==============================
    # Rendering
    # ==============================

    def banner(self, text):
        self.clear()
        print("\n" * self.padding, end="")
        print("=" * self.width)
        print()
        for line in self._wrap_center(text):
            print(line)
        print()
        print("=" * self.width)
        print("\n" * self.padding, end="")

    def bottom_text(self, text):
        self.clear()
        lines = self._wrap_center(text)
        blank = max(0, self._terminal_height() - len(lines) - self.padding)
        print("\n" * blank, end="")
        for line in lines:
            print(line)

    # ==============================
    # Persistence
    # ==============================

    def _load(self):
        if not self.save_path.exists():
            return {}
        try:
            return json.loads(self.save_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def _save(self):
        self.save_path.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def set(self, key, value):
        self.state[key] = value
        self._save()

    def get(self, key, default=None):
        return self.state.get(key, default)

    # ==============================
    # Input Helpers
    # ==============================

    def ask_text(self, key, question, default=""):
        self.banner(question)
        answer = input("> ").strip() or default
        self.set(key, answer)
        return answer

    def ask_yes_no(self, key, question, default=False):
        hint = "Y/n" if default else "y/N"
        self.banner(f"{question}\n[{hint}]")

        raw = input("> ").strip().lower()

        if raw in ("y", "yes"):
            value = True
        elif raw in ("n", "no"):
            value = False
        else:
            value = default

        self.set(key, value)
        return value

    # ==============================
    # Story Helpers
    # ==============================

    def day_screen(self, number, title=""):
        label = f"Day {number:03d}"
        if title:
            label += f"\n{title}"
        self.banner(label)
        self.wait()

    # ==============================
    # Day Management
    # ==============================

    def get_current_day(self):
        return self.get("current_day", 1)

    def set_current_day(self, day: int):
        self.set("current_day", day)

    def end_day(self, next_day: int):
        """Save progress and prepare next day"""
        self.set_current_day(next_day)
        self._save()
