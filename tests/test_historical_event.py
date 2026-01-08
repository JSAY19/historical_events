"""
Модульные тесты для класса HistoricalEvent и его наследников.
"""

import pytest
from historical_event import HistoricalEvent, Battle, Treaty


class TestHistoricalEvent:
    """Тесты для базового класса HistoricalEvent."""

    def test_init(self):
        """Тест успешного создания события."""
        event = HistoricalEvent("Тестовое событие", "2024")
        assert event.name == "Тестовое событие"
        assert event.date == "2024"

    def test_str(self):
        """Тест строкового представления события."""
        event = HistoricalEvent("Тестовое событие", "2024")
        result = str(event)
        assert "Тестовое событие" in result
        assert "2024" in result

    def test_repr(self):
        """Тест представления для отладки."""
        event = HistoricalEvent("Тестовое событие", "2024")
        result = repr(event)
        assert "HistoricalEvent" in result
        assert "Тестовое событие" in result
        assert "2024" in result


class TestBattle:
    """Тесты для класса Battle."""

    def test_init(self):
        """Тест успешного создания битвы."""
        battle = Battle("Куликовская битва", "1380", "Куликово поле")
        assert battle.name == "Куликовская битва"
        assert battle.date == "1380"
        assert battle.place == "Куликово поле"
        assert battle.type == "Битва"

    def test_inheritance(self):
        """Тест наследования от HistoricalEvent."""
        battle = Battle("Битва", "1000", "Место")
        assert isinstance(battle, HistoricalEvent)

    def test_str(self):
        """Тест строкового представления битвы."""
        battle = Battle("Куликовская битва", "1380", "Куликово поле")
        result = str(battle)
        assert "Битва" in result
        assert "Куликовская битва" in result
        assert "1380" in result
        assert "Куликово поле" in result

    def test_repr(self):
        """Тест представления для отладки."""
        battle = Battle("Куликовская битва", "1380", "Куликово поле")
        result = repr(battle)
        assert "Battle" in result
        assert "Куликовская битва" in result
        assert "1380" in result
        assert "Куликово поле" in result


class TestTreaty:
    """Тесты для класса Treaty."""

    def test_init(self):
        """Тест успешного создания договора."""
        treaty = Treaty("Версальский договор", "1919", "Германия и союзники")
        assert treaty.name == "Версальский договор"
        assert treaty.date == "1919"
        assert treaty.parties == "Германия и союзники"
        assert treaty.type == "Договор"

    def test_inheritance(self):
        """Тест наследования от HistoricalEvent."""
        treaty = Treaty("Договор", "1000", "Стороны")
        assert isinstance(treaty, HistoricalEvent)

    def test_str(self):
        """Тест строкового представления договора."""
        treaty = Treaty("Версальский договор", "1919", "Германия и союзники")
        result = str(treaty)
        assert "Договор" in result
        assert "Версальский договор" in result
        assert "1919" in result
        assert "Германия и союзники" in result

    def test_repr(self):
        """Тест представления для отладки."""
        treaty = Treaty("Версальский договор", "1919", "Германия и союзники")
        result = repr(treaty)
        assert "Treaty" in result
        assert "Версальский договор" in result
        assert "1919" in result
        assert "Германия и союзники" in result

