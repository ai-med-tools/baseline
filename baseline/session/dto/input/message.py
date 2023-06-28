from pydantic import dataclasses


@dataclasses.dataclass(frozen=True)
class MessageDto:
    message: str
