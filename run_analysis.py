"""
Скрипт для автоматического запуска всех инструментов анализа кода.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, output_file=None):
    """Запускает команду и сохраняет результат в файл."""
    try:
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                f.write(f"Команда: {command}\n")
                f.write("=" * 80 + "\n\n")
                f.write("STDOUT:\n")
                f.write(result.stdout)
                f.write("\n\nSTDERR:\n")
                f.write(result.stderr)
                f.write(f"\n\nКод возврата: {result.returncode}\n")
            print(f"[OK] Результаты сохранены в {output_file}")
        else:
            result = subprocess.run(command, shell=True)
            return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении команды: {e}")
        return False
    return True

def main():
    """Главная функция для запуска анализа."""
    print("=" * 80)
    print("АНАЛИЗ КОДА ПРОЕКТА 'ИСТОРИЧЕСКИЕ СОБЫТИЯ'")
    print("=" * 80)
    
    # Создаем директорию для результатов
    results_dir = Path("analysis_results")
    results_dir.mkdir(exist_ok=True)
    
    python_files = ["main.py", "historical_event.py", "container.py", "command_parser.py"]
    
    print("\n1. Запуск pylint (линтинг)...")
    run_command(
        f"pylint {' '.join(python_files)} --output-format=text",
        results_dir / "pylint_report.txt"
    )
    
    print("\n2. Запуск flake8 (проверка стиля)...")
    run_command(
        f"flake8 {' '.join(python_files)} --max-line-length=100",
        results_dir / "flake8_report.txt"
    )
    
    print("\n3. Запуск mypy (проверка типов)...")
    run_command(
        f"mypy {' '.join(python_files)} --ignore-missing-imports",
        results_dir / "mypy_report.txt"
    )
    
    print("\n4. Запуск cProfile (профилирование производительности)...")
    if os.path.exists("commands.txt"):
        run_command(
            "python -m cProfile -s cumulative -o analysis_results/profile.prof main.py commands.txt",
            None
        )
        print("[OK] Профиль сохранен в analysis_results/profile.prof")
        print("  Для просмотра используйте: python -m pstats analysis_results/profile.prof")
    else:
        print("⚠ Файл commands.txt не найден, пропускаем профилирование")
    
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print(f"Результаты сохранены в директории: {results_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()

