from dataclasses import dataclass
from domain.models.version import Version


@dataclass(frozen=True)
class Package:
    name: str
    version: Version

    def __str__(self):
        return f"{self.name}-{self.version}"