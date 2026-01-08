# Использование autopep8 в PowerShell

## Проблема

В PowerShell шаблон `*.py` не раскрывается автоматически, как в bash. Поэтому команда:
```bash
autopep8 --in-place --aggressive --aggressive *.py
```
не работает.

## Решения

### Вариант 1: Использовать Get-ChildItem (рекомендуется)

```powershell
Get-ChildItem -Filter *.py | ForEach-Object { 
    autopep8 --in-place --aggressive --aggressive $_.Name 
}
```

### Вариант 2: Указать файлы явно

```powershell
autopep8 --in-place --aggressive --aggressive main.py historical_event.py container.py command_parser.py
```

### Вариант 3: Использовать рекурсивный поиск

```powershell
Get-ChildItem -Recurse -Filter *.py | ForEach-Object { 
    autopep8 --in-place --aggressive --aggressive $_.FullName 
}
```

### Вариант 4: Создать скрипт

Создайте файл `fix_code.py`:
```python
import subprocess
import glob

for file in glob.glob("*.py"):
    subprocess.run(["autopep8", "--in-place", "--aggressive", "--aggressive", file])
```

Затем запустите:
```powershell
python fix_code.py
```

## Что делает autopep8

- Удаляет пробелы из пустых строк
- Исправляет отступы
- Добавляет/удаляет пробелы вокруг операторов
- Исправляет длину строк
- И другие стилистические исправления согласно PEP 8

## Флаги

- `--in-place` - изменяет файлы напрямую (без этого флага показывает, что изменится)
- `--aggressive` - более агрессивные исправления (можно использовать дважды)
- `--max-line-length=N` - максимальная длина строки (по умолчанию 79)

## Проверка перед применением

Чтобы увидеть, что будет изменено (без изменения файлов):

```powershell
Get-ChildItem -Filter *.py | ForEach-Object { 
    autopep8 --diff $_.Name 
}
```

## После применения autopep8

1. Проверьте изменения:
```powershell
git diff
```

2. Проверьте, что все исправлено:
```powershell
flake8 *.py
```

3. Если все хорошо, закоммитьте:
```powershell
git add .
git commit -m "Fix code style with autopep8"
```

