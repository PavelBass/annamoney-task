from types import MappingProxyType

from annamoney_task.entites import (
    WebSocketCommand,
    WebSocketParsedCommand,
)
from annamoney_task.mixins import LoggerMixin
from annamoney_task.validators import ValidationError


class WebSocketService(LoggerMixin):
    def __init__(self):
        super().__init__()
        self._commands = {'ping': WebSocketCommand(self._ping, [])}
        self._default = WebSocketCommand(self._default_command, [])

    @property
    def commands(self) -> MappingProxyType:
        return MappingProxyType(self._commands)

    @staticmethod
    async def _default_command(command_name: str, *args) -> bytes:
        return f'Unknown command "{command_name}" {str(args)}'.encode()

    @staticmethod
    async def _invalid_command_result(parsed_command: WebSocketParsedCommand) -> bytes:
        return f'Invalid command arguments: "{parsed_command.name}" {" ".join(parsed_command.arguments)}'.encode()

    @staticmethod
    async def _ping(command_name: str) -> bytes:  # pylint: disable=unused-argument
        return b'pong'

    @staticmethod
    def _parse_message(message: str) -> WebSocketParsedCommand:
        return WebSocketParsedCommand(message, [])

    async def process_message(self, message: str):
        parsed_command = self._parse_message(message)
        command = self._commands.get(parsed_command.name, self._default)
        try:
            [validator(parsed_command.arguments) for validator in command.validators]
        except ValidationError:
            return await self._invalid_command_result(parsed_command)
        return await command.method(parsed_command.name, *parsed_command.arguments)
