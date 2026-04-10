from infrastructure.persistence.toml.reader import load_config
from infrastructure.persistence.toml.writer import save_config


def run(args):
    name = args.package
    constraint = args.constraint

    data = load_config()

    data["dependencies"][name] = constraint

    save_config(data)

    print(f"✔ Added {name} ({constraint})")