from typing import List, Dict, Set

from ..models.timeline import TimelineMarker
from ..models.template import Template
from ..models.group import Group
from ..models.track import Track, TrackType
from ..repositories.template_repository import TemplateRepository

class TemplateService:
    def __init__(self, repository: TemplateRepository):
        self.repository = repository

    def create_template(self, genres: List[str]) -> Template:
        """Create a template based on one or more genres"""
        if not genres:
            raise ValueError("At least one genre must be specified")

        templates = []
        for genre in genres:
            try:
                template = self.repository.load_template(genre.strip().lower())
                templates.append(template)
            except ValueError as e:
                print(f"Warning: {str(e)}")

        if not templates:
            raise ValueError("No valid templates found for the specified genres")

        if len(templates) == 1:
            return templates[0]

        return self.merge_templates(templates)

    def merge_templates(self, templates: List[Template]) -> Template:
        """Merge multiple templates into one, finding common elements"""
        if not templates:
            raise ValueError("No templates to merge")

        # Find common groups and tracks
        common_groups = self._find_common_groups(templates)
        
        # Calculate average tempo and duration
        avg_tempo = sum(t.default_tempo for t in templates) / len(templates)
        avg_duration = sum(t.default_duration_minutes for t in templates) / len(templates)

        # Merge timeline markers
        merged_markers = self._merge_timeline_markers(templates)

        return Template(
            genre="+".join(t.genre for t in templates),
            groups=common_groups,
            default_tempo=avg_tempo,
            default_duration_minutes=avg_duration,
            timeline_markers=merged_markers
        )

    def _find_common_groups(self, templates: List[Template]) -> List[Group]:
        """Find groups that appear in all templates"""
        common_groups = []
        reference_groups = templates[0].groups

        for ref_group in reference_groups:
            # Check if similar group exists in all other templates
            if all(self._find_similar_group(ref_group, t.groups) for t in templates[1:]):
                merged_group = self._merge_similar_groups(
                    [self._find_similar_group(ref_group, t.groups) for t in templates]
                )
                common_groups.append(merged_group)

        return common_groups

    def _find_similar_group(self, reference: Group, groups: List[Group]) -> Group:
        """Find a group similar to the reference in a list of groups"""
        for group in groups:
            if self._are_groups_similar(reference, group):
                return group
        return None

    def _are_groups_similar(self, group1: Group, group2: Group) -> bool:
        """Check if two groups are similar (same purpose)"""
        # Groups are considered similar if they have the same color
        # and similar names or similar track types
        if group1.color == group2.color:
            return True
        return False

    def _merge_similar_groups(self, groups: List[Group]) -> Group:
        """Merge similar groups into one"""
        if not groups:
            return None

        # Use first group as base
        base_group = groups[0]

        # Find common tracks
        common_tracks = self._find_common_tracks(groups)

        return Group(
            name=base_group.name,
            color=base_group.color,
            tracks=common_tracks,
            subgroups=[]  # Merge subgroups if needed
        )

    def _find_common_tracks(self, groups: List[Group]) -> List[Track]:
        """Find tracks that appear in all groups"""
        common_tracks = []
        reference_tracks = groups[0].tracks

        for ref_track in reference_tracks:
            # Check if similar track exists in all other groups
            similar_tracks = [
                self._find_similar_track(ref_track, group.tracks)
                for group in groups[1:]
            ]
            
            if all(similar_tracks):
                merged_track = self._merge_similar_tracks([ref_track] + similar_tracks)
                common_tracks.append(merged_track)

        return common_tracks

    def _find_similar_track(self, reference: Track, tracks: List[Track]) -> Track:
        """Find a track similar to the reference in a list of tracks"""
        for track in tracks:
            if self._are_tracks_similar(reference, track):
                return track
        return None

    def _are_tracks_similar(self, track1: Track, track2: Track) -> bool:
        """Check if two tracks are similar (same purpose)"""
        # Tracks are considered similar if they have the same color
        # and compatible types
        if track1.color == track2.color:
            if track1.type == track2.type or track1.type.BOTH in (track1.type, track2.type):
                return True
        return False

    def _merge_similar_tracks(self, tracks: List[Track]) -> Track:
        """Merge similar tracks into one"""
        if not tracks:
            return None

        # Use maximum number of layers
        max_layers = max(track.layers for track in tracks)

        # Use most flexible track type
        track_type = TrackType.BOTH if any(t.type == TrackType.BOTH for t in tracks) else tracks[0].type

        return Track(
            name=tracks[0].name,
            type=track_type,
            color=tracks[0].color,
            layers=max_layers
        )

    def _merge_timeline_markers(self, templates: List[Template]) -> List[TimelineMarker]:
        """Merge timeline markers from multiple templates"""
        # For now, use the markers from the template with the most detailed timeline
        return max(templates, key=lambda t: len(t.timeline_markers)).timeline_markers