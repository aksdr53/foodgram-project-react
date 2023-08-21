import csv

from django.core.management.base import BaseCommand

from app.models import Ingredient
from foodgram.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, filepath):
        with open(BASE_DIR/filepath, 'r') as file:
            reader = csv.DictReader(file)
            ingredients = []
            for row in reader:
                ingredients.append(Ingredient(
                    name=row[0],
                    measurement_unit=row[1]
                ))
        Ingredient.objects.bulk_create(ingredients)