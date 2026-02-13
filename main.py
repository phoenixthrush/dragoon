import json
import os
import textwrap

WIDTH = 80
PADDING = 2
CHOICES_FILE = "choices.json"


def clear():
    """Clear terminal"""
    print("\033[H\033[J", end="")


def center_lines(text, width=WIDTH):
    """Wrap and center text to width"""
    text = textwrap.dedent(text).strip("\n")
    raw_lines = text.splitlines()

    wrapped = []
    for ln in raw_lines:
        if not ln.strip():
            wrapped.append("")
            continue
        wrapped.extend(textwrap.wrap(ln, width=width) or [""])

    non_empty = [ln for ln in wrapped if ln.strip()]
    max_len = max((len(ln) for ln in non_empty), default=0)
    left_pad = max(0, (width - max_len) // 2)

    out = []
    for ln in wrapped:
        out.append("" if not ln.strip() else (" " * left_pad + ln))
    return out


def banner(text):
    """Show a banner screen"""
    clear()
    print("\n" * PADDING, end="")
    print("=" * WIDTH)
    print()
    for ln in center_lines(text):
        print(ln)
    print()
    print("=" * WIDTH)
    print("\n" * PADDING, end="")


def wait_key(prompt="(press Enter)"):
    """Wait for Enter"""
    input(prompt)


def load_choices(path=CHOICES_FILE):
    """Load choices dict"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}


def save_choice(key, value, path=CHOICES_FILE):
    """Persist a single choice"""
    data = load_choices(path)
    data[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ask_text(key, question, default=""):
    """Ask for free text"""
    banner(question)
    answer = input("> ").strip()
    if not answer and default:
        answer = default
    save_choice(key, answer)
    return answer


def ask_yes_no(key, question, default=False):
    """Ask a yes/no question"""
    hint = "Y/n" if default else "y/N"
    banner(f"{textwrap.dedent(question).strip()}\n\n[{hint}]")
    raw = input("> ").strip().lower()

    if raw in ("y", "yes"):
        val = True
    elif raw in ("n", "no"):
        val = False
    else:
        val = bool(default)

    save_choice(key, val)
    return val


def day_screen(day_number, day_title=""):
    """Show the current day screen"""
    title = f"Day {day_number:03d}"
    extra = f"\n{day_title}" if day_title else ""
    banner(f"{title}{extra}")
    wait_key()


def run_day_001():
    """Run day 1"""
    day_screen(1, "Prologue")

    banner("""
Clayn got stabbed to death and reincarnated as a hero to fight a dragon
that later became his new wife
""")
    wait_key()

    name = ask_text("name", "What is your name? (empty for Clayn)", default="Clayn")
    ask_yes_no("pregnancy", "Do you want pregnancy on?", default=False)

    banner(f"""
You wake up at home and notice that you are late for class, {name}.
""")
    wait_key()

    banner("""
You quickly get ready and dash out of the house, in the direction of your school.
""")
    wait_key()

    banner("""
On the way you have to cross the road.
""")
    wait_key()


def main():
    """Entry point"""
    run_day_001()


if __name__ == "__main__":
    main()
