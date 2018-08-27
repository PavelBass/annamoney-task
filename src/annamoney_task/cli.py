import logging

import click
from aiohttp import web
from annamoney_task import setup
from annamoney_task.handlers import WebSocketHandler
from annamoney_task.services import (
    websocket_service_instance,
    FactorialService,
)

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
    _configure_application(app)
    _configure_service()
    web.run_app(app, host=host, port=port)


def _configure_application(app: web.Application) -> None:
    app.router.add_route('GET', '/ws', WebSocketHandler)


def _configure_service() -> None:
    websocket_service_instance.register_command('get_factorial', FactorialService().get_factorial_command, [])
