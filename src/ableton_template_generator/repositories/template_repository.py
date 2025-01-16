import json
from pathlib import Path
from typing import Dict, List
from ..models.template import Template
from ..models.group import Group
from ..models.track import Track, TrackType, ColorCode
from ..models.timeline import TimelineMarker, MarkerType

class TemplateRepository:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir).resolve()  # Get absolute path
        print(f"Template directory: {self.templates_dir}")  # Debug print
        self.templates_dir.mkdir(exist_ok=True)

    def load_template(self, genre: str) -> Template:
        template_path = self.templates_dir / f"{genre.lower()}.json"
        print(f"Looking for template at: {template_path}")  # Debug print
        if not template_path.exists():
            raise ValueError(f"No template found for genre: {genre}")

        with open(template_path, 'r') as f:
            data = json.load(f)
            return self._deserialize_template(data)

    def save_template(self, template: Template) -> None:
        template_path = self.templates_dir / f"{template.genre.lower()}.json"
        with open(template_path, 'w') as f:
            json.dump(self._serialize_template(template), f, indent=2)

    def _deserialize_template(self, data: Dict) -> Template:
        timeline_markers = [
            TimelineMarker(
                name=marker['name'],
                position_bars=marker['position_bars'],
                duration_bars=marker['duration_bars'],
                description=marker['description'],
                marker_type=MarkerType[marker.get('marker_type', 'SECTION_START')]
            )
            for marker in data.get('timeline_markers', [])
        ]

        groups = [
            Group(
                name=group['name'],
                color=ColorCode[group['color']],
                tracks=[
                    Track(
                        name=track['name'],
                        type=TrackType[track['type']],
                        color=ColorCode[track['color']],
                        layers=track.get('layers', 1)
                    )
                    for track in group['tracks']
                ],
                subgroups=[
                    Group(**subgroup) for subgroup in group.get('subgroups', [])
                ]
            )
            for group in data['groups']
        ]

        return Template(
            genre=data['genre'],
            groups=groups,
            default_tempo=data.get('default_tempo', 120.0),
            default_duration_minutes=data.get('default_duration_minutes', 4.0),
            timeline_markers=timeline_markers
        )

    def _serialize_template(self, template: Template) -> Dict:
        return {
            'genre': template.genre,
            'default_tempo': template.default_tempo,
            'default_duration_minutes': template.default_duration_minutes,
            'timeline_markers': [
                {
                    'name': marker.name,
                    'position_bars': marker.position_bars,
                    'duration_bars': marker.duration_bars,
                    'description': marker.description,
                    'marker_type': marker.marker_type.name
                }
                for marker in template.timeline_markers
            ],
            'groups': [
                {
                    'name': group.name,
                    'color': group.color.name,
                    'tracks': [
                        {
                            'name': track.name,
                            'type': track.type.name,
                            'color': track.color.name,
                            'layers': track.layers
                        }
                        for track in group.tracks
                    ],
                    'subgroups': [
                        self._serialize_group(subgroup)
                        for subgroup in (group.subgroups or [])
                    ]
                }
                for group in template.groups
            ]
        }

    def _serialize_group(self, group: Group) -> Dict:
        return {
            'name': group.name,
            'color': group.color.name,
            'tracks': [
                {
                    'name': track.name,
                    'type': track.type.name,
                    'color': track.color.name,
                    'layers': track.layers
                }
                for track in group.tracks
            ]
        }