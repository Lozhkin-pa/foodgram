from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    """
    Импорт ингредиентов в базу данных проекта.
    """
    help = 'Import CSV files'

    def handle(self, *args, **options):
        try:
            with open(
                f'{settings.BASE_DIR}/data/ingredients.csv',
                'r',
                encoding='utf-8'
            ) as csv_file:

                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1]
                    )

            self.stdout.write(
                self.style.SUCCESS('Файл ingredients.csv загружен!')
            )
        except ValueError as error:
            print(f'Ошибка при загрузке файла ingredients.csv: {error}')
