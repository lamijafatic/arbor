from infrastructure.persistence.toml.reader import load_config


def run(args):
    data = load_config()
    deps = data.get("dependencies", {})

    print("=== Dependencies ===")

    if not deps:
        print("No dependencies")
        return

    for name, constraint in deps.items():
        print(f"{name} -> {constraint}")