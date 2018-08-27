import asyncio

import aiohttp
import ujson
from aiohttp import web

from annamoney_task.mixins import LoggerMixin
from annamoney_task.services import websocket_service_instance


class WebSocketHandler(LoggerMixin, web.View):
    service = websocket_service_instance

    async def get(self) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                asyncio.ensure_future(self._process_ws_message(ws, msg.data))
        return ws

    async def _process_ws_message(self, ws: web.WebSocketResponse, message: str):
        answer = await self.service.process_message(message)
        await ws.send_json(answer, dumps=ujson.dumps)
