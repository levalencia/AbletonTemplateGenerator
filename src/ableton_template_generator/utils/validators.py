from typing import List
from ..models import Template, Group, Track

def validate_template(template: Template) -> bool:
    """Validate template structure and settings"""
    if not template.groups:
        return False
    
    return all([
        validate_group(group) for group in template.groups
    ])

def validate_group(group: Group) -> bool:
    """Validate group structure"""
    if not group.tracks:
        return False
    
    return all([
        validate_track(track) for track in group.tracks
    ])

def validate_track(track: Track) -> bool:
    """Validate track settings"""
    return (
        track.name and
        track.type and
        track.color and
        track.layers > 0
    )