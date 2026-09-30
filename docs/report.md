# Отчёт по лабораторной работе №8

Самодуров Матвей Николаевич, группа 221341, вариант 8.

Тема: экосистемы Python — Poetry, pytest, TDD, архитектура,
ИИ-субагенты.

## Средняя сложность

- **№4 Реализовать TDD для калькулятора** — `lab8/calculator.py`:
  четыре функции `add` / `sub` / `mul` / `div` с аннотациями
  `float | int`; `div` проверяет нулевой делитель и бросает
  `ZeroDivisionError`. Доказательство TDD — история коммитов:
  сначала `test: add calculator tests for TDD red phase`
  (только тесты, тесты падают), затем
  `feat: implement calculator to pass tests` (код, тесты зелёные);
  подробнее — раздел «TDD-цикл».
- **№8 Написать простой модуль с CLI argparse** — `lab8/cli.py`:
  подкоманды `add A B`, `sub A B`, `greet NAME`; функция
  `main(argv: list[str] | None = None) -> int` не вызывает
  `sys.exit` сама, а возвращает код: 0 — успех, 2 — ошибки
  использования argparse (его значение по умолчанию), 1 —
  операнды не числа (сообщение в stderr). Тесты вызывают
  `main([...])` напрямую (без subprocess) и проверяют коды
  возврата и stdout/stderr через `io.StringIO` c
  `redirect_stdout` / `redirect_stderr`.
- **№10 Описать архитектуру MVC** — `docs/mvc.md` + пакет
  `lab8/mvc/`: `model.py` (`TaskStore` со списком задач),
  `view.py` (функция `render_tasks` возвращает строку),
  `controller.py` (`handle_add` / `handle_complete` используют
  model и view). Поток «add → render» покрыт тестом
  `tests/test_mvc.py`.

## Повышенная сложность

- **№1 Реализовать мини-микросервис (FastAPI)** —
  `lab8/microservice.py`: `app = FastAPI(...)`, маршруты
  `GET /health` → `{"status": "ok"}`, `GET /items`,
  `POST /items` (Pydantic-схема `Item`: `name`, `price` c
  `ge=0`, `in_stock`), `GET /items/{item_id}` → 404 для
  отсутствующего элемента. Хранилище in-memory,
  `reset_items()` изолирует тесты; тесты — `TestClient` (httpx).
- **№8 Интегрировать внешний ИИ API** — `lab8/ai_client.py`:
  класс `AIClient(model="gpt-4o-mini", api_key=None,
  transport=None)` с методом `complete(prompt) -> str`.
  Транспорт по умолчанию (`http_transport`) делает POST через
  `urllib.request` на
  `https://api.openai.com/v1/chat/completions` с заголовком
  `Authorization: Bearer <key>`; ключ берётся ТОЛЬКО из
  параметра `api_key` или переменной окружения
  `OPENAI_API_KEY` (ключей в репозитории нет), без ключа
  конструктор бросает `RuntimeError`. Тесты подменяют
  `transport` фейковой функцией (проверка URL, ключа, payload и
  парсинга ответа), отдельно проверяется `urlopen` с
  `monkeypatch` (метод POST, URL, заголовок) и отсутствие ключа.

## TDD-цикл (red → green → refactor)

Цикл доказан историей коммитов:

1. **red** — коммит `test: add calculator tests for TDD red
   phase`: в репозитории только `tests/test_calculator.py`,
   модуля ещё нет. Реальный вывод `pytest -q` на этом состоянии:

```text
==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_calculator.py ___________________
ImportError while importing test module '/home/kyomufs/Desktop/mtp/lab8/mtp-lab8-variant8/tests/test_calculator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../../.local/share/uv/python/cpython-3.14.6-linux-x86_64-gnu/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_calculator.py:10: in <module>
    from lab8.calculator import add, div, mul, sub
E   ModuleNotFoundError: No module named 'lab8.calculator'
=========================== short test summary info ============================
ERROR tests/test_calculator.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.07s
```

2. **green** — коммит `feat: implement calculator to pass
   tests`: добавлен `lab8/calculator.py`, все тесты проходят.
   Реальный вывод `pytest -q` после этого коммита:

```text
......                                                                   [100%]
6 passed in 0.01s
```

3. **refactor** — публичный оставшийся интерфейс мал: четыре
   функции с точными докстрингами и аннотациями, без
   дублирования; код стиля flake8 (79 колонок) не менялся.

## Экосистема Poetry и pytest

- `pyproject.toml` в формате Poetry: `[tool.poetry]` (name
  `mtp-lab8-variant8`, version `1.0.0`, authors), зависимости
  `python ^3.12`, `fastapi`, `pydantic`, группа dev — `pytest`,
  `flake8`, `httpx`; таблица `[tool.pytest.ini_options]` с
  `testpaths = ["tests"]`.
- `setup.cfg` — конфиг flake8 (`max-line-length = 79`): flake8
  не читает `pyproject.toml`, поэтому конфиг вынесен отдельно.
- `requirements-dev.txt` — те же пакеты для CI (`pip install -r
  requirements-dev.txt`), workflow гоняет flake8 и `pytest -q`
  на Python 3.12 и 3.13 (matrix).
- Локальные команды (python3 в PATH нет, всё через `uv`):

```bash
uv run --with pytest --with flake8 --with fastapi --with httpx pytest -q
uv run --with flake8 flake8 lab8 tests
uv run python -m lab8
```

## Проверки

Реальный вывод команд (снимок на дату выполнения отчёта).

Тесты, все задания:

```text
$ uv run --with pytest --with flake8 --with fastapi --with httpx pytest -q
................................                                         [100%]
32 passed in 0.25s
```

Стиль кода (flake8 молчит, поэтому показан код возврата):

```text
$ uv run --with flake8 flake8 lab8 tests; echo "flake8 exit code: $?"
flake8 exit code: 0
```

История коммитов на момент написания отчёта (снимок на дату;
позже добавляются коммит CI-workflow, merge feature-ветки и тег
`v1.0.0`):

```text
10c8bfc feat: add demo entry point
4eb93e5 feat: add AI client with pluggable transport
7eb4357 feat: add FastAPI mini microservice
0cf73ae feat: add MVC architecture example package
7a0d846 feat: add argparse CLI module
5547d75 feat: implement calculator to pass tests
2f28c50 test: add calculator tests for TDD red phase
b5aff47 docs: create initial project skeleton
```
