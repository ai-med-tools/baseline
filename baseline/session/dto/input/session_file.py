from pydantic import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class SessionFileDto:
    session_id: int
    epicrisis_id: int
    version_id: int
    team_id: int
    task_id: int
    session_type_code: str
    aws_link: str
