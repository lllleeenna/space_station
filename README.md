# API cервис по управлению космическими станциями.
В сервисе хранится информация о станциях и их позиции в пространстве. 

## Описание сервиса
У станции 3 координаты: x, y, z. 
При запуске станции ее координаты по умолчанию равны: 100, 100, 100.

Станция исправно может двигаться только в диапазоне положительных координат.
Если Станция вышла за эти координаты, мы считаем ее неисправной,
даже если в будущем она вернулась обратно в разрешенную зону.

Позиция станции меняется через Указание: ось и значение смещения.
За одно Указание можно сместиться только в одну сторону на неограниченное
расстояние.
Например:
Указание #1: ось: x, смещение: -100.
После получения этого указания станция сдвинется по оси X на 100 в лево.

## Технологии
- python 3.9
- Django 3.2.16
- djangorestframework 3.12.4
- Pytest
- swagger

## Реализованы следующие эндпойнты:
* GET, POST: /stations/ - Просмотр списка станций, создание станции
* GET, PUT, PATCH, DELETE: /stations/{station_id}/ - Просмотре, изменение
  и удаление станции.
* GET: /stations/{station_id}/state/ - Получение координат станции.
* POST: /stations/{station_id}/state/ - Изменение позиции станции.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lllleeenna/space_station.git
```

```
cd space_station
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

На основе написанных эндпоинтов генерируется swagger, 
доступен по ссылке http://127.0.0.1:8000/api/schema/swagger/. 
Для генерации документации используется drf-spectacular. 