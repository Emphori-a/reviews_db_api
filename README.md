# База отзывов пользователей на произведения - YaMDb.

## Описание:
Проект собирает отзывы и оценки пользователей на произведения. Произведения делятся на категории: фильмы, книги, музыка, также произведению может быть присвоен жанр. Информация о произведениях, их категориях и жанрах обновляется администратором. На основании отзывов и оценок произведений формируется рейтинг произведения. Пользователи могут оставлять комментарии к отзывам.

## Использованные технологии:
Python 3.9  
Django 3.2  
Django REST Framework 3.12  
djangorestframework-simplejwt 5.3.1  

## Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке.
```
git clone https://github.com/Emphori-a/reviews_db_api
```
```
cd reviews_db_api
```

2. Cоздать и активировать виртуальное окружение.
- Если у вас Linux/macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
- Если у вас Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

3. Установить зависимости.
```
python -m pip install --upgrade pip  # обновляем установщик пакетов pip
```
```
pip install -r requirements.txt
```

4. Создать файл ".env" наполнить его данными. Для примера в корне проекта есть файл .env.example.

5. Выполнить миграции.
```
cd api_yamdb/  # переходим в директорию основного приложения
```
```
python manage.py migrate
```

6. Загрузить данные в БД из csv-файлов <sup>(опционально)</sup>.
```
python api_yamdb/manage.py import_csv ./api_yamdb/static/data/
```

7. Создать суперпользователя <sup>(опционально)</sup>.
```
python manage.py createsuperuser
```

8. Запуск проекта.
```
python manage.py runserver
```

## API:

Подробная документация API - http://127.0.0.1:8000/redoc/.  
API доступен по адресу http://127.0.0.1:8000/api/v1/.  
Анонимным пользователям доступны данные только для чтения.  

* Для аутентификации используются JWT-токены и библиотека djangorestframework-simplejwt.
auth/ - Регистрация пользователей и выдача токенов. Реализовано разделение по ролям пользователей: Аноним, Аутентифицированный пользователь, Модератор, Администратор.

* users/ - Пользователи.  
Для списка всех пользователей реализован поиск по имени пользователя(username).
    * Только для пользователя с правом доступа Администратор: получение списка всех пользователей, добавление пользователя, получение пользователя по username, изменение данных пользователя по username, удаление пользователя по username.
    * Для Авторизованного пользователя для своей учетной записи: получение данных своей учетной записи, изменение данных своей учетной записи.  

* titles/ - Произведения, к которым пишут отзывы:
    * Для любых пользователей:
        - получение списка всех произведений, реализована фильтрация по полям: категория(category), жанр(genre), название(name), год(year),
        - получение информации о произведении.
    * Только для пользователя с правом доступа Администратор: добавление произведения, частичное обновление информации о произведении, удаление произведения.

* categories/ - Категории (типы) произведений:
    * Для любых пользователей: получение списка всех категорий, реализован поиск по названию категории(name).
    * Только для пользователя с правом доступа Администратор: добавление новой категории, удаление категории.

* genres/ - Жанры произведений:
    * Для любых пользователей: получение списка всех жанров, реализован поиск по названию категории(name).
    * Только для пользователя с правом доступа Администратор: добавление жанра, удаление жанра.

* reviews/ - Отзывы на произведения:
    * Для любых пользователей: получение списка всех отзывов, полуение отзыва по id.
    * Для пользователей с правом доступа Аутентифицированные пользователи: добавление нового отзыва.
    * Для пользователей с правами доступа: Автор отзыва, модератор или администратор: частичное обновление отзыва по id, удаление отзыва по id.

* comments/ - Комментарии к отзывам:
    * Для любых пользователей: получение списка всех комментариев к отзыву, получение комментария к отзыву.
    * Для пользователей с правом доступа Аутентифицированные пользователи: добавление комментария к отзыву.
    * Для пользователей с правами доступа: Автор комментария, модератор или администратор: частичное обновление комментария к отзыву, удаление комментария к отзыву.

## Авторы, контактная информация:

Семен Григорьев
* https://github.com/haitaks
* e-mail: udieigetpaid@gmail.com

Алексей Мальцев
* https://github.com/Thinker90
* e-mail: lexa.thinker@gmail.com

Мартынова Валерия
* https://github.com/Emphori-a
* e-mail: v.e.martynova@yandex.ru
* Telegram: @Emphori

