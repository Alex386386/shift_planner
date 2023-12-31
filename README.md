# Shift planner

### Описание

Тестовое задание представляющее собой API интерфейс для создания расписания работы сотрудников на месяц.
Согласно ТЗ каждый день представляет собой смену продолжительностью с 8:00 до 22:00.
Максимальное количество смен для сотрудника 12, продолжительностью по 12 часов. 
В связи с предоставленными требованиями, оптимальным графиком работы выбран 1/2, с возможными доп. сменами по понедельникам.
Минимальное количество сотрудников для оптимального их распределения равно шести. При меньшем количестве сотрудников возможны переработки.

## Stack

Python 3.11, Django 4.2, Django Rest Framework 3.14.0

### Установка, Как запустить проект:

Перейдите в папку с проектом:

```
cd shift_planner/
```

Создайте файл .env со следующим содержанием:

```
SECRET_KEY=<your django secret key>
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в папку с файлом manage.py
```
cd job_scheduler/
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать суперюзера:

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```


### Эндпоинты и примеры запросов:

Список запросов:

1. Запросы к эндпоинту юзера(стандартные эндпоинты djoser):

    POST /api/v1/auth/jwt/create/ - Получение токена для доступа к сайту и создания расписания и пользователей
    
    ```json
    {
        "username": "name",
        "password": "password"
    }
    ```
    
    POST /api/v1/auth/users/ - Создание нового пользователя
    
    ```json
    {
        "username": "name",
        "password": "password"
    }
    ```
   
    Пример ответа:
    
    ```json
    {
        "id": 1,
        "year": 2023,
        "month_number": 11,
        "days": [
            {
                "id": 1,
                "day_number": 1,
                "workers_required": 2,
                "workers": [
                    {
                        "id": 1,
                        "name": "name"
                    },
                    {
                        "id": 2,
                        "name": "name"
                    }
                ]
            },
            ...
        ]
    }
    ```

2. Запросы к эндпоинту месяца, для получения расписания:

    GET /api/v1/month/ - Получение списка месяцов

    GET /api/v1/month/{month_id} - Получение расписания на конкретный месяц

    POST /api/v1/month/ - Создание расписания на конкретный месяц, нельзя указать дату меньше чем настоящая. (только аутентифицированный пользователь)

    ```json
    {
        "month_number": 11,
        "year": 2023
    }
    ```
    
    DELETE /api/v1/month/{month_id} - Удаление расписания на конкретный месяц вместе со всеми объектами дней. (только аутентифицированный пользователь)

3. Запросы к эндпоинту работников:

    GET /api/v1/worker/{worker_id} - Получение работника

    GET /api/v1/worker/ - Получение списка всех работников
  
    POST /api/v1/worker/ - Создание объекта работника (только аутентифицированный пользователь)
  
    ```json
    {
        "name": "name"
    }
    ```
   
TODO:

1. Добавить модель event для событий внутри месяца и дальнейшей переработки месяца под события.
2. Добавить обработку команды PATCH для вьюсета месяца.
3. Добавить функционал построения графика по последним дням предыдущего месяца.
4. Дописать тесты.


Автор:

- [Александр Мамонов](https://github.com/Alex386386) 
