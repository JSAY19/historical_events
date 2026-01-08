"""
Модуль для работы с контейнером исторических событий.
"""

from typing import List, Callable
from historical_event import HistoricalEvent


class EventContainer:
    """Контейнер для хранения исторических событий."""

    def __init__(self):
        """Инициализация пустого контейнера."""
        self._events: List[HistoricalEvent] = []

    def add(self, event: HistoricalEvent) -> None:
        """
        Добавить событие в контейнер.

        Args:
            event: Историческое событие для добавления
        """
        self._events.append(event)

    def remove(self, condition: Callable[[HistoricalEvent], bool]) -> int:
        """
        Удалить события, соответствующие условию.

        Args:
            condition: Функция-условие для проверки событий

        Returns:
            Количество удаленных событий
        """
        initial_count = len(self._events)
        self._events = [
            event for event in self._events if not condition(event)]
        removed_count = initial_count - len(self._events)
        return removed_count

    def print_all(self) -> None:
        """Вывести все события на экран."""
        if not self._events:
            print("Контейнер пуст.")
            return

        print(f"\nВсего событий в контейнере: {len(self._events)}")
        print("=" * 60)
        for i, event in enumerate(self._events, 1):
            print(f"{i}. {event}")
        print("=" * 60)
