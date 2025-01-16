from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class TrackType(Enum):
    MIDI = "midi"
    AUDIO = "audio"
    BOTH = "both"

class ColorCode(Enum):
    BLUE = "#0000FF"     # Bass
    YELLOW = "#FFFF00"   # Percussion
    RED = "#FF0000"      # Lead
    GREEN = "#00FF00"    # Harmony
    PURPLE = "#800080"   # FX
    ORANGE = "#FFA500"   # Vocals

@dataclass
class Track:
    name: str
    type: TrackType
    color: ColorCode
    layers: int = 1