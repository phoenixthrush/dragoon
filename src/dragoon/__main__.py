from entities import Hero
from vn_engine import VNEngine

# =====================================
# Day 01 - Prologue
# =====================================


def run_day_001(vn: VNEngine):
    vn.day_screen(1, "Prologue")

    vn.banner("""
Clayn got stabbed to death and reincarnated as a hero
to fight a dragon that later became his new wife.
""")
    vn.wait()

    name = vn.ask_text("name", "What is your name? (empty for Clayn)", default="Clayn")
    hero = Hero(name)

    vn.ask_yes_no("pregnancy", "Do you want pregnancy on?", default=False)

    vn.bottom_text(f"""
You wake up at home and notice that you are late for class, {hero.name}.
""")
    vn.wait()

    vn.bottom_text("""
You quickly get ready and dash out of the house toward your school.
""")
    vn.wait()

    vn.bottom_text("""
On the way, you have to cross the road.
""")
    vn.wait()

    vn.end_day(2)


# =====================================
# Day 02 - A New Morning
# =====================================


def run_day_002(vn: VNEngine):
    vn.day_screen(2, "A New Morning")

    name = vn.get("name", "Clayn")

    vn.bottom_text(f"""
Good Morning, {name}.
""")
    vn.wait()

    vn.ask_multiple(
        "drink",
        "What do you want to drink?",
        ["Coffee", "Tea", "Water"],
        default="Coffee",
    )

    vn.end_day(3)


# =====================================
# Entry Point
# =====================================


def main():
    DAYS = {
        1: run_day_001,
        2: run_day_002,
    }

    vn = VNEngine()

    try:
        while True:
            current_day = vn.get_current_day()

            if current_day in DAYS:
                DAYS[current_day](vn)
            else:
                break

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
