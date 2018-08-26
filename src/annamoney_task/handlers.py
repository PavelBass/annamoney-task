import aiohttp
from aiohttp import web

from annamoney_task.mixins import LoggerMixin
from annamoney_task.services import WebSocketService


class WebSocketHandler(web.View, LoggerMixin):
    service = WebSocketService()

    async def get(self) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.service.process_message(msg.body)
        return ws
