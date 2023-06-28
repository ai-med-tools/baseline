from pydantic import dataclasses, Field
from typing import Optional

from baseline.tools.constants import SessionContestType, SessionStageType, SessionDatasetType, SessionMainType


@dataclasses.dataclass(frozen=True)
class SessionStarterOptions:
    session_type: SessionMainType = 'training'
    contest: SessionContestType = 'finder'

    stage: SessionStageType = 'rus'
    file_count: Optional[int] = None
    file_timeout: Optional[int] = None

    def prepare_to_command(self) -> dict:
        object_start = {
            'contest': self.contest,
            'params': {
                'countFiles': self.file_count,
                'stage': self.stage,
                'sessionType': self.session_type,
                'time': self.file_timeout
            }
        }

        if self.file_count:
            object_start['params']['countFiles'] = self.file_count

        if self.file_timeout:
            object_start['params']['time'] = self.file_timeout

        return object_start
