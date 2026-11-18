# Центр дополнительного образования — учебный FastAPI + PostgreSQL

**Предметная область:** приём заявок и управление учебными группами центра дополнительного образования детей, на основе модели из лабораторной по 1С.

- **FastAPI:** ровно 10 REST-операций, работающих с демонстрационными данными в памяти (словарями Python). **API не использует PostgreSQL.** Изменения сбрасываются при перезапуске приложения.
- **PostgreSQL:** отдельный контейнер и миграция SQL, создающая 5 связанных таблиц при первом запуске базы.

## Файлы

- `main.py` — 10 API-методов и Pydantic-модели.
- `migrations/001_create_tables.sql` — миграция с 5 таблицами.
- `compose.yaml` — API и PostgreSQL в Docker Compose.
- `Dockerfile` — сборка образа приложения.
- `requirements.txt` — Python-зависимости.
- `.env.example` — пример переменной окружения PostgreSQL.

## Запуск

Установите Docker Desktop с Docker Compose. В каталоге проекта выполните:

```bash
docker compose up --build -d
```

Откройте **http://localhost:8000/docs** — Swagger UI, где можно вызвать все 10 операций.

Проверка PostgreSQL:

```bash
docker compose exec db psql -U education_user -d education_center -c '\dt'
```

Остановка (данные PostgreSQL сохраняются в Docker volume):

```bash
docker compose down
```

**Важно:** скрипт `/docker-entrypoint-initdb.d/001_create_tables.sql` запускается только при **первой** инициализации пустого каталога данных PostgreSQL. При последующих изменениях SQL существующий volume не мигрируется автоматически. Для учебного сброса БД можно использовать `docker compose down -v` (это **удалит все данные базы**), затем `docker compose up --build -d`.

## 10 эндпоинтов

| № | Метод | URL | Действие |
|---|---|---|---|
| 1 | GET | `/programs` | Список программ |
| 2 | GET | `/programs/{program_id}` | Программа по ID |
| 3 | POST | `/programs` | Создание программы |
| 4 | PUT | `/programs/{program_id}` | Изменение программы |
| 5 | DELETE | `/programs/{program_id}` | Удаление программы |
| 6 | GET | `/groups` | Список учебных групп |
| 7 | GET | `/groups/{group_id}` | Учебная группа по ID |
| 8 | POST | `/applications` | Создание заявки |
| 9 | GET | `/applications/{application_id}` | Заявка по ID |
| 10 | DELETE | `/applications/{application_id}` | Удаление заявки |

Пример JSON для `POST /applications`:

```json
{
  "student_name": "Иванов Иван",
  "parent_name": "Иванова Мария",
  "program_id": 1
}
```

## Структура базы данных

1. `parents` — законные представители.
2. `students` — ученики, `parent_id → parents.id`.
3. `programs` — образовательные программы.
4. `study_groups` — учебные группы, `program_id → programs.id`.
5. `applications` — заявки со ссылками на родителя, ученика, программу и необязательную группу.

Модель БД упрощена до 5 таблиц в рамках задания. Расписание и история статусов, присутствовавшие в модели 1С, в этом варианте не вынесены в отдельные таблицы.

## Загрузка на GitHub

Создайте пустой репозиторий `education-center-api` на GitHub. Из каталога проекта:

```bash
git init
git add .
git commit -m "Initial FastAPI and PostgreSQL project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/education-center-api.git
git push -u origin main
```

Замените `YOUR_USERNAME` на своё имя пользователя GitHub. Не добавляйте в репозиторий реальные пароли или `.env`.
