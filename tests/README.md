# Модульные тесты для проекта "Исторические события"

## Описание

Этот подпроект содержит модульные тесты для всех компонентов системы обработки исторических событий.

## Структура

```
tests/
├── __init__.py              # Инициализация модуля тестов
├── conftest.py              # Конфигурация pytest
├── pytest.ini               # Настройки pytest
├── requirements.txt         # Зависимости для тестов
├── test_historical_event.py # Тесты для классов событий
├── test_container.py        # Тесты для контейнера
└── test_command_parser.py   # Тесты для парсера команд
```

## Установка

```bash
pip install -r tests/requirements.txt
```

## Запуск тестов

### Все тесты
```bash
pytest
```

### С покрытием кода
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Конкретный файл
```bash
pytest tests/test_historical_event.py
```

### Конкретный тест
```bash
pytest tests/test_historical_event.py::TestHistoricalEvent::test_init
```

## Результаты

Все 51 тест успешно проходят, покрывая:
- ✅ Создание объектов
- ✅ Все методы классов
- ✅ Успешные сценарии
- ✅ Исключительные ситуации
- ✅ Граничные случаи

