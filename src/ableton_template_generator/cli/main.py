import click
from rich.console import Console
from rich.table import Table
from typing import List

from ..services.template_service import TemplateService
from ..services.pattern_service import PatternService
from ..repositories.template_repository import TemplateRepository
from ..repositories.pattern_repository import PatternRepository
from ..models.template import Template
from ..models.track import Track

console = Console()

def display_template(template: Template):
    """Display template information in a formatted table"""
    # Create main template info table
    main_table = Table(title=f"Template: {template.genre}")
    main_table.add_column("Property", style="cyan")
    main_table.add_column("Value", style="green")

    main_table.add_row("Tempo", f"{template.default_tempo} BPM")
    main_table.add_row("Duration", f"{template.default_duration_minutes} minutes")
    
    console.print(main_table)

    # Create groups and tracks table
    groups_table = Table(title="Groups and Tracks")
    groups_table.add_column("Group", style="cyan")
    groups_table.add_column("Track", style="green")
    groups_table.add_column("Type", style="yellow")
    groups_table.add_column("Layers", style="magenta")

    for group in template.groups:
        for track in group.tracks:
            groups_table.add_row(
                group.name,
                track.name,
                track.type.value,
                str(track.layers)
            )

    console.print(groups_table)

    # Create timeline table
    timeline_table = Table(title="Timeline Markers")
    timeline_table.add_column("Position", style="cyan")
    timeline_table.add_column("Duration", style="green")
    timeline_table.add_column("Description", style="yellow")

    for marker in template.timeline_markers:
        timeline_table.add_row(
            f"{marker.position_bars} bars",
            f"{marker.duration_bars} bars",
            marker.description
        )

    console.print(timeline_table)

@click.group()
def cli():
    """Ableton Template Generator CLI"""
    pass

@cli.command()
@click.argument('genres', nargs=-1, required=True)
@click.option('--output', '-o', help='Output directory for the template')
@click.option('--with-patterns/--no-patterns', default=True, 
              help='Include MIDI patterns in the template')
def create(genres: List[str], output: str, with_patterns: bool):
    """Create a new template for specified genres"""
    try:
        # Initialize services
        template_repo = TemplateRepository(output if output else "templates")
        pattern_repo = PatternRepository()
        template_service = 