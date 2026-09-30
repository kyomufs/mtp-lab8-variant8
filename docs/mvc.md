# Архитектура MVC (задание №10, средняя сложность)

Модель MVC (Model — View — Controller) разделяет приложение на
три слоя, которые общаются только в одну сторону: Controller
управляет Model и просит View отрисовать результат.

## Кто что делает

- **Model** (`lab8/mvc/model.py`) — данные и правила хранения.
  Класс `TaskStore` хранит список задач (`Task`), умеет
  добавлять задачу (`add`) и помечать её выполненной
  (`complete`). Не знает ничего ни о текстовом выводе, ни о
  пользователе.
- **View** (`lab8/mvc/view.py`) — отображение. Функция
  `render_tasks` берёт готовые данные (`Sequence[Task]`) и
  возвращает строку-чеклист. Не меняет данные и не принимает
  решений — только рисует.
- **Controller** (`lab8/mvc/controller.py`) — координация.
  `handle_add` / `handle_complete` принимают запрос, просят
  Model изменить состояние, затем передают новые данные в View
  и возвращают готовый текст наверх.

## Как данные текут

1. Вызов (CLI-команда, тест, HTTP-обработчик) обращается к
   Controller: `handle_add(store, "write report")`.
2. Controller вызывает Model: `store.add("write report")` —
   состояние обновилось.
3. Controller читает актуальные данные: `store.tasks()`.
4. Controller передаёт данные в View: `render_tasks(tasks)`.
5. View возвращает строку, Controller возвращает её вызывающему
   — Model и View друг о друге не знают.

Ошибки Model (например, `IndexError` при несуществующем номере
задачи) Controller не прячет, а пробрасывает — вызывающий
решает, что делать.

## Схема

```
        вызов (CLI / тесты / HTTP)
                  |
                  v
        +-----------------+
        |   Controller    |
        | handle_add()    |
        | handle_complete |
        +---+---------+---+
            |         ^
 1. add /   |         | 4. str: "1. [ ] write report"
    complete|         |
            v         |
        +---------+   | 3. render_tasks(tasks)
        |  Model  |   |
        | TaskStore|  |
        +----+----+   |
            |         |
            | 2. list[Task]
            v         |
        +---------+   |
        |  View   | --+
        | render_tasks()
        +---------+
```

## Минимальный рабочий пример

```python
from lab8.mvc import TaskStore, handle_add, handle_complete

store = TaskStore()
print(handle_add(store, "write report"))
# 1. [ ] write report
print(handle_complete(store, 1))
# 1. [x] write report
```

Поток «add → render» покрыт тестом
`tests/test_mvc.py::test_add_then_render_contains_title`.
