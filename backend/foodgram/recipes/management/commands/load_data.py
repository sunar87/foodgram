from csv import reader

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Добавление ингридиентов в БД."""

    def handle(self, *args, **kwargs):
        path = 'recipes/data/ingredients.csv'
        with open(path, 'r', encoding='UTF-8') as ingredients:
            for row in reader(ingredients):
                Ingredient.objects.get_or_create(
                    name=row[0], measurement_unit=row[1],
                )
        self.stdout.write(self.style.SUCCESS('Ингридиенты загружены в БД'))
