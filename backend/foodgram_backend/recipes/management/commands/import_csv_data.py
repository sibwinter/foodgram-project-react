from csv import DictReader
from django.conf import settings

from django.core.management import BaseCommand
from recipes.models import Ingredient

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезалить данные из файлов CSV в базу данных,
то сначала удалите файл db.sqlite3, затем выполните миграции
командой `python manage.py migrate` для создание новой пустой базы данных.
"""


def import_ingredients(row):
    Ingredient.objects.get_or_create(
        name=row['name'],
        measurement_unit=row['measurement_unit']
    )


DATA_CSV = {
    import_ingredients: 'data/ingredients.csv',
}


class Command(BaseCommand):
    help = "Загрузка данных в базу данных из таблиц CSV"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(("Загружаем данные в базу..."))
        )
        for method, file_path in DATA_CSV.items():
            for row in DictReader(
                open(f'{settings.BASE_DIR.parent.parent}/{file_path}',
                     encoding='utf-8')
            ):
                method(row)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Файл {file_path} успешно импортирован"
                )
            )
