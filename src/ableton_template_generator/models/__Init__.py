"""Models module for template generation."""

from .track import Track, TrackType, ColorCode
from .group import Group
from .template import Template
from .timeline import (
    TimelineMarker,
    TimelineSection,
    Timeline,
    TimeSignature
)
from .midi_pattern import (
    MidiNote,
    MidiCC,
    MidiPattern,
    SessionClip,
    PatternVariation,
    NoteLength,
    Velocity,
    AutomationPoint,
    AutomationEnvelope
)

__all__ = [
    'Track',
    'TrackType',
    'ColorCode',
    'Group',
    'Template',
    'TimelineMarker',
    'TimelineSection',
    'Timeline',
    'TimeSignature',
    'MidiNote',
    'MidiCC',
    'MidiPattern',
    'SessionClip',
    'PatternVariation',
    'NoteLength',
    'Velocity',
    'AutomationPoint',
    'AutomationEnvelope'
]