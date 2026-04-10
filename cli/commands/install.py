from infrastructure.persistence.toml.reader import load_config


def run(args):
    data = load_config()
    deps = data.get("dependencies", {})

    print("=== Installing Packages ===")

    for name, constraint in deps.items():
        print(f"Installing {name} ({constraint})")

    print("✔ Install complete (mock)")