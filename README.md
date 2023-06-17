# Проект «Продуктовый помощник» - Foodgram

Foodgram - cервис, позволяющий авторизованным пользователям публиковать свои рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Неавторизованные пользователи могут просматривать опубликованные рецепты.

[Адрес проекта](http://62.84.120.235/)

Пользователи:
- admin@gmail.com admin (для админки логин admin)
- testuser1@gmail.com shinkava1309
- testuser2@gmail.com shinkava1309

## Инструкция по развертыванию проекта

1. Установить соединение с сервером
```
ssh username@server_address
```
2. Обновите индекс пакетов APT и обновите установленные в системе пакеты и установите обновления безопасности
```
sudo apt update
sudo apt upgrade -y
```
3. В корневую папку скопируйте файлы nginx.conf и docker-compose.yml, а также содержимое папки Docs
```
nano nginx.conf 
sudo docker-compose.yml
```
```
mkdir docs
cd docs
nano openapi-schema.yml
nano redoc.html
```
4. Установите Docker и Docker-compose
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
```
Проверка корректности установки:
sudo  docker-compose --version
```
5. На сервере создайте файл .env и заполните переменные окружения
```
nano .env
```
```
SECRET_KEY=<SECRET_KEY>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## Инструкция после успешного развертывания проекта
1. На сервере соберите docker-compose
```
sudo docker-compose up -d --build
```
2. Выполните миграции
```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate --noinput
```
3. Соберите статику
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
4. Создайте суперпользователя
```
sudo docker-compose exec web python manage.py createsuperuser
```
5. Наполните базу ингредиентами
```
sudo docker-compose exec web python manage.py load_ingredients
```

## Дополнительные команды
- Для остановки контейнеров с их удалением
```
sudo docker compose down -v 
```
- Для остановки контейнеров без удаления
```
sudo docker compose stop 
```
- Для удаления неиспользуемых образов
```
sudo image prune
```
- Для внесения изменений в образ бэкенда (локально)
```
docker build -t shinkava/foogram-backend:v5 .
```
- Для отправки образа
```
docker push shinkava/foogram-backend:v5
```
- Для обновления образа на сервере
```
sudo docker pull shinkava/foogram-backend:v5
```

