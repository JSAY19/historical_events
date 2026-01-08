"""
Модульные тесты для класса CommandParser.
"""

import pytest
import tempfile
import os
from command_parser import CommandParser
from container import EventContainer
from historical_event import Battle, Treaty


class TestCommandParser:
    """Тесты для класса CommandParser."""

    @pytest.fixture
    def container(self):
        """Фикстура для создания контейнера."""
        return EventContainer()

    @pytest.fixture
    def parser(self, container):
        """Фикстура для создания парсера."""
        return CommandParser(container)

    def test_init(self, container):
        """Тест инициализации парсера."""
        parser = CommandParser(container)
        assert parser.container == container

    def test_parse_add_command_battle_success(self, parser):
        """Тест успешного парсинга команды ADD для битвы."""
        result = parser.parse_add_command("ADD Битва|Куликовская битва|1380|Куликово поле")
        assert result is True
        assert len(parser.container._events) == 1
        assert isinstance(parser.container._events[0], Battle)
        assert parser.container._events[0].name == "Куликовская битва"

    def test_parse_add_command_treaty_success(self, parser):
        """Тест успешного парсинга команды ADD для договора."""
        result = parser.parse_add_command("ADD Договор|Версальский договор|1919|Германия и союзники")
        assert result is True
        assert len(parser.container._events) == 1
        assert isinstance(parser.container._events[0], Treaty)
        assert parser.container._events[0].name == "Версальский договор"

    def test_parse_add_command_invalid_format(self, parser, capsys):
        """Тест парсинга команды ADD с неверным форматом."""
        result = parser.parse_add_command("ADD Битва|Название|Дата")
        assert result is False
        assert len(parser.container._events) == 0
        captured = capsys.readouterr()
        assert "Неверный формат команды ADD" in captured.out

    def test_parse_add_command_unknown_type(self, parser, capsys):
        """Тест парсинга команды ADD с неизвестным типом."""
        result = parser.parse_add_command("ADD Неизвестный|Название|Дата|Параметр")
        assert result is False
        assert len(parser.container._events) == 0
        captured = capsys.readouterr()
        assert "Неизвестный тип события" in captured.out

    def test_parse_add_command_empty_line(self, parser, capsys):
        """Тест парсинга пустой команды ADD."""
        result = parser.parse_add_command("ADD ")
        assert result is False
        captured = capsys.readouterr()
        assert "Неверный формат команды ADD" in captured.out

    def test_parse_rem_command_by_type(self, parser):
        """Тест парсинга команды REM по типу."""
        battle = Battle("Битва 1", "1000", "Место 1")
        treaty = Treaty("Договор 1", "2000", "Стороны 1")
        parser.container.add(battle)
        parser.container.add(treaty)
        
        result = parser.parse_rem_command('REM type == "Битва"')
        assert result is True
        assert len(parser.container._events) == 1
        assert parser.container._events[0].type == "Договор"

    def test_parse_rem_command_by_name(self, parser):
        """Тест парсинга команды REM по названию."""
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM name == "Битва 1"')
        assert result is True
        assert len(parser.container._events) == 1
        assert parser.container._events[0].name == "Битва 2"

    def test_parse_rem_command_by_date(self, parser):
        """Тест парсинга команды REM по дате."""
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM date == "1000"')
        assert result is True
        assert len(parser.container._events) == 1

    def test_parse_rem_command_by_place(self, parser):
        """Тест парсинга команды REM по месту (для битв)."""
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM place == "Место 1"')
        assert result is True
        assert len(parser.container._events) == 1
        assert parser.container._events[0].place == "Место 2"

    def test_parse_rem_command_by_parties(self, parser):
        """Тест парсинга команды REM по сторонам (для договоров)."""
        treaty1 = Treaty("Договор 1", "2000", "Стороны 1")
        treaty2 = Treaty("Договор 2", "2100", "Стороны 2")
        parser.container.add(treaty1)
        parser.container.add(treaty2)
        
        result = parser.parse_rem_command('REM parties == "Стороны 1"')
        assert result is True
        assert len(parser.container._events) == 1

    def test_parse_rem_command_name_contains(self, parser):
        """Тест парсинга команды REM с условием contains."""
        battle1 = Battle("Куликовская битва", "1380", "Куликово поле")
        battle2 = Battle("Бородинское сражение", "1812", "Бородино")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM name contains "Куликов"')
        assert result is True
        assert len(parser.container._events) == 1
        assert "Бородинское" in parser.container._events[0].name

    def test_parse_rem_command_date_greater(self, parser):
        """Тест парсинга команды REM с условием date >."""
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1500", "Место 2")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM date > "1200"')
        assert result is True
        assert len(parser.container._events) == 1
        assert parser.container._events[0].date == "1000"

    def test_parse_rem_command_date_less(self, parser):
        """Тест парсинга команды REM с условием date <."""
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1500", "Место 2")
        parser.container.add(battle1)
        parser.container.add(battle2)
        
        result = parser.parse_rem_command('REM date < "1200"')
        assert result is True
        assert len(parser.container._events) == 1
        assert parser.container._events[0].date == "1500"

    def test_parse_rem_command_invalid_condition(self, parser, capsys):
        """Тест парсинга команды REM с неверным условием."""
        battle = Battle("Битва 1", "1000", "Место 1")
        parser.container.add(battle)
        
        result = parser.parse_rem_command('REM invalid condition')
        assert result is False
        captured = capsys.readouterr()
        assert "Ошибка при удалении событий" in captured.out

    def test_parse_condition_type_equality(self, parser):
        """Тест парсинга условия type ==."""
        condition = parser._parse_condition('type == "Битва"')
        battle = Battle("Битва", "1000", "Место")
        treaty = Treaty("Договор", "2000", "Стороны")
        assert condition(battle) is True
        assert condition(treaty) is False

    def test_parse_condition_name_equality(self, parser):
        """Тест парсинга условия name ==."""
        condition = parser._parse_condition('name == "Тест"')
        battle = Battle("Тест", "1000", "Место")
        battle2 = Battle("Другой", "1100", "Место")
        assert condition(battle) is True
        assert condition(battle2) is False

    def test_parse_condition_date_equality(self, parser):
        """Тест парсинга условия date ==."""
        condition = parser._parse_condition('date == "1000"')
        battle = Battle("Битва", "1000", "Место")
        battle2 = Battle("Битва", "1100", "Место")
        assert condition(battle) is True
        assert condition(battle2) is False

    def test_parse_condition_place_equality(self, parser):
        """Тест парсинга условия place ==."""
        condition = parser._parse_condition('place == "Место 1"')
        battle = Battle("Битва", "1000", "Место 1")
        battle2 = Battle("Битва", "1100", "Место 2")
        treaty = Treaty("Договор", "2000", "Стороны")
        assert condition(battle) is True
        assert condition(battle2) is False
        assert condition(treaty) is False  # Договоры не имеют place

    def test_parse_condition_parties_equality(self, parser):
        """Тест парсинга условия parties ==."""
        condition = parser._parse_condition('parties == "Стороны 1"')
        treaty = Treaty("Договор", "2000", "Стороны 1")
        treaty2 = Treaty("Договор", "2100", "Стороны 2")
        battle = Battle("Битва", "1000", "Место")
        assert condition(treaty) is True
        assert condition(treaty2) is False
        assert condition(battle) is False  # Битвы не имеют parties

    def test_parse_condition_name_contains(self, parser):
        """Тест парсинга условия name contains."""
        condition = parser._parse_condition('name contains "война"')
        battle1 = Battle("Первая мировая война", "1914", "Европа")
        battle2 = Battle("Куликовская битва", "1380", "Куликово поле")
        assert condition(battle1) is True
        assert condition(battle2) is False

    def test_parse_condition_date_greater(self, parser):
        """Тест парсинга условия date >."""
        condition = parser._parse_condition('date > "1500"')
        battle1 = Battle("Битва 1", "1000", "Место")
        battle2 = Battle("Битва 2", "1600", "Место")
        assert condition(battle1) is False
        assert condition(battle2) is True

    def test_parse_condition_date_less(self, parser):
        """Тест парсинга условия date <."""
        condition = parser._parse_condition('date < "1500"')
        battle1 = Battle("Битва 1", "1000", "Место")
        battle2 = Battle("Битва 2", "1600", "Место")
        assert condition(battle1) is True
        assert condition(battle2) is False

    def test_parse_condition_invalid(self, parser):
        """Тест парсинга неверного условия."""
        with pytest.raises(ValueError, match="Неизвестный формат условия"):
            parser._parse_condition("invalid condition")

    def test_process_file_success(self, parser, tmp_path):
        """Тест успешной обработки файла с командами."""
        test_file = tmp_path / "test_commands.txt"
        content = """ADD Битва|Куликовская битва|1380|Куликово поле
ADD Договор|Версальский договор|1919|Германия и союзники
PRINT
REM type == "Битва"
PRINT
"""
        test_file.write_text(content, encoding='utf-8')
        
        parser.process_file(str(test_file))
        assert len(parser.container._events) == 1
        assert isinstance(parser.container._events[0], Treaty)

    def test_process_file_not_found(self, parser, capsys):
        """Тест обработки несуществующего файла."""
        parser.process_file("несуществующий_файл.txt")
        captured = capsys.readouterr()
        assert "не найден" in captured.out

    def test_process_file_with_comments(self, parser, tmp_path):
        """Тест обработки файла с комментариями."""
        test_file = tmp_path / "test_commands.txt"
        content = """# Это комментарий
ADD Битва|Битва 1|1000|Место 1
# Еще комментарий
PRINT
"""
        test_file.write_text(content, encoding='utf-8')
        
        parser.process_file(str(test_file))
        assert len(parser.container._events) == 1

    def test_process_file_with_empty_lines(self, parser, tmp_path):
        """Тест обработки файла с пустыми строками."""
        test_file = tmp_path / "test_commands.txt"
        content = """ADD Битва|Битва 1|1000|Место 1

ADD Договор|Договор 1|2000|Стороны 1

PRINT
"""
        test_file.write_text(content, encoding='utf-8')
        
        parser.process_file(str(test_file))
        assert len(parser.container._events) == 2

    def test_process_file_unknown_command(self, parser, tmp_path, capsys):
        """Тест обработки файла с неизвестной командой."""
        test_file = tmp_path / "test_commands.txt"
        content = """ADD Битва|Битва 1|1000|Место 1
UNKNOWN COMMAND
PRINT
"""
        test_file.write_text(content, encoding='utf-8')
        
        parser.process_file(str(test_file))
        captured = capsys.readouterr()
        assert "Неизвестная команда" in captured.out

