"""
Модуль для работы с историческими событиями.
Базовый класс и производные классы для битв и договоров.
"""


class HistoricalEvent:
    """Базовый класс для исторических событий."""

    def __init__(self, name: str, date: str):
        """
        Инициализация исторического события.

        Args:
            name: Название события
            date: Дата события
        """
        self.name = name
        self.date = date

    def __str__(self) -> str:
        """Строковое представление события."""
        return f"Название: {self.name}, Дата: {self.date}"

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"HistoricalEvent(name='{self.name}', date='{self.date}')"


class Battle(HistoricalEvent):
    """Класс для битв."""

    def __init__(self, name: str, date: str, place: str):
        """
        Инициализация битвы.

        Args:
            name: Название битвы
            date: Дата битвы
            place: Место битвы
        """
        super().__init__(name, date)
        self.place = place
        self.type = "Битва"

    def __str__(self) -> str:
        """Строковое представление битвы."""
        return f"{self.type}: {self.name}, Дата: {self.date}, Место: {self.place}"

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Battle(name='{self.name}', date='{self.date}', place='{self.place}')"


class Treaty(HistoricalEvent):
    """Класс для договоров."""

    def __init__(self, name: str, date: str, parties: str):
        """
        Инициализация договора.

        Args:
            name: Название договора
            date: Дата договора
            parties: Стороны договора
        """
        super().__init__(name, date)
        self.parties = parties
        self.type = "Договор"

    def __str__(self) -> str:
        """Строковое представление договора."""
        return f"{self.type}: {self.name}, Дата: {self.date}, Стороны: {self.parties}"

    def __repr__(self) -> str:
        """Представление для отладки."""
        return f"Treaty(name='{self.name}', date='{self.date}', parties='{self.parties}')"
