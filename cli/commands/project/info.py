from infrastructure.persistence.toml.reader import load_config


def run(args):
    data = load_config()

    print("=== Project Info ===")
    print(f"Name: {data['project']['name']}")
    print(f"Dependencies: {len(data.get('dependencies', {}))}")