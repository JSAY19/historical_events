"""
Главный файл программы для обработки исторических событий.
Программа обрабатывает файл с командами ADD, REM, PRINT.
"""

import sys
from container import EventContainer
from command_parser import CommandParser


def main():
    """Главная функция программы."""
    if len(sys.argv) < 2:
        print("Использование: python main.py <имя_файла>")
        print("Пример: python main.py commands.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Создаем контейнер и парсер
    container = EventContainer()
    parser = CommandParser(container)
    
    # Обрабатываем файл с командами
    print(f"Обработка файла: {filename}")
    print("-" * 60)
    parser.process_file(filename)
    print("-" * 60)
    print("Обработка завершена.")


if __name__ == "__main__":
    main()

