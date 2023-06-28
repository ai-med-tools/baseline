import dotenv
import os
from typing import Final
from pathlib import Path

path: Path = Path(__file__).parent.parent.parent
if 'BASELINE_ROOT_DIR' in os.environ:
    path: Path = Path(os.environ['BASELINE_ROOT_DIR'])
ROOT_DIR: Final[Path] = path

ENV_FILE_PATH: Final[Path] = ROOT_DIR.joinpath('.env')

dotenv.load_dotenv(ENV_FILE_PATH)

IS_DEBUG: Final[bool] = bool('DEBUG' in os.environ and bool(os.environ['DEBUG']))
CHECK_DIRECTORY_ANSWER: Final[bool] = bool('CHECK_DIRECTORY_ANSWER' in os.environ and bool(os.environ['CHECK_DIRECTORY_ANSWER'])) or 0
TOKEN: Final[str] = str('TOKEN' in os.environ and os.environ['TOKEN'])
DOWNLOAD_HOST: Final[str] = str('DOWNLOAD_HOST' in os.environ and os.environ['DOWNLOAD_HOST'])
SESSION_IS_ONLY_SAVE_FILES: Final[bool] = bool('SESSION_IS_ONLY_SAVE_FILES' in os.environ and bool(os.environ['SESSION_IS_ONLY_SAVE_FILES']))
AUTOMATIC_ANSWER_FILE_GENERATE: Final[bool] = bool('AUTOMATIC_ANSWER_FILE_GENERATE' in os.environ and bool(os.environ['AUTOMATIC_ANSWER_FILE_GENERATE']))
SESSION_WS_PROTOCOL_VERSION: Final[int] = int('SESSION_WS_PROTOCOL_VERSION' in os.environ and os.environ['SESSION_WS_PROTOCOL_VERSION']) or 2
CHECK_DIRECTORY_ANSWER_DELAY: Final[int] = int('CHECK_DIRECTORY_ANSWER_DELAY' in os.environ and os.environ['CHECK_DIRECTORY_ANSWER_DELAY']) or 0

DEBUG_MAX_MARKUP_DEMO_DELAY: Final[int] = int('DEBUG_MAX_MARKUP_DEMO_DELAY' in os.environ and os.environ['DEBUG_MAX_MARKUP_DEMO_DELAY'])
