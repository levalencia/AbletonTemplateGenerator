from typing import List, Dict
from ..models.midi_pattern import MidiPattern, SessionClip
from ..repositories.pattern_repository import PatternRepository

class PatternService:
    def __init__(self, pattern_repository: PatternRepository):
        self.pattern_repository = pattern_repository

    def get_patterns_for_track(self, genre: str, track_name: str) -> List[SessionClip]:
        """Get all patterns for a specific track in a genre"""
        try:
            patterns = self.pattern_repository.load_patterns(genre)
            return patterns.get(track_name, [])
        except ValueError:
            return []

    def merge_track_patterns(self, genres: List[str], track_name: str) -> List[SessionClip]:
        """Merge patterns for a track from multiple genres"""
        all_patterns = []
        current_slot = 0

        for genre in genres:
            patterns = self.get_patterns_for_track(genre, track_name)
            for pattern in patterns:
                # Adjust slot index to avoid overlaps
                pattern.slot_index = current_slot
                all_patterns.append(pattern)
                current_slot += 1

        return all_patterns

