import sys
from baseline.tools.constants import LOGS_DIR, IS_DEBUG


def logger_configure():
    # init base logger config
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": "DEBUG" if IS_DEBUG else "INFO",
                "format": "<green>{time}</green>  |  <level>{level}</level>  | <level>{message}</level>",
                "colorize": True
            },
            {
                "sink": LOGS_DIR.joinpath('info_{time:YYYY.MM.DD}.log'),
                "level": "INFO",
                "format": "{time}  |  {level}  | {message}"
            },
            {
                "sink": LOGS_DIR.joinpath('sessions_{time:YYYY.MM.DD}.log'),
                "filter": lambda record: record["extra"].get('session') is not None,
                "format": "{time}: {message} {extra}"
            },
        ],
    }

    if IS_DEBUG:
        config['handlers'].append({
            "sink": LOGS_DIR.joinpath('debug_{time:YYYY.MM.DD}.log'),
            "serialize": True,
            "backtrace": True,
            "level": "DEBUG"
        })

    from loguru import logger
    logger.configure(**config)
