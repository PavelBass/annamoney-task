from types import MappingProxyType

import pytest

from annamoney_task.entites import (
    WebSocketParsedCommandEntity,
    WebSocketCommandResultEntity,
)
from annamoney_task.services import (
    WebSocketService,
    FactorialService,
)


def test_websocketservice__commands__exists_with_expected_type():
    # arrange
    ws_service = WebSocketService()

    # assert
    assert isinstance(ws_service.commands, MappingProxyType)


@pytest.mark.asyncio
async def test_websocketservice__ping__return_expected():
    # arrange
    ws_service = WebSocketService()

    # act
    result = await ws_service._ping('any')

    # assert
    assert isinstance(result, WebSocketCommandResultEntity)
    assert result.result == 'pong'


@pytest.mark.asyncio
async def test_websocketservice__default__return_expected_type():
    # arrange
    ws_service = WebSocketService()
    command = WebSocketParsedCommandEntity('any', ['args'])

    # act
    result = await ws_service._default_command(command)

    # assert
    assert isinstance(result, WebSocketCommandResultEntity)


@pytest.mark.asyncio
async def test_websocketservice__invalid_command__return_expected_type():
    # arrange
    ws_service = WebSocketService()
    command = WebSocketParsedCommandEntity('any', ['args'])

    # act
    result = await ws_service._invalid_command_result(command)

    # assert
    assert isinstance(result, WebSocketCommandResultEntity)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'message,expected', [
        ('ping', {'result': 'pong', 'time': 0})
    ]
)
async def test_websocketservice__process_message__return_expected(message, expected):
    # arrange
    ws_service = WebSocketService()

    # act
    result = await ws_service.process_message(message)

    # assert
    assert result == expected


def test_websocketservice__parse_message__return_expected_type():
    # arrange
    ws_service = WebSocketService()

    # act
    result = ws_service._parse_message('some message')

    # assert
    assert isinstance(result, WebSocketParsedCommandEntity)


def test_websocketservice__register_command__adds_command():
    # arrange
    ws_service = WebSocketService()
    commands_len = len(ws_service.commands)

    async def some_awaitable():
        pass

    # act
    ws_service.register_command('some-new-command', some_awaitable, [])

    # assert
    assert len(ws_service.commands) == commands_len + 1
    assert 'some-new-command' in ws_service.commands


@pytest.mark.asyncio
async def test_factorialservice__get_cached__returns_expected():
    # arrange
    factorial_service = FactorialService()
    factorial_service._cache[10] = 123

    # act
    result = await factorial_service._get_cached(10)

    # assert
    assert result == 123


@pytest.mark.asyncio
async def test_factorialservice_get_factorial__cached_number__returns_expected():
    # arrange
    factorial_service = FactorialService()
    factorial_service._cache[10] = 123

    # act
    result = await factorial_service.get_factorial(10)

    # assert
    assert result == 123


@pytest.mark.asyncio
async def test_factorialservice_get_factorial__not_cached_number__returns_expected():
    # arrange
    factorial_service = FactorialService()

    # act
    result = await factorial_service.get_factorial(10)

    # assert
    assert result == 3628800


@pytest.mark.asyncio
async def test_factorialservice__get_factorial_command__returns_expected():
    # arrange
    factorial_service = FactorialService()
    command = WebSocketParsedCommandEntity('get_factorial', ['10'])

    # act
    result = await factorial_service.get_factorial_command(command)

    # assert
    assert isinstance(result, WebSocketCommandResultEntity)
    assert result.result == '3628800'
