import json
import os
from domain.models.version import Version


class LocalRepository:
    def __init__(self, path="data/repository.json"):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        full_path = os.path.join(base_dir, path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Repository file not found: {full_path}")

        with open(full_path) as f:
            self.data = json.load(f)

    def get_versions(self, package_name):
        versions = self.data.get(package_name, {})
        return list(versions.keys())

    def get_dependencies(self, package_name, version):
        return self.data.get(package_name, {}).get(version, [])
    
    def get_conflicts(self):
        return self.data.get("conflicts", [])