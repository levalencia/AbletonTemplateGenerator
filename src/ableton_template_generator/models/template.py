from dataclasses import dataclass
from typing import List
from .group import Group
from .timeline import TimelineMarker

@dataclass
class Template:
    genre: str
    groups: List[Group]
    default_tempo: float
    default_duration_minutes: float
    timeline_markers: List[TimelineMarker]