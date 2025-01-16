# src/ableton_template_generator/models/timeline.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import math

class MarkerType(Enum):
    SECTION_START = "section_start"
    SECTION_END = "section_end"
    CUE_POINT = "cue_point"
    LOOP_POINT = "loop_point"
    ARRANGEMENT = "arrangement"
    TEMPO_CHANGE = "tempo_change"
    TIME_SIGNATURE_CHANGE = "time_signature_change"
    KEY_CHANGE = "key_change"

class TimeSignature:
    def __init__(self, numerator: int = 4, denominator: int = 4):
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def beats_per_bar(self) -> float:
        return float(self.numerator)

    def beat_value(self) -> float:
        return 4.0 / float(self.denominator)

@dataclass
class TimelineMarker:
    name: str
    position_bars: int
    duration_bars: int
    description: str
    marker_type: MarkerType = MarkerType.SECTION_START
    color: Optional[str] = None
    time_signature: TimeSignature = TimeSignature()
    tempo: Optional[float] = None
    key: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @property
    def end_position_bars(self) -> int:
        """Get the end position of the marker in bars"""
        return self.position_bars + self.duration_bars

    def get_position_time(self, tempo: float) -> float:
        """Convert bar position to time in seconds at given tempo"""
        beats_per_second = tempo / 60.0
        beats = self.position_bars * self.time_signature.beats_per_bar()
        return beats / beats_per_second

    def get_duration_time(self, tempo: float) -> float:
        """Convert duration in bars to time in seconds at given tempo"""
        beats_per_second = tempo / 60.0
        beats = self.duration_bars * self.time_signature.beats_per_bar()
        return beats / beats_per_second

    def overlaps_with(self, other: 'TimelineMarker') -> bool:
        """Check if this marker overlaps with another marker"""
        return (
            self.position_bars < other.end_position_bars and
            other.position_bars < self.end_position_bars
        )

@dataclass
class TimelineSection:
    """Represents a section in the timeline (e.g., Intro, Verse, Chorus)"""
    name: str
    start_bar: int
    length_bars: int
    section_type: str
    energy_level: float = 1.0  # 0.0 to 1.0
    intensity: float = 1.0     # 0.0 to 1.0
    markers: List[TimelineMarker] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.markers is None:
            self.markers = []
        if self.metadata is None:
            self.metadata = {}

    @property
    def end_bar(self) -> int:
        return self.start_bar + self.length_bars

class Timeline:
    def __init__(self):
        self.markers: List[TimelineMarker] = []
        self.sections: List[TimelineSection] = []
        self.default_tempo: float = 120.0
        self.default_time_signature: TimeSignature = TimeSignature()

    def add_marker(self, marker: TimelineMarker) -> None:
        """Add a marker to the timeline"""
        # Check for overlaps if marker has duration
        if marker.duration_bars > 0:
            for existing_marker in self.markers:
                if marker.overlaps_with(existing_marker):
                    raise ValueError(
                        f"Marker '{marker.name}' overlaps with existing marker '{existing_marker.name}'"
                    )
        self.markers.append(marker)
        self.markers.sort(key=lambda m: m.position_bars)

    def add_section(self, section: TimelineSection) -> None:
        """Add a section to the timeline"""
        # Check for overlaps
        for existing_section in self.sections:
            if (section.start_bar < existing_section.end_bar and
                existing_section.start_bar < section.end_bar):
                raise ValueError(
                    f"Section '{section.name}' overlaps with existing section '{existing_section.name}'"
                )
        self.sections.append(section)
        self.sections.sort(key=lambda s: s.start_bar)

    def get_marker_at_position(self, bar: int) -> Optional[TimelineMarker]:
        """Get marker at specific bar position"""
        for marker in self.markers:
            if marker.position_bars <= bar < marker.end_position_bars:
                return marker
        return None

    def get_section_at_position(self, bar: int) -> Optional[TimelineSection]:
        """Get section at specific bar position"""
        for section in self.sections:
            if section.start_bar <= bar < section.end_bar:
                return section
        return None

    def get_markers_in_range(self, start_bar: int, end_bar: int) -> List[TimelineMarker]:
        """Get all markers within a range of bars"""
        return [
            marker for marker in self.markers
            if (marker.position_bars >= start_bar and
                marker.position_bars < end_bar)
        ]

    def get_sections_in_range(self, start_bar: int, end_bar: int) -> List[TimelineSection]:
        """Get all sections within a range of bars"""
        return [
            section for section in self.sections
            if (section.start_bar < end_bar and
                section.end_bar > start_bar)
        ]

    def get_total_bars(self) -> int:
        """Get total length of timeline in bars"""
        if not self.sections and not self.markers:
            return 0
        
        last_section_end = max(
            (section.end_bar for section in self.sections),
            default=0
        )
        last_marker_end = max(
            (marker.end_position_bars for marker in self.markers),
            default=0
        )
        return max(last_section_end, last_marker_end)

    def validate(self) -> bool:
        """Validate timeline structure"""
        try:
            # Check for overlapping markers with duration
            for i, marker1 in enumerate(self.markers):
                if marker1.duration_bars > 0:
                    for marker2 in self.markers[i+1:]:
                        if marker1.overlaps_with(marker2):
                            return False

            # Check for overlapping sections
            for i, section1 in enumerate(self.sections):
                for section2 in self.sections[i+1:]:
                    if (section1.start_bar < section2.end_bar and
                        section2.start_bar < section1.end_bar):
                        return False

            # Ensure markers are within sections if both are used
            if self.sections and self.markers:
                timeline_length = self.get_total_bars()
                for bar in range(timeline_length):
                    if self.get_section_at_position(bar) is None:
                        return False

            return True
        except Exception:
            return False