import logging
from typing import Dict
from pythonjsonlogger import jsonlogger


logger = logging.getLogger(__name__)


def _configure_logging() -> None:
    root_logger = logging.getLogger()
    [root_logger.removeHandler(h) for h in root_logger.handlers]
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter())
    root_logger.addHandler(handler)


class HttpLifecycle:
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
