# Краткий мануал по переходу-функциональности

### Запуск ядра
- **БЫЛО** - ```python baseline.py core```
- **СТАЛО** - ```docker compose up -d --force-recreate``` (стартует при поднятии контейнера)

### Проверка статуса запущенности
- **БЫЛО** - ```ps aux``` или другой поиск процесса
- **СТАЛО** - ```docker compose ps``` 

### Ввод и запуск команд
- **БЫЛО** - ```python baseline.py <команда>```
- **СТАЛО** - для unix - ```./baseline <команда>```. для unix - ```docker-compose exec -iT baseline sh -c "python baseline.py <команда>"```