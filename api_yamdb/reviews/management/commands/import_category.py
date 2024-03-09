import csv
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from api_yamdb.reviews.models import Category, Comment, Genre, Review, Title


class Command(BaseCommand):
    help = 'Imports data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                try:
                    user = User(
                        id=int(row[0]),
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6])
                    user.set_unusable_password()
                    user.full_clean()
                    user.save()
                except ValidationError as e:
                    self.stdout.write(self.style.WARNING(
                        f"Skipping invalid data for user with id={row[0]}: {e}"
                    ))

        self.stdout.write(self.style.SUCCESS('Импорт данных выполнен успешно'))
