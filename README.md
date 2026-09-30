# Лабораторная работа №8

Самодуров Матвей Николаевич, группа 221341, вариант 8, лабораторная №8.

Тема: экосистемы Python — Poetry, pytest, TDD, архитектура, ИИ-субагенты.

## Задания варианта

**Средняя сложность:**

- №4 — TDD для калькулятора (`lab8/calculator.py`)
- №8 — простой модуль с CLI на argparse (`lab8/cli.py`)
- №10 — описание архитектуры MVC (`docs/mvc.md`, пакет `lab8/mvc/`)

**Повышенная сложность:**

- №1 — мини-микросервис на FastAPI (`lab8/microservice.py`)
- №8 — интеграция с внешним ИИ API (`lab8/ai_client.py`)

## Клонирование

```bash
git clone https://github.com/kyomufs/mtp-lab8-variant8.git
cd mtp-lab8-variant8
```

## Запуск

Демо по всем заданиям (сервер НЕ запускается, печатаются
инструкции и быстрые примеры):

```bash
uv run python -m lab8
```

Примеры CLI (коды возврата: 0 — успех, 1 — неверное число,
2 — ошибка использования argparse):

```bash
uv run python -m lab8.cli add 2 3
uv run python -m lab8.cli sub 10 4
uv run python -m lab8.cli greet MTP
```

Микросервис запускается отдельной командой:

```bash
uv run --with fastapi --with uvicorn uvicorn lab8.microservice:app
curl http://127.0.0.1:8000/health
```

Ключ внешнего ИИ API берётся ТОЛЬКО из аргумента `api_key` или
из переменной окружения `OPENAI_API_KEY`; в репозитории ключей нет.

## Проверки

```bash
uv run --with pytest --with flake8 --with fastapi --with httpx pytest -q
uv run --with flake8 flake8 lab8 tests
```

Зависимости описаны в `pyproject.toml` (формат Poetry),
`requirements-dev.txt` — для CI, `setup.cfg` — конфиг flake8
(flake8 не читает `pyproject.toml`).

Подробное описание выполнения — в `docs/report.md`,
архитектура MVC — в `docs/mvc.md`.
