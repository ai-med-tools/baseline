# ВАЖНО
Для коллег на WINDOWS, ранее запускавших команды через python baseline.py - теперь необходимо использовать обращение 
```docker-compose exec -iT baseline sh -c "python baseline.py <команда>"```. Также команда ```python baseline.py core``` теперь выполняется АВТОМАТИЧЕСКИ при старте контейнера. Дополнительно её вызывать НЕ НУЖНО.

# Документация по доступным командам
- ```docker-compose exec -iT baseline sh -c "python baseline.py check"``` - проверка состояния утилиты. при запуске проверит, запущена ли и ответит в консоль. Пример ответа -
***Baseline process is now started. PID - 249194
Current INPUT queue state - 0
Current OUTPUT queue state - 0***
- ```docker-compose exec -iT baseline sh -c "python baseline.py kill"``` - поиск и завершение процесса core.py. Закроет соединение с платформой и отключит сам процесс от внутренней очереди.# Документация по доступным командам
### Если утилита стартовала корректно

- ```docker-compose exec -iT baseline sh -c "python baseline.py start --contest=doctor --stage=semifinal --type=training --count=10 --timeout=10 --nosology=1,2"```

Список параметров - 
1) ***contest*** - вид конкурса. возможные значения - **finder** / **doctor**
2) ***stage*** - этап конкурса. возможные значения - **qualifying** / **semifinal** / **final**
3) ***type*** - тип проводимой сессиии. возможные значения - **training** (тренировка) / **algorithmic** (алгоритмическая) / **challenge** (испытание)/ **estimated-training** (расчётно-тренировочная)
4) ***count*** - количество запрашиваемых файлов. ОПЦИОНАЛЬНЫЙ. ранжируется в пределах от 1 до 2000. При значении count > 2000 будет показана ошибка. Используется ТОЛЬКО в тренировочных (--type=training) сессиях.
5) ***timeout*** - таймаут. Промежуток времени между отправлением файлов с платформы. ОПЦИОНАЛЬНЫЙ. ранжируется в пределах от 10 до 30 секунд
6) ***nosology*** - ID нозологии. Указывается через запятую без пробелов - 1,2,3,4,5,6 . Подробная информация здесь - 
#### [Словарь нозологий](/docs/nosology.md)
- ```docker-compose exec -iT baseline sh -c "python baseline.py send --path=<path_to_solution_json> --taskid=<ID_задачи>"``` - команда отправит на платформу решение в формате JSON. Пример указания пути - ```python baseline.py send --path=files/answer.json```. **ВАЖНО** - путь нужно указывать от корня ***baseline*** без точки в начале.
- ```docker-compose exec -iT baseline sh -c "python baseline.py abort"``` - сигнал прерывания сессии со стороны клиента. запущенная ранее сессия будет прервана с соответствующими отметками. 
### Если утилита стартовала некорректно
- ```docker-compose exec -iT baseline sh -c "python baseline.py flush"``` - чистка внутренней очереди команд. Далее снова попытаться выполнить start.


## Для финальных сессий
На финальной сессии конкурса I'm doctor необходимо в ходе обмена запрашивать дополнительные фрагменты эпикриза с исследованиями. Это делается командой
- ```docker-compose exec -iT baseline sh -c "python baseline.py test --test_id=<id_исследования> --description=<обоснование_запроса_исследования_в_кавычках> --hypotheses=<массив_с_предполагаемыми_id_диагноза>"```
Для параметров запуска этой команды есть отдельный md файл 
#### [Описание параметров команды ./baseline test](/docs/final-params.md)