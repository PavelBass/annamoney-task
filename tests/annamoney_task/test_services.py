from types import MappingProxyType

import pytest

from annamoney_task.entites import WebSocketParsedCommand
from annamoney_task.services import WebSocketService


@pytest.mark.asyncio
async def test_websocket_service__commands__exists_with_expected_type():
    # arrange
    ws_service = WebSocketService()

    # assert
    assert isinstance(ws_service.commands, MappingProxyType)


@pytest.mark.asyncio
async def test_websocket_service__ping__return_expected():
    # arrange
    ws_service = WebSocketService()

    # act
    result = await ws_service._ping('any')

    # assert
    assert isinstance(result, bytes)
    assert result == b'pong'


@pytest.mark.asyncio
async def test_websocket_service__default__return_expected_type():
    # arrange
    ws_service = WebSocketService()

    # act
    result = await ws_service._default_command('any', ['args'])

    # assert
    assert isinstance(result, bytes)


@pytest.mark.asyncio
async def test_websocket_service__invalid_command_result__return_expected_type():
    # arrange
    ws_service = WebSocketService()
    command = WebSocketParsedCommand('any', ['args'])

    # act
    result = await ws_service._invalid_command_result(command)

    # assert
    assert isinstance(result, bytes)
