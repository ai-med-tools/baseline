from pathlib import Path
from typing import Final, Literal
from .env_config import ROOT_DIR, IS_DEBUG, SESSION_IS_ONLY_SAVE_FILES, SESSION_WS_PROTOCOL_VERSION

FILES_DIR: Final[Path] = ROOT_DIR.joinpath('files')
LOGS_DIR: Final[Path] = ROOT_DIR.joinpath('logs')

# types
SessionMainType: Final = Literal['training', 'algorithmic', 'challenge', 'estimated-training']
SessionContestType: Final = Literal['doctor', 'finder']
SessionStageType: Final = Literal['qualifying', 'semifinal', 'final']
SessionDatasetType: Final = Literal['train', 'test']
