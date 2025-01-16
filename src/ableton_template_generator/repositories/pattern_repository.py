
import json
from pathlib import Path
from typing import Dict, List
from ..models.midi_pattern import MidiPattern, SessionClip

class PatternRepository:
    def __init__(self, patterns_dir: str = "patterns"):
        self.patterns_dir = Path(patterns_dir)

    def load_patterns(self, genre: str) -> Dict[str, List[SessionClip]]:
        """Load MIDI patterns for a specific genre"""
        pattern_file = self.patterns_dir / f"{genre}_patterns.json"
        if not pattern_file.exists():
            raise ValueError(f"No patterns found for genre: {genre}")

        with open(pattern_file, 'r') as f:
            data = json.load(f)
            return self._deserialize_patterns(data)

    def _deserialize_patterns(self, data: Dict) -> Dict[str, List[SessionClip]]:
        """Convert JSON data to SessionClip objects"""
        patterns = {}
        for instrument, clips in data["patterns"].items():
            patterns[instrument] = [
                SessionClip(
                    name=clip["name"],
                    pattern=MidiPattern(
                        name=clip["name"],
                        length_bars=clip["length_bars"],
                        notes=[MidiNote(**note) for note in clip["notes"]]
                    ),
                    slot_index=clip["slot_index"],
                    scene_index=clip["scene_index"],
                    color=clip.get("color")
                )
                for clip in clips["clips"]
            ]
        return patterns