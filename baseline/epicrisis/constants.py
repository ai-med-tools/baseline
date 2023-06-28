from pathlib import Path
from typing import Final
from baseline.tools.constants import ROOT_DIR

FILES_ROOT_DIR: Final[Path] = Path().joinpath(ROOT_DIR, 'files')

FILES_SESSION_DIR: Final[Path] = Path().joinpath(FILES_ROOT_DIR, 'sessions')
FILES_CUSTOM_DIR: Final[Path] = Path().joinpath(FILES_ROOT_DIR, 'custom')
