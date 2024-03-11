from csv import DictReader
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Comment, Category, Review, Title, Genre

User = get_user_model()


class Command(BaseCommand):
    help = 'Imports data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_directory', type=str)

    def handle(self, *args, **options):
        csv_directory = options['csv_directory']

        for row in DictReader(open(Path(csv_directory) / 'users.csv',
                                   encoding='utf-8')):
            user = User(id=row['id'],
                        username=row['username'],
                        email=row['email'],
                        role=row['role'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'])
            user.save()
        self.stdout.write(self.style.SUCCESS('User выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'category.csv',
                                   encoding='utf-8')):
            category = Category(id=row['id'],
                                name=row['name'],
                                slug=row['slug'])
            category.save()
        self.stdout.write(self.style.SUCCESS('Category выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'genre.csv',
                                   encoding='utf-8')):
            genre = Genre(id=row['id'],
                          name=row['name'],
                          slug=row['slug'])
            genre.save()
        self.stdout.write(self.style.SUCCESS('Genre выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'titles.csv',
                                   encoding='utf-8')):
            title = Title(id=row['id'],
                          name=row['name'],
                          year=row['year'],
                          category=Category.objects.get(id=row['category']))
            title.save()
        self.stdout.write(self.style.SUCCESS('Title выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'review.csv',
                                   encoding='utf-8')):
            review = Review(id=row['id'],
                            title=Title.objects.get(id=row['title_id']),
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            score=row['score'],
                            pub_date=row['pub_date'])
            review.save()
        self.stdout.write(self.style.SUCCESS('Review выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'comments.csv',
                                   encoding='utf-8')):
            comment = Comment(id=row['id'],
                              review=Review.objects.get(id=row['review_id']),
                              text=row['text'],
                              author=User.objects.get(id=row['author']),
                              pub_date=row['pub_date'])
            comment.save()
        self.stdout.write(self.style.SUCCESS('Comment выполнен успешно'))

        for row in DictReader(open(Path(csv_directory) / 'genre_title.csv',
                                   encoding='utf-8')):
            title = Title.objects.get(pk=row['title_id'])
            genre = Genre.objects.get(pk=row['genre_id'])
            title.genre.add(genre)
            comment.save()
        self.stdout.write(self.style.SUCCESS('genre_title выполнен успешно'))

        self.stdout.write(self.style.SUCCESS('Импорт данных выполнен!'))
