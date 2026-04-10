from infrastructure.persistence.toml.reader import load_config
from infrastructure.persistence.toml.writer import save_config


def run(args):
    name = args.package

    data = load_config()

    if name not in data["dependencies"]:
        print("Dependency not found")
        return

    del data["dependencies"][name]

    save_config(data)

    print(f"✔ Removed {name}")