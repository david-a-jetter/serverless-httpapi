import logging
from typing import Dict
from pythonjsonlogger import jsonlogger


logger = logging.getLogger(__name__)


def _configure_logging() -> None:
    logger = logging.getLogger()
    [logger.removeHandler(h) for h in logger.handlers]
    logger.setLevel(logging.INFO)
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(logHandler)


class Lifecycle:
    def __init__(self, event: Dict, context):
        self._event = event
        self._context = context
        self._log_context = {"function_name": context.function_name}

    def __enter__(self):
        _configure_logging()
        logger.info("Event received", extra=self._log_context)

    def __exit__(self, type, value, traceback):
        if type:
            logger.error(
                "Event handling failed",
                extra={
                    "type": str(type),
                    "value": str(value),
                    "traceback": traceback.format_exc(),
                    **self._log_context,
                },
            )
        else:
            logger.info("Event handling completed", extra=self._log_context)
