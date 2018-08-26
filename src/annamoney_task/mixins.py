from logging import (
    Logger,
    getLogger,
)
from typing import Optional


# pylint: disable=too-few-public-methods
class LoggerMixin:
    logger: Logger

    def __init__(self, *args, logger_name: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if not (hasattr(self, 'logger') and self.logger):
            self.logger = getLogger(logger_name or self.__class__.__name__)
