# ВАЖНОЕ ОБНОВЛЕНИЕ
#### В полуфинальном этапе становится доступен параметр --nosology в команде start. Просьба повторно ознакомиться с файлами:
#### [Описание мех-ма работы с утилитой ДЛЯ LINUX/VMWARE](/docs/commands-native.md)
#### [Описание мех-ма работы с утилитой ДЛЯ WINDOWS](/docs/commands-native.md)
Команда start, параметр номер 6. И с файлом:
### [Словарь нозологий](/docs/nosology.md)

## Baseline участников
Пакет baseline представляет собой программный продукт (библиотеку, пакет) для взаимодействия участников с платформой.
## Baseline 2.0 - вторая версия консольной утилиты для платформы AIMED.
Увидеть все зависимости можно в файле `Pipfile`

## Требования для работы Baseline

-   [docker](https://docs.docker.com/get-docker/)
-   [docker compose](https://docs.docker.com/compose/install/) v2 +

## Развертывание и установка:
> При наличии ошибок всегда проверяйте наличие актуальной версии.

1) Заполнить поле TOKEN в файле tmp/creds.cfg 
2) Разворот и установка окружения
        ```shell script
    # Копируем файл настроек
    cp .env.example .env

    # Скачиваем актуальную версию образа
    docker compose pull

    # Поднимаем сервис
    docker compose up -d --force-recreate

    # Проверить что сервис поднят (в случае успеха вы должны увидеть Status в состоянии Up)
    docker compose ps
    ```

#### [Описание мех-ма работы с утилитой ДЛЯ LINUX/VMWARE](/docs/commands-native.md)
#### [Описание мех-ма работы с утилитой ДЛЯ WINDOWS](/docs/commands-native.md)
#### [Краткий справочник после перехода на Docker](/docs/migrate-docker.md)
#### [Краткий справочник после б1](/docs/migrate.md)