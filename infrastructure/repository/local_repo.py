import json
import os

from infrastructure.repository.abstract_repo import AbstractRepository


import os
import importlib.resources as ir


def _find_repo_json():
    # 1. Local project (dev mode)
    cwd_path = os.path.join(os.getcwd(), "data", "repository.json")
    if os.path.exists(cwd_path):
        return cwd_path

    # 2. Package-installed version
    try:
        return str(ir.files("data").joinpath("repository.json"))
    except Exception:
        pass

    raise FileNotFoundError(
        "Cannot find repository.json (neither local nor installed package)."
    )


class LocalRepository(AbstractRepository):
    def __init__(self):
        path = _find_repo_json()
        with open(path) as f:
            self.data = json.load(f)

    def get_versions(self, package_name: str) -> list:
        return list(self.data.get(package_name, {}).keys())

    def get_dependencies(self, package_name: str, version: str) -> list:
        return self.data.get(package_name, {}).get(version, [])

    def get_conflicts(self) -> list:
        return self.data.get("conflicts", [])

    def list_packages(self) -> list:
        return [k for k in self.data.keys() if k != "conflicts"]
