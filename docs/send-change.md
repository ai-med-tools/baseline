### Имя файла
В Бейзлайн файл приходит в нейминге (пример) - ```82215_1_23098.xml```.
Где 82215 - внутренний ID, 1 - версия, 23098 - ID задачи.

## Отправка файла
- **БЫЛО** - ```./baseline send --path=<path_to_solution_json>```
- **СТАЛО** - ```./baseline send --path=<path_to_solution_json> --taskid=<ID_задачи>```

### Данная правка была сделана для облегчения привязки отправленного результата с определенной задаче, чтобы участнику было гарантировано, что результат будет привязан именно к желаемой задаче.

### Извлекать ID задачи из имени присланного файла участник должен самостоятельно.