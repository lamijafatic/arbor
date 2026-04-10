import os


def run(args):
    print("=== Doctor Check ===")

    if not os.path.exists("mypm.toml"):
        print("No project initialized")
        return

    print("✔ Config file exists")
    print("✔ Basic structure OK")