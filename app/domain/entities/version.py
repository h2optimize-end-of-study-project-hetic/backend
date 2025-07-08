from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Version:
    name: str
    version: str

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)