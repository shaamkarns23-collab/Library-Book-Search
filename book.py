from dataclasses import dataclass, asdict
@dataclass
class Book:
    isbn: str
    title: str
    author: str
    category: str
    year: int
    rating: float = 0.0
    total_copies: int = 1
    available_copies: int = 1
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, d): return cls(**d)
