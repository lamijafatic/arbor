import re
from domain.models.version import Version


class Constraint:
    def __init__(self, raw: str):
        self.raw = raw
        self.conditions = self.parse(raw)

    def parse(self, raw):
        if not raw:
            return []

        parts = raw.split(",")  # 🔥 KLJUČNO
        conditions = []

        for part in parts:
            part = part.strip()

            match = re.match(r"(>=|<=|>|<|==)?\s*([\d\.]+)", part)
            if not match:
                raise ValueError(f"Invalid constraint: {part}")

            op, version = match.groups()
            op = op or "=="

            conditions.append((op, Version(version)))

        return conditions

    def is_satisfied_by(self, version: Version) -> bool:
        for op, v in self.conditions:
            if op == "==" and not (version == v):
                return False
            elif op == ">=" and not (version >= v):
                return False
            elif op == "<=" and not (version <= v):
                return False
            elif op == ">" and not (version > v):
                return False
            elif op == "<" and not (version < v):
                return False

        return True

    def __str__(self):
        return self.raw