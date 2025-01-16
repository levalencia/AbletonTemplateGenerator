from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class NoteLength(Enum):
    THIRTYSECOND = 0.125
    SIXTEENTH = 0.25
    EIGHTH = 0.5
    QUARTER = 1.0
    HALF = 2.0
    WHOLE = 4.0

class Velocity(Enum):
    PPP = 16    # Pianississimo
    PP = 32     # Pianissimo
    P = 48      # Piano
    MP = 64     # Mezzo-piano
    MF = 80     # Mezzo-forte
    F = 96      # Forte
    FF = 112    # Fortissimo
    FFF = 127   # Fortississimo

@dataclass
class MidiNote:
    pitch: int              # MIDI note number (0-127)
    velocity: int           # Note velocity (0-127)
    position: float         # Position in beats (0.0 = start of bar)
    duration: float         # Duration in beats
    probability: float = 1.0  # Probability for randomization/humanization (0.0-1.0)
    channel: int = 0        # MIDI channel (0-15)
    
    def validate(self) -> bool:
        """Validate MIDI note parameters"""
        return (
            0 <= self.pitch <= 127 and
            0 <= self.velocity <= 127 and
            self.position >= 0 and
            self.duration > 0 and
            0 <= self.probability <= 1 and
            0 <= self.channel <= 15
        )

@dataclass
class MidiCC:
    """MIDI Control Change message"""
    controller: int         # CC number (0-127)
    value: int             # CC value (0-127)
    position: float        # Position in beats
    channel: int = 0       # MIDI channel (0-15)

@dataclass
class AutomationPoint:
    """Automation point for parameters"""
    value: float           # Parameter value
    position: float        # Position in beats
    curve: float = 0.0     # Curve type (-1.0 to 1.0, 0 = linear)

@dataclass
class AutomationEnvelope:
    """Parameter automation envelope"""
    parameter_name: str
    points: List[AutomationPoint]
    loop_start: Optional[float] = None
    loop_end: Optional[float] = None

@dataclass
class MidiPattern:
    name: str
    length_bars: int
    notes: List[MidiNote]
    time_signature_numerator: int = 4
    time_signature_denominator: int = 4
    swing_amount: float = 0.0          # 0.0 = no swing, 1.0 = maximum swing
    groove_amount: float = 0.0         # 0.0 = no groove, 1.0 = maximum groove
    velocity_variation: float = 0.0    # Random velocity variation amount
    timing_variation: float = 0.0      # Random timing variation in beats
    control_changes: List[MidiCC] = None
    automations: List[AutomationEnvelope] = None
    metadata: Dict[str, Any] = None    # Additional pattern metadata

    def __post_init__(self):
        """Initialize optional fields"""
        if self.control_changes is None:
            self.control_changes = []
        if self.automations is None:
            self.automations = []
        if self.metadata is None:
            self.metadata = {}

    def get_duration_beats(self) -> float:
        """Get total duration in beats"""
        return self.length_bars * self.time_signature_numerator

    def get_notes_at_position(self, position: float, tolerance: float = 0.01) -> List[MidiNote]:
        """Get all notes at a specific position"""
        return [
            note for note in self.notes
            if abs(note.position - position) <= tolerance
        ]

    def add_note(self, note: MidiNote) -> None:
        """Add a note to the pattern"""
        if note.validate():
            self.notes.append(note)
        else:
            raise ValueError("Invalid MIDI note parameters")

    def add_automation(self, parameter: str, points: List[AutomationPoint]) -> None:
        """Add an automation envelope"""
        envelope = AutomationEnvelope(parameter_name=parameter, points=points)
        self.automations.append(envelope)

    def quantize_notes(self, grid: float = 0.25) -> None:
        """Quantize notes to a specific grid"""
        for note in self.notes:
            note.position = round(note.position / grid) * grid
            note.duration = round(note.duration / grid) * grid

    def transpose(self, semitones: int) -> None:
        """Transpose all notes by a number of semitones"""
        for note in self.notes:
            new_pitch = note.pitch + semitones
            if 0 <= new_pitch <= 127:
                note.pitch = new_pitch

@dataclass
class SessionClip:
    """Represents a clip in Ableton's Session View"""
    name: str
    pattern: MidiPattern
    slot_index: int        # Vertical position in session view
    scene_index: int       # Horizontal position in session view
    color: Optional[str] = None
    launch_quantization: Optional[str] = "1 bar"
    launch_mode: str = "trigger"  # trigger, gate, repeat
    launch_probability: float = 1.0
    follow_action: Optional[str] = None
    follow_action_time: Optional[float] = None

    def duplicate(self, new_slot: int, new_scene: int) -> 'SessionClip':
        """Create a copy of the clip in a new position"""
        return SessionClip(
            name=f"{self.name} (Copy)",
            pattern=self.pattern,
            slot_index=new_slot,
            scene_index=new_scene,
            color=self.color,
            launch_quantization=self.launch_quantization,
            launch_mode=self.launch_mode,
            launch_probability=self.launch_probability,
            follow_action=self.follow_action,
            follow_action_time=self.follow_action_time
        )

@dataclass
class PatternVariation:
    """Represents a variation of a base pattern"""
    base_pattern: MidiPattern
    variation_type: str    # e.g., "velocity", "timing", "notes", "combination"
    variation_amount: float  # 0.0 = minimal variation, 1.0 = maximum variation
    preserve_rhythm: bool = True
    preserve_pitches: bool = False
    
    def generate(self) -> MidiPattern:
        """Generate a new pattern based on the variation settings"""
        # Implementation would depend on the variation type
        # This would contain the logic for creating variations
        pass