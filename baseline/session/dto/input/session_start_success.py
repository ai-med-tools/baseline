from pydantic import dataclasses


@dataclasses.dataclass(frozen=True)
class SessionStartSuccessDto:
    session_id: int
