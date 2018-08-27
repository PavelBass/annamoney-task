import asyncio
import dataclasses
import time
from types import MappingProxyType
from typing import (
    Callable,
    Any,
    Awaitable,
    List,
    Dict,
)

from annamoney_task.entites import (
    WebSocketCommandEntity,
    WebSocketParsedCommandEntity,
    WebSocketCommandResultEntity,
)
from annamoney_task.mixins import LoggerMixin
from annamoney_task.validators import ValidationError


class WebSocketService(LoggerMixin):
    def __init__(self):
        super().__init__()
        self._commands = {'ping': WebSocketCommandEntity(self._ping, [])}
        self._default = WebSocketCommandEntity(self._default_command, [])

    @property
    def commands(self) -> MappingProxyType:
        return MappingProxyType(self._commands)

    @staticmethod
    async def _default_command(command: WebSocketParsedCommandEntity) -> WebSocketCommandResultEntity:
        return WebSocketCommandResultEntity(
            f'Unknown command "{command.name}" {str(command.arguments)}',
            0,
        )

    @staticmethod
    async def _invalid_command_result(command: WebSocketParsedCommandEntity) -> WebSocketCommandResultEntity:
        return WebSocketCommandResultEntity(
            f'Invalid command arguments: "{command.name}" {" ".join(command.arguments)}',
            0,
        )

    # pylint: disable=unused-argument
    @staticmethod
    async def _ping(command: WebSocketParsedCommandEntity) -> WebSocketCommandResultEntity:
        return WebSocketCommandResultEntity('pong', 0)
    # pylint: enable=unused-argument

    @staticmethod
    def _parse_message(message: str) -> WebSocketParsedCommandEntity:
        command_name, *args = message.strip().split(' ')
        return WebSocketParsedCommandEntity(command_name, args)

    async def process_message(self, message: str) -> Dict[str, Any]:
        parsed_command = self._parse_message(message)
        command = self._commands.get(parsed_command.name, self._default)
        try:
            [validator(parsed_command.arguments) for validator in command.validators]
        except ValidationError:
            return dataclasses.asdict(await self._invalid_command_result(parsed_command))
        return dataclasses.asdict(await command.method(parsed_command))

    def register_command(
            self,
            command_name: str,
            method: Callable[[Any], Awaitable[bytes]],
            validators: List[Callable[[List[str]], None]]
    ) -> None:
        self._commands[command_name] = WebSocketCommandEntity(method, validators)


class FactorialService(LoggerMixin):
    def __init__(self):
        super().__init__()
        self._cache = {0: 0, 1: 1, 2: 2}

    async def get_factorial_command(self, command: WebSocketParsedCommandEntity) -> WebSocketCommandResultEntity:
        start = time.time()
        number = int(command.arguments[0])
        result = await self.get_factorial(number)
        return WebSocketCommandResultEntity(str(result), time.time() - start)

    async def get_factorial(self, number: int) -> int:
        number = abs(number)
        self.logger.info('Started factorial %s', number)
        if number in self._cache:
            return self._cache[number]
        if (number - 1) not in self._cache:
            asyncio.ensure_future(self.get_factorial(number - 1))
        result = await self._get_cached(number - 1) * number
        self._cache[number] = result
        self.logger.info('Cached factorial %s', number)
        return result

    async def _get_cached(self, number: int) -> int:
        while number not in self._cache:
            await asyncio.sleep(0)
        return self._cache[number]


websocket_service_instance = WebSocketService()
