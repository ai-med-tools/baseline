from pydantic import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class SessionFileSendDto:
    session_id: Optional[int]
    task_id: Optional[int]
    epicrisis_id: Optional[int]
    message: Optional[str]
