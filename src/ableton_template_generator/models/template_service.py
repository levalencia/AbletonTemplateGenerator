from typing import List
from ..models import Template, Group, Track
from ..repositories import TemplateRepository

class TemplateService:
    def __init__(self, repository: TemplateRepository):
        self.repository = repository

    def create_template(self, genres: List[str]) -> Template:
        templates = [self.repository.load_template(genre) for genre in genres]
        if len(templates) == 1:
            return templates[0]
        return self.merge_templates(templates)

    def merge_templates(self, templates: List[Template]) -> Template:
        # Implementation of template merging logic
        pass