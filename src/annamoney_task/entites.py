from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
    Union,
)


@dataclass
class WebSocketParsedCommandEntity:
    name: str
    arguments: List[str]


@dataclass
class WebSocketCommandEntity:
    method: Callable[[Any], Awaitable[bytes]]
    validators: List[Callable[[List[str]], None]]


@dataclass
class WebSocketCommandResultEntity:
    result: Union[str, int, float]
    time: float
