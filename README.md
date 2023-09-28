# &#129361; FOODGRAM
## _"Продуктовый помощник"_

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Foodgram - сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд с возможностью скачать файл с перечнем и количеством необходимых ингредиентов для всех рецептов.

### __Возможности Foodgram__
- Регистрация и авторизация пользователя.
- Создание/обновление/удаление рецепта: название, описание, время приготовления, выбор ингредиентов, тегов, загрузка фотографии.
- Просмотр выбранного рецепта.
- Просмотр всех рецептов всех пользователей.
- Просмотре всех рецептов выбранного пользователя.
- Подписка на пользователей.
- Добавление рецептов в Избанное.
- Добавление рецептов в Список покупок.
- Скачивание файла с перечнем и количеством ингредиентов из Списка покупок.
- Фильтрация рецептов по тегам.

### __Установка на локальном компьютере__
1. Клонируйте репозиторий
```
> git clone git@github.com:Lozhkin-pa/foodgram-project-react.git
```
2. Установите и активируйте виртуальное окружение
```
> python -m venv venv
> source venv/Scripts/activate  - для Windows
> source venv/bin/activate - для Linux
```
3. Установите зависимости
```
> python -m pip install --upgrade pip
> pip install -r requirements.txt
```
4. Перейдите в папку backend и выполните миграции
```
> cd backend
> python manage.py migrate
```
5. Создайте суперпользователя
```
> python manage.py createsuperuser
```
6. Загрузите подготовленную базу ингредиентов
```
> python manage.py import_data
```
7. Запустите проект
```
> python manage.py runserver
```

### __Развертывание на удаленном сервере__
1. Создайте папку проекта в домашней директории сервера и перейдите в нее
```
> mkdir foodgram
> cd foodgram
```
2. Скопируйте на сервер в папку проекта файл docker-compose.production.yml
3. Скачайте с Docker Hub на сервер образы для контейнеров
```
> sudo docker compose -f docker-compose.production.yml pull
```
4. Запустите контейнеры в режиме демона
```
> sudo docker compose -f docker-compose.production.yml up -d
```
5. Выполните команды для миграций и сборки статики
```
> sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
> sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
> sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collect_static/. /static_backend/static/
```
6. Загрузите подготовленную базу ингредиентов
```
> sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_data
```
7. Создайте суперпользователя
```
> sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

### __Суперпользователь__
```
https://myfoodgramproject.sytes.net/
usermane: Admin
email: admin@mail.ru
password: Admin
```

### __Примеры запросов__

- **GET:** http://127.0.0.1:8000/api/users/  - показать список всех пользователей.

Пример ответа (200 OK):
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```
- **POST:** http://127.0.0.1:8000/api/users/  - регистрация пользователя.

Пример тела запроса:
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
Пример ответа (200 OK):
```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```
- **GET:** http://127.0.0.1:8000/api/recipes/  - показать список всех рецептов.

Пример ответа (200 OK):
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```
- **POST:** http://127.0.0.1:8000/api/recipes/  - создание рецепта.

Пример тела запроса:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Пример ответа (200 OK):
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

### __Технологии__
* [Python 3.2.0](https://www.python.org/doc/)
* [Django 3.2.3](https://docs.djangoproject.com/en/4.2/)
* [Django Rest Framework  3.12.4](https://www.django-rest-framework.org/)
* [Djoser 2.1.0](https://djoser.readthedocs.io/en/latest/getting_started.html)
* [Gunicorn 20.1.0](https://gunicorn.org/#docs)
* [Nginx 1.21.3](https://docs.nginx.com/)
* [Docker 20.10.14](https://docs.docker.com/)

### __Автор__
Бэкенд-разработка: [Павел Ложкин](https://github.com/Lozhkin-pa)
