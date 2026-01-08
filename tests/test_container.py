"""
Модульные тесты для класса EventContainer.
"""

import pytest
from container import EventContainer
from historical_event import HistoricalEvent, Battle, Treaty


class TestEventContainer:
    """Тесты для класса EventContainer."""

    def test_init(self):
        """Тест инициализации пустого контейнера."""
        container = EventContainer()
        assert len(container._events) == 0

    def test_add_battle(self):
        """Тест добавления битвы в контейнер."""
        container = EventContainer()
        battle = Battle("Куликовская битва", "1380", "Куликово поле")
        container.add(battle)
        assert len(container._events) == 1
        assert container._events[0] == battle

    def test_add_treaty(self):
        """Тест добавления договора в контейнер."""
        container = EventContainer()
        treaty = Treaty("Версальский договор", "1919", "Германия и союзники")
        container.add(treaty)
        assert len(container._events) == 1
        assert container._events[0] == treaty

    def test_add_multiple_events(self):
        """Тест добавления нескольких событий."""
        container = EventContainer()
        battle = Battle("Битва 1", "1000", "Место 1")
        treaty = Treaty("Договор 1", "2000", "Стороны 1")
        container.add(battle)
        container.add(treaty)
        assert len(container._events) == 2

    def test_remove_by_type(self):
        """Тест удаления событий по типу."""
        container = EventContainer()
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        treaty = Treaty("Договор 1", "2000", "Стороны 1")
        container.add(battle1)
        container.add(battle2)
        container.add(treaty)
        
        removed = container.remove(lambda e: e.type == "Битва")
        assert removed == 2
        assert len(container._events) == 1
        assert container._events[0] == treaty

    def test_remove_by_name(self):
        """Тест удаления события по названию."""
        container = EventContainer()
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        container.add(battle1)
        container.add(battle2)
        
        removed = container.remove(lambda e: e.name == "Битва 1")
        assert removed == 1
        assert len(container._events) == 1
        assert container._events[0].name == "Битва 2"

    def test_remove_by_date(self):
        """Тест удаления событий по дате."""
        container = EventContainer()
        battle1 = Battle("Битва 1", "1000", "Место 1")
        battle2 = Battle("Битва 2", "1100", "Место 2")
        container.add(battle1)
        container.add(battle2)
        
        removed = container.remove(lambda e: e.date < "1050")
        assert removed == 1
        assert len(container._events) == 1
        assert container._events[0].date == "1100"

    def test_remove_none(self):
        """Тест удаления при отсутствии подходящих событий."""
        container = EventContainer()
        battle = Battle("Битва 1", "1000", "Место 1")
        container.add(battle)
        
        removed = container.remove(lambda e: e.name == "Несуществующее")
        assert removed == 0
        assert len(container._events) == 1

    def test_remove_from_empty(self):
        """Тест удаления из пустого контейнера."""
        container = EventContainer()
        removed = container.remove(lambda e: True)
        assert removed == 0

    def test_print_all_empty(self, capsys):
        """Тест вывода пустого контейнера."""
        container = EventContainer()
        container.print_all()
        captured = capsys.readouterr()
        assert "Контейнер пуст" in captured.out

    def test_print_all_with_events(self, capsys):
        """Тест вывода контейнера с событиями."""
        container = EventContainer()
        battle = Battle("Битва 1", "1000", "Место 1")
        treaty = Treaty("Договор 1", "2000", "Стороны 1")
        container.add(battle)
        container.add(treaty)
        
        container.print_all()
        captured = capsys.readouterr()
        assert "Всего событий в контейнере: 2" in captured.out
        assert "Битва 1" in captured.out
        assert "Договор 1" in captured.out

