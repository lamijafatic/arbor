import toml

CONFIG_FILE = "mypm.toml"


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        toml.dump(data, f)