import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из JSON файла в таблицу Ingredients'

    def handle(self, *args, **kwargs):
        with open(
            settings.FILE_INGREDIENTS_PATH, 'r', encoding='utf8'
        ) as file:
            data = json.load(file)

            ingredients_to_create = []
            for item in data:
                name = item['name']
                measurement_unit = item['measurement_unit']

                if not Ingredient.objects.filter(
                    name=name, measurement_unit=measurement_unit
                ).exists():
                    ingredients_to_create.append(
                        Ingredient(
                            name=name, measurement_unit=measurement_unit
                        )
                    )
            Ingredient.objects.bulk_create(ingredients_to_create)
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных прошла успешно.')
        )
