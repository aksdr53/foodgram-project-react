## Tecnhologies
`Python` `Django` `Django Rest Framework` `Docker` `Gunicorn` `NGINX` `PostgreSQL` `Yandex Cloud` `Continuous Integration` `Continuous Deployment`

# **_Foodgram_**
Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

```
topcats.site
```

### Локальный запуск проекта:

**_Склонировать репозиторий к себе_**
```
git@github.com:aksdr53/foodgram-project-react.git
```

**_В корневой директории создать файл .env и заполнить своими данными:_**
```
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```
**_Установить Docker, Docker Compose:_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```
**_Создать и запустить контейнеры Docker**_
```
sudo docker compose up -d
```
**_Выполнить миграции:_**
```
sudo docker compose exec backend python manage.py migrate
```
**_Собрать статику:_**
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```
**_Наполнить базу данных содержимым из файла ingredients.json:_**
```
sudo docker compose exec backend python manage.py load_data
```
**_Создать суперпользователя:_**
```
sudo docker compose exec backend python manage.py createsuperuser
```
**_Для остановки контейнеров Docker:_**
```
sudo docker compose down -v      - с их удалением
sudo docker compose stop         - без удаления
```

**_После запуска проект будут доступен по адресу: http://localhost/_**

**_Документация будет доступна по адресу: http://localhost/api/docs/_**

### Автор
Мыльников Александр