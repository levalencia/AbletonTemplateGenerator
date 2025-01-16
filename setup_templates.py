import json
from pathlib import Path

def setup_templates():
    # Create templates directory inside src/ableton_template_generator
    package_dir = Path(__file__).parent / "src" / "ableton_template_generator"
    templates_dir = package_dir / "templates"
    templates_dir.mkdir(exist_ok=True, parents=True)
    
    # Cumbia template
    cumbia_template = {
        "genre": "cumbia",
        "default_tempo": 90,
        "default_duration_minutes": 3.5,
        "groups": [
            {
                "name": "Rhythm",
                "color": "YELLOW",
                "tracks": [
                    {
                        "name": "Guiro",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 1
                    },
                    {
                        "name": "Congas",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 2
                    },
                    {
                        "name": "Drums",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 1
                    }
                ]
            },
            {
                "name": "Bass",
                "color": "BLUE",
                "tracks": [
                    {
                        "name": "Bass",
                        "type": "MIDI",
                        "color": "BLUE",
                        "layers": 1
                    }
                ]
            },
            {
                "name": "Harmony",
                "color": "GREEN",
                "tracks": [
                    {
                        "name": "Keys",
                        "type": "MIDI",
                        "color": "GREEN",
                        "layers": 2
                    },
                    {
                        "name": "Guitar",
                        "type": "BOTH",
                        "color": "GREEN",
                        "layers": 1
                    }
                ]
            }
        ],
        "timeline_markers": [
            {
                "name": "Intro",
                "position_bars": 0,
                "duration_bars": 8,
                "description": "Percussion build-up",
                "marker_type": "SECTION_START"
            },
            {
                "name": "Verse 1",
                "position_bars": 8,
                "duration_bars": 16,
                "description": "Main cumbia pattern",
                "marker_type": "SECTION_START"
            },
            {
                "name": "Chorus",
                "position_bars": 24,
                "duration_bars": 16,
                "description": "Full intensity",
                "marker_type": "SECTION_START"
            }
        ]
    }

    # Nu Disco template
    nudisco_template = {
        "genre": "nudisco",
        "default_tempo": 118,
        "default_duration_minutes": 4.5,
        "groups": [
            {
                "name": "Drums",
                "color": "YELLOW",
                "tracks": [
                    {
                        "name": "Kick",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 1
                    },
                    {
                        "name": "Snare",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 1
                    },
                    {
                        "name": "Hats",
                        "type": "BOTH",
                        "color": "YELLOW",
                        "layers": 2
                    }
                ]
            },
            {
                "name": "Bass",
                "color": "BLUE",
                "tracks": [
                    {
                        "name": "Bass",
                        "type": "MIDI",
                        "color": "BLUE",
                        "layers": 1
                    }
                ]
            },
            {
                "name": "Harmony",
                "color": "GREEN",
                "tracks": [
                    {
                        "name": "Strings",
                        "type": "MIDI",
                        "color": "GREEN",
                        "layers": 2
                    },
                    {
                        "name": "Keys",
                        "type": "MIDI",
                        "color": "GREEN",
                        "layers": 2
                    }
                ]
            },
            {
                "name": "FX",
                "color": "PURPLE",
                "tracks": [
                    {
                        "name": "Impacts",
                        "type": "AUDIO",
                        "color": "PURPLE",
                        "layers": 1
                    },
                    {
                        "name": "Risers",
                        "type": "AUDIO",
                        "color": "PURPLE",
                        "layers": 1
                    }
                ]
            }
        ],
        "timeline_markers": [
            {
                "name": "Intro",
                "position_bars": 0,
                "duration_bars": 16,
                "description": "Filtered build-up",
                "marker_type": "SECTION_START"
            },
            {
                "name": "Break",
                "position_bars": 16,
                "duration_bars": 8,
                "description": "Drop preparation",
                "marker_type": "SECTION_START"
            },
            {
                "name": "Drop",
                "position_bars": 24,
                "duration_bars": 32,
                "description": "Main groove",
                "marker_type": "SECTION_START"
            }
        ]
    }

    # Save templates
    with open(templates_dir / "cumbia.json", 'w') as f:
        json.dump(cumbia_template, f, indent=2)
    
    with open(templates_dir / "nudisco.json", 'w') as f:
        json.dump(nudisco_template, f, indent=2)

    print(f"Templates created in: {templates_dir.resolve()}")
    return str(templates_dir.resolve())