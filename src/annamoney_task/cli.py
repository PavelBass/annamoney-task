import logging

import click
from aiohttp import web
from annamoney_task import setup
from annamoney_task.handlers import WebSocketHandler

logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:  # pragma: no cover
    setup()


@cli.command()
@click.option('--host', type=str, default='0.0.0.0')
@click.option('--port', type=int, default=8000)
def run(host: str, port: int) -> None:
    logger.info('=== START ===')
    app = web.Application()
    app.router.add_route('GET', '/ws', WebSocketHandler)
    web.run_app(app, host=host, port=port)
