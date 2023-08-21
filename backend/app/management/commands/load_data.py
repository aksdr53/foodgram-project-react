import csv

from django.core.management.base import BaseCommand

from app.models import Ingredient
from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(BASE_DIR/'ingredients.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ingredients = []
            for row in reader:
                print(row)
                ingredients.append(Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit']
                ))
        Ingredient.objects.bulk_create(ingredients)