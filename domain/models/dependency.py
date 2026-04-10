from dataclasses import dataclass
from domain.models.constraint import Constraint


@dataclass
class Dependency:
    name: str
    constraint: Constraint

    def __str__(self):
        return f"{self.name} ({self.constraint})"