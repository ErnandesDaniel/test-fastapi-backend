# Employee Management API

FastAPI приложение для управления сотрудниками, их отпусками и командировками.

## Функциональность

### Сотрудники (Employees)
- Создание, просмотр, обновление и удаление сотрудников
- Получение детальной информации о сотруднике с его отпусками и командировками
- Валидация email адресов
- Поддержка различных должностей и отделов

### Отпуска (Vacations)
- Создание заявок на отпуск
- Просмотр всех отпусков с фильтрацией по статусу
- Одобрение и отклонение отпусков
- Получение отпусков конкретного сотрудника

### Командировки (Business Trips)
- Создание заявок на командировку
- Управление статусами командировок (запланирована, в процессе, завершена)
- Отслеживание планируемых и фактических расходов
- Одобрение командировок

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите приложение:
```bash
python main.py
```

Или используя uvicorn напрямую:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Откройте браузер и перейдите по адресу:
- API документация (Swagger): http://localhost:8000/docs
- Альтернативная документация (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Сотрудники
- `POST /employees/` - Создать сотрудника
- `GET /employees/` - Получить список сотрудников
- `GET /employees/{employee_id}` - Получить сотрудника с деталями
- `PUT /employees/{employee_id}` - Обновить сотрудника
- `DELETE /employees/{employee_id}` - Удалить сотрудника

### Отпуска
- `POST /vacations/` - Создать заявку на отпуск
- `GET /vacations/` - Получить список отпусков
- `GET /vacations/{vacation_id}` - Получить отпуск
- `GET /employees/{employee_id}/vacations` - Получить отпуска сотрудника
- `PUT /vacations/{vacation_id}` - Обновить отпуск
- `POST /vacations/{vacation_id}/approve` - Одобрить отпуск
- `POST /vacations/{vacation_id}/reject` - Отклонить отпуск
- `DELETE /vacations/{vacation_id}` - Удалить отпуск

### Командировки
- `POST /business-trips/` - Создать заявку на командировку
- `GET /business-trips/` - Получить список командировок
- `GET /business-trips/{trip_id}` - Получить командировку
- `GET /employees/{employee_id}/business-trips` - Получить командировки сотрудника
- `PUT /business-trips/{trip_id}` - Обновить командировку
- `POST /business-trips/{trip_id}/approve` - Одобрить командировку
- `POST /business-trips/{trip_id}/complete` - Завершить командировку
- `DELETE /business-trips/{trip_id}` - Удалить командировку

## Модели данных

### Employee (Сотрудник)
- `first_name` - Имя
- `last_name` - Фамилия
- `email` - Email (уникальный)
- `position` - Должность (enum)
- `department` - Отдел
- `hire_date` - Дата найма
- `salary` - Зарплата (опционально)

### Vacation (Отпуск)
- `employee_id` - ID сотрудника
- `start_date` - Дата начала
- `end_date` - Дата окончания
- `reason` - Причина (опционально)
- `status` - Статус (pending, approved, rejected, cancelled)

### Business Trip (Командировка)
- `employee_id` - ID сотрудника
- `destination` - Место назначения
- `start_date` - Дата начала
- `end_date` - Дата окончания
- `purpose` - Цель командировки
- `estimated_cost` - Планируемые расходы
- `actual_cost` - Фактические расходы
- `status` - Статус (planned, in_progress, completed, cancelled)

## База данных

Приложение использует SQLite базу данных (`employees.db`), которая создается автоматически при первом запуске.

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер
- **SQLite** - база данных