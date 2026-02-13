import json
import os
import shutil
import textwrap
from pathlib import Path


class VNEngine:
    def __init__(self, width=100, padding=2, save_file="save_data.json"):
        """Initialize the vn engine with terminal width, padding, and save file"""
        self.width = width  # max width of text
        self.padding = padding  # blank lines around content
        self.save_path = Path(save_file)  # where progress will be saved
        self.state = self._load()  # load saved state or start empty

    # ==============================
    # Core Utilities
    # ==============================

    def clear(self):
        """Clear the terminal screen"""
        os.system("cls" if os.name == "nt" else "clear")

    def wait(self):
        """Pause and wait for user to press enter"""
        input()

    def _terminal_height(self):
        """Get the current terminal height in lines"""
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
                wrapped_lines.append("")  # preserve empty lines
                continue

            wrapped_lines.extend(textwrap.wrap(raw_line, self.width) or [""])

        # figure out left padding to center non-empty lines
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
        """Display big banner with text surrounded by lines"""
        self.clear()

        print("\n" * self.padding, end="")
        print("=" * self.width)
        print()

        for line in self._wrap_center(text):
            print(line)

        print()
        print("=" * self.width)
        print("\n" * self.padding, end="")

    def bottom_text(self, text, speaker=None):
        """Show text at bottom, optionally with a speaker name"""
        self.clear()

        if speaker:
            text = f"{speaker}: {text}"

        lines = self._wrap_center(text)
        blank = max(0, self._terminal_height() - len(lines) - self.padding)
        print("\n" * blank, end="")
        for line in lines:
            print(line)

    # ==============================
    # Persistence
    # ==============================

    def _load(self):
        """Load saved state from json or return empty dict"""
        if not self.save_path.exists():
            return {}
        try:
            return json.loads(self.save_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def _save(self):
        """Save current state to json"""
        self.save_path.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def set_value(self, key, value):
        """Save a value in state and persist"""
        self.state[key] = value
        self._save()

    def get_value(self, key, default=None):
        """Get a value from state or return default"""
        return self.state.get(key, default)

    # ==============================
    # Input Helpers
    # ==============================

    def ask_text(self, key, question, default=""):
        """Ask the player to type text and save it"""
        self.banner(question)

        answer = input("> ").strip() or default
        self.set_value(key, answer)

        return answer

    def ask_yes_no(self, key, question, default=False):
        """Ask the player a yes/no question and save result"""
        hint = "Y/n" if default else "y/N"
        self.banner(f"{question}\n[{hint}]")

        raw = input("> ").strip().lower()

        if raw in ("y", "yes"):
            value = True
        elif raw in ("n", "no"):
            value = False
        else:
            value = default

        self.set_value(key, value)
        return value

    def ask_multiple(self, key, question, options, multiple=False, default=None):
        """
        Ask the player to choose one or more options and save result

        Parameters:
        - key: state key to save
        - question: prompt text
        - options: list of strings
        - multiple: if True, allow multiple selections
        - default: default selection(s) if input is empty
        """

        self.banner(question)

        # show each option numbered
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        print()

        while True:
            prompt = "> " if not multiple else "(comma-separated numbers) > "
            raw = input(prompt).strip()

            if not raw and default is not None:
                selection = default
            else:
                try:
                    if multiple:
                        # allow comma-separated numbers
                        indices = [int(x) for x in raw.split(",")]

                        if any(i < 1 or i > len(options) for i in indices):
                            raise ValueError

                        selection = [options[i - 1] for i in indices]
                    else:
                        idx = int(raw)

                        if idx < 1 or idx > len(options):
                            raise ValueError

                        selection = options[idx - 1]
                except ValueError:
                    print("Invalid input. Please enter valid number(s).")
                    continue

            self.set_value(key, selection)
            return selection

    # ==============================
    # Story Helpers
    # ==============================

    def day_screen(self, number, title=""):
        """Show day number and optional title in a banner"""
        label = f"Day {number:03d}"

        if title:
            label += f"\n{title}"

        self.banner(label)
        self.wait()

    # ==============================
    # Day Management
    # ==============================

    def get_current_day(self):
        """Return the current day from state or 1"""
        return self.get_value("current_day", 1)

    def set_current_day(self, day: int):
        """Update the current day in state"""
        self.set_value("current_day", day)

    def end_day(self, next_day: int):
        """Save progress and move to next day"""
        self.set_current_day(next_day)
        self._save()
