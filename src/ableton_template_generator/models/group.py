from dataclasses import dataclass
from typing import List
from .track import Track, ColorCode

@dataclass
class Group:
    name: str
    color: ColorCode
    tracks: List[Track]
    subgroups: List['Group'] = None