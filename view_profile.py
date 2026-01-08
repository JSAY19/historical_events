"""
Скрипт для просмотра результатов профилирования.
"""

import pstats
from pathlib import Path


def view_profile(profile_file="analysis_results/profile.prof", num_stats=20):
    """Выводит статистику профилирования."""
    if not Path(profile_file).exists():
        print(f"Файл профиля {profile_file} не найден!")
        return

    stats = pstats.Stats(profile_file)

    print("=" * 80)
    print("СТАТИСТИКА ПРОФИЛИРОВАНИЯ")
    print("=" * 80)
    print(f"\nВсего функций: {stats.total_calls}")
    print(f"Время выполнения: {stats.total_tt:.4f} секунд")

    print("\n" + "=" * 80)
    print("ТОП функций по времени выполнения (cumulative):")
    print("=" * 80)
    stats.sort_stats('cumulative')
    stats.print_stats(num_stats)

    print("\n" + "=" * 80)
    print("ТОП функций по собственному времени:")
    print("=" * 80)
    stats.sort_stats('tottime')
    stats.print_stats(num_stats)


if __name__ == "__main__":
    view_profile()
