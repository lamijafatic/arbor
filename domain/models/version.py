from dataclasses import dataclass


@dataclass(frozen=True)
class Version:
    raw: str
    def __post_init__(self):
        
        if isinstance(self.raw, Version):
            object.__setattr__(self, "raw", self.raw.raw)
    def to_tuple(self):
        return tuple(int(x) for x in self.raw.split("."))

    def __lt__(self, other: "Version"):
        return self.to_tuple() < other.to_tuple()

    def __le__(self, other: "Version"):
        return self.to_tuple() <= other.to_tuple()

    def __eq__(self, other: object):
        if not isinstance(other, Version):
            return False
        return self.raw == other.raw

    def __str__(self):
        return self.raw