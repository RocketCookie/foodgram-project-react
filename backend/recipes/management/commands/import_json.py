import json
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из JSON файла в таблицу Ingredients'

    def handle(self, *args, **kwargs):
        with open(
                settings.FILE_INGREDIENTS_PATH, 'r', encoding='utf8') as file:
            data = json.load(file)
            for item in data:
                if not Ingredient.objects.filter(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']).exists():
                    Ingredient.objects.create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных прошла успешно.'))
