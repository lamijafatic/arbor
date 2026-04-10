import os
from infrastructure.persistence.toml.writer import save_config


def run(args):
    if os.path.exists("mypm.toml"):
        print("Project already initialized.")
        return

    data = {
        "project": {
            "name": "my_project"
        },
        "dependencies": {}
    }

    save_config(data)

    print("Project initialized.")