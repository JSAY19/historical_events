"""
Модуль для парсинга и обработки команд из файла.
"""

import re
from typing import Callable
from historical_event import HistoricalEvent, Battle, Treaty
from container import EventContainer


class CommandParser:
    """Парсер команд для обработки файла с командами."""
    
    def __init__(self, container: EventContainer):
        """
        Инициализация парсера.
        
        Args:
            container: Контейнер для хранения событий
        """
        self.container = container
    
    def parse_add_command(self, line: str) -> bool:
        """
        Парсинг команды ADD.
        Формат: ADD <тип>|<название>|<дата>|<специфичный_параметр>
        Примеры:
        ADD Битва|Куликовская битва|1380|Куликово поле
        ADD Договор|Версальский договор|1919|Германия и союзники
        
        Args:
            line: Строка с командой ADD
            
        Returns:
            True если команда успешно обработана, False иначе
        """
        # Убираем "ADD " из начала строки
        data = line[4:].strip()
        
        # Разделяем по символу |
        parts = [part.strip() for part in data.split('|')]
        
        if len(parts) < 4:
            print(f"Ошибка: Неверный формат команды ADD: {line}")
            return False
        
        event_type = parts[0]
        name = parts[1]
        date = parts[2]
        specific_param = parts[3]
        
        try:
            if event_type == "Битва":
                event = Battle(name, date, specific_param)
            elif event_type == "Договор":
                event = Treaty(name, date, specific_param)
            else:
                print(f"Ошибка: Неизвестный тип события: {event_type}")
                return False
            
            self.container.add(event)
            print(f"Добавлено событие: {event}")
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении события: {e}")
            return False
    
    def parse_rem_command(self, line: str) -> bool:
        """
        Парсинг команды REM.
        Формат условий:
        - type == "Битва" или type == "Договор"
        - name == "<название>"
        - date == "<дата>"
        - place == "<место>" (только для битв)
        - parties == "<стороны>" (только для договоров)
        - name contains "<подстрока>"
        - date > "<дата>" или date < "<дата>" (лексикографическое сравнение)
        
        Примеры:
        REM type == "Битва"
        REM name == "Куликовская битва"
        REM date > "1500"
        REM name contains "война"
        
        Args:
            line: Строка с командой REM
            
        Returns:
            True если команда успешно обработана, False иначе
        """
        # Убираем "REM " из начала строки
        condition_str = line[4:].strip()
        
        try:
            condition = self._parse_condition(condition_str)
            removed_count = self.container.remove(condition)
            print(f"Удалено событий: {removed_count}")
            return True
            
        except Exception as e:
            print(f"Ошибка при удалении событий: {e}")
            return False
    
    def _parse_condition(self, condition_str: str) -> Callable[[HistoricalEvent], bool]:
        """
        Парсинг условия в функцию-предикат.
        
        Args:
            condition_str: Строка с условием
            
        Returns:
            Функция-предикат для проверки события
        """
        # Удаляем кавычки из строки условия для упрощения парсинга
        condition_str = condition_str.strip()
        
        # Проверка на равенство типа
        if re.match(r'type\s*==\s*"([^"]+)"', condition_str):
            match = re.match(r'type\s*==\s*"([^"]+)"', condition_str)
            target_type = match.group(1)
            return lambda e: hasattr(e, 'type') and e.type == target_type
        
        # Проверка на равенство названия
        if re.match(r'name\s*==\s*"([^"]+)"', condition_str):
            match = re.match(r'name\s*==\s*"([^"]+)"', condition_str)
            target_name = match.group(1)
            return lambda e: e.name == target_name
        
        # Проверка на равенство даты
        if re.match(r'date\s*==\s*"([^"]+)"', condition_str):
            match = re.match(r'date\s*==\s*"([^"]+)"', condition_str)
            target_date = match.group(1)
            return lambda e: e.date == target_date
        
        # Проверка на равенство места (для битв)
        if re.match(r'place\s*==\s*"([^"]+)"', condition_str):
            match = re.match(r'place\s*==\s*"([^"]+)"', condition_str)
            target_place = match.group(1)
            return lambda e: isinstance(e, Battle) and e.place == target_place
        
        # Проверка на равенство сторон (для договоров)
        if re.match(r'parties\s*==\s*"([^"]+)"', condition_str):
            match = re.match(r'parties\s*==\s*"([^"]+)"', condition_str)
            target_parties = match.group(1)
            return lambda e: isinstance(e, Treaty) and e.parties == target_parties
        
        # Проверка на вхождение подстроки в название
        if re.match(r'name\s+contains\s+"([^"]+)"', condition_str):
            match = re.match(r'name\s+contains\s+"([^"]+)"', condition_str)
            substring = match.group(1)
            return lambda e: substring.lower() in e.name.lower()
        
        # Проверка на сравнение дат (лексикографическое)
        if re.match(r'date\s*>\s*"([^"]+)"', condition_str):
            match = re.match(r'date\s*>\s*"([^"]+)"', condition_str)
            target_date = match.group(1)
            return lambda e: e.date > target_date
        
        if re.match(r'date\s*<\s*"([^"]+)"', condition_str):
            match = re.match(r'date\s*<\s*"([^"]+)"', condition_str)
            target_date = match.group(1)
            return lambda e: e.date < target_date
        
        # Если условие не распознано, выбрасываем исключение
        raise ValueError(f"Неизвестный формат условия: {condition_str}")
    
    def process_file(self, filename: str) -> None:
        """
        Обработка файла с командами.
        
        Args:
            filename: Имя файла с командами
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Пропускаем пустые строки и комментарии
                    if not line or line.startswith('#'):
                        continue
                    
                    # Обработка команды ADD
                    if line.startswith('ADD '):
                        self.parse_add_command(line)
                    
                    # Обработка команды REM
                    elif line.startswith('REM '):
                        self.parse_rem_command(line)
                    
                    # Обработка команды PRINT
                    elif line == 'PRINT':
                        self.container.print_all()
                    
                    else:
                        print(f"Строка {line_num}: Неизвестная команда: {line}")
                        
        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден.")
        except Exception as e:
            print(f"Ошибка при обработке файла: {e}")

