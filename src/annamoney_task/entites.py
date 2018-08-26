from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
)


@dataclass
class WebSocketParsedCommand:
    name: str
    arguments: List[str]


@dataclass
class WebSocketCommand:
    method: Callable[[Any], Awaitable[bytes]]
    validators: List[Callable[[List[str]], None]]
