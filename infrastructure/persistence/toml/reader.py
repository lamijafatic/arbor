import toml
import os

CONFIG_FILE = "mypm.toml"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise Exception("Project not initialized")

    return toml.load(CONFIG_FILE)