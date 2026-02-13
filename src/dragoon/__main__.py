from entities import Hero
from vn_engine import VNEngine

# =====================================
# Story Implementation
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


# =====================================
# Entry Point
# =====================================


def main():
    vn = VNEngine()

    try:
        run_day_001(vn)
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
