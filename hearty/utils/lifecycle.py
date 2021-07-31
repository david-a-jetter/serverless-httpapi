import logging
from threading import local
from functools import wraps
from http import HTTPStatus
from typing import Dict, Iterable

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
from contextlib import ContextDecorator

from hearty.api.models import ApiError, ApiResponse
from hearty.utils.aws.models import HttpApiResponse


logger = logging.getLogger(__name__)
log_context_data = local()


def update_context(**kwargs) -> None:
    for k, v in kwargs.items():
        setattr(log_context_data, k, v)


def remove_context(keys: Iterable[str]) -> None:
    for k in keys:
        if hasattr(log_context_data, k):
            delattr(log_context_data, k)


class ThreadingLocalContextFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        for k, v in log_context_data.__dict__.items():
            setattr(record, k, v)
        return True


def _configure_logging() -> None:
    root_logger = logging.getLogger()
    for h in root_logger.handlers:
        root_logger.removeHandler(h)
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.addFilter(ThreadingLocalContextFilter())
    handler.setFormatter(jsonlogger.JsonFormatter())
    root_logger.addHandler(handler)


class HttpLifecycle(ContextDecorator):
    def __init__(self):
        _configure_logging()

    def __enter__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapped_f(event: Dict, context) -> Dict:
            log_ctx = {"function_name": context.function_name}
            update_context(**log_ctx)
            logger.info("Event received")
            try:
                output = func(event, context)
                logger.info("Event handling successfully completed")

                # TODO: Make this a map / strategy pattern
                if output is None:
                    http_response = HttpApiResponse()
                elif isinstance(output, HttpApiResponse):
                    http_response = output
                elif isinstance(output, BaseModel):
                    http_response = HttpApiResponse(body=output.json())
                else:
                    http_response = HttpApiResponse(body=ApiResponse(message=str(output)).json())
                return http_response.dict()

            except Exception as ex:
                logger.exception("Exception raised from event handler")
                response = HttpApiResponse(
                    statusCode=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                    body=ApiError(error=str(ex)).json(),
                )
                return response.dict()

        return wrapped_f

    def __exit__(self, type, value, traceback):
        if type:
            logger.error(
                "Event handling failed",
                extra={"type": str(type), "value": str(value), "traceback": traceback.format_exc()},
            )
        else:
            logger.info("Event handling completed")
