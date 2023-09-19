# Краткий мануал по переходу-функциональности
### Старт сессии
- **БЫЛО** - ```python cli.py session start```
- **СТАЛО** - ```python baseline.py core``` 1 РАЗ ДЛЯ СТАРТА ДЕМОНА. ЗАТЕМ  ```python baseline.py start --contest=finder --stage=qualifying --type=training --count=10 --timeout=10```

### Конфигурация
- **БЫЛО** - файл .env
- **СТАЛО** - файл creds.cfg

### Отправка файла
- **БЫЛО** - интеграция в алгоритмы пайтон без возможности произвольной отправки
- **СТАЛО** - ```python baseline.py send --path=<path_to_solution_json>```

### Процесс
- **БЫЛО** - захватывает консоль
- **СТАЛО** - работает в демоне (daemon) и получает команды извне