from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dataclasses import dataclass
from enum import Enum

class AIProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    CUSTOM = "custom"

@dataclass
class AIModelConfig:
    provider: AIProvider
    model_name: str
    temperature: float
    max_tokens: int
    api_url: str
    timeout: int = 30

@dataclass
class GenreSettings:
    preferred_complexity: int
    typical_bar_length: int
    instruments: Dict[str, Dict[str, Any]]

@dataclass
class PatternGenerationSettings:
    default_variations: int
    max_variations: int
    complexity_range: tuple
    default_bars: int
    max_bars: int

class AIConfig:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize AI configuration from YAML file"""
        if config_path is None:
            # Default to config directory in package
            package_dir = Path(__file__).parent.parent
            config_path = package_dir / "config" / "ai_generation.yml"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.model_config = self._init_model_config()
        self.pattern_settings = self._init_pattern_settings()
        self.genre_settings = self._init_genre_settings()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing config file: {str(e)}")

    def _init_model_config(self) -> AIModelConfig:
        """Initialize AI model configuration"""
        api_config = self.config['ai_generation']['api']
        
        return AIModelConfig(
            provider=AIProvider(api_config['provider']),
            model_name=api_config['model'],
            temperature=api_config.get('temperature', 0.7),
            max_tokens=api_config.get('max_tokens', 2000),
            api_url=api_config.get('api_url', self._get_default_api_url(api_config['provider'])),
            timeout=api_config.get('timeout', 30)
        )

    def _init_pattern_settings(self) -> PatternGenerationSettings:
        """Initialize pattern generation settings"""
        pattern_config = self.config['ai_generation']['pattern_generation']
        
        return PatternGenerationSettings(
            default_variations=pattern_config.get('default_variations', 2),
            max_variations=pattern_config.get('max_variations', 5),
            complexity_range=tuple(pattern_config.get('complexity_range', [1, 5])),
            default_bars=pattern_config.get('default_bars', 2),
            max_bars=pattern_config.get('max_bars', 8)
        )

    def _init_genre_settings(self) -> Dict[str, GenreSettings]:
        """Initialize genre-specific settings"""
        genre_configs = self.config['ai_generation']['genre_specific_settings']
        genre_settings = {}
        
        for genre, settings in genre_configs.items():
            genre_settings[genre] = GenreSettings(
                preferred_complexity=settings.get('preferred_complexity', 3),
                typical_bar_length=settings.get('typical_bar_length', 4),
                instruments=settings.get('instruments', {})
            )
            
        return genre_settings

    def _get_default_api_url(self, provider: str) -> str:
        """Get default API URL for provider"""
        urls = {
            'anthropic': 'https://api.anthropic.com/v1/messages',
            'openai': 'https://api.openai.com/v1/chat/completions',
        }
        return urls.get(provider, '')

    @property
    def is_enabled(self) -> bool:
        """Check if AI generation is enabled"""
        return self.config['ai_generation'].get('enabled', False)

    def get_genre_settings(self, genre: str) -> Optional[GenreSettings]:
        """Get settings for specific genre"""
        return self.genre_settings.get(genre.lower())

    def get_instrument_settings(self, genre: str, instrument: str) -> Dict[str, Any]:
        """Get instrument-specific settings for a genre"""
        genre_settings = self.get_genre_settings(genre)
        if genre_settings:
            return genre_settings.instruments.get(instrument, {})
        return {}

    def get_api_settings(self) -> Dict[str, Any]:
        """Get API-related settings"""
        return {
            'provider': self.model_config.provider.value,
            'model': self.model_config.model_name,
            'temperature': self.model_config.temperature,
            'max_tokens': self.model_config.max_tokens,
            'api_url': self.model_config.api_url,
            'timeout': self.model_config.timeout
        }

    def validate(self) -> bool:
        """Validate configuration"""
        try:
            # Check required sections
            required_sections = ['ai_generation', 'pattern_generation', 'genre_specific_settings']
            for section in required_sections:
                if section not in self.config.get('ai_generation', {}):
                    return False

            # Validate model configuration
            if not self.model_config.api_url:
                return False
            if not (0 <= self.model_config.temperature <= 1):
                return False

            # Validate pattern settings
            if not (0 < self.pattern_settings.max_variations <= 10):
                return False
            if not (1 <= self.pattern_settings.complexity_range[0] <= self.pattern_settings.complexity_range[1] <= 5):
                return False

            return True
        except Exception:
            return False

    def save(self) -> None:
        """Save current configuration to file"""
        config_data = {
            'ai_generation': {
                'enabled': self.is_enabled,
                'api': self.get_api_settings(),
                'pattern_generation': {
                    'default_variations': self.pattern_settings.default_variations,
                    'max_variations': self.pattern_settings.max_variations,
                    'complexity_range': list(self.pattern_settings.complexity_range),
                    'default_bars': self.pattern_settings.default_bars,
                    'max_bars': self.pattern_settings.max_bars
                },
                'genre_specific_settings': {
                    genre: {
                        'preferred_complexity': settings.preferred_complexity,
                        'typical_bar_length': settings.typical_bar_length,
                        'instruments': settings.instruments
                    }
                    for genre, settings in self.genre_settings.items()
                }
            }
        }

        with open(self.config_path, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)