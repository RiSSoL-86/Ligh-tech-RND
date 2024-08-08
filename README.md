# Тестовое задание от Ligh-tech RND

Создание API-сервиса согласно ТЗ

## Установка и первый запуск

Для установки и запуска микросервиса `Ligh-tech RND` необходимо выполнить следующие шаги:

- Клонируйте репозиторий Ligh-tech RND:
```sh
git clone git@github.com:RiSSoL-86/Ligh-tech-RND.git
```
- Перейдите в директорию Ligh-tech RND:
```sh
cd Ligh-tech RND
```
- Создайте файл .env по примеру из .env.example
- Запустить контейнер для локальной разработки
```sh
docker compose stop && docker compose up --build
```
- Открыть дополнительный терминал и накатить миграции в Docker
```sh
docker-compose exec service poetry run python app/manage.py migrate
```
- Создать суперпользователя для административной панели Django
```sh
docker-compose exec service poetry run python app/manage.py createsuperuser
```


- Админ панель: http://localhost:8000/admin

Для небольшой проверки работоспособности ручек можно воспользоваться коллекцией для Postman.
