import logging
from functools import wraps
from http import HTTPStatus
from typing import Dict

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
from contextlib import ContextDecorator

from hearty.models import ApiError, ApiResponse
from hearty.utils.aws.models import HttpApiResponse

logger = logging.getLogger(__name__)


def _configure_logging() -> None:
    root_logger = logging.getLogger()
    [root_logger.removeHandler(h) for h in root_logger.handlers]
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
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
            context = {"function_name": context.function_name}
            logger.info("Event received", extra=context)
            try:
                output = func(event, context)
                logger.info("Event handling successfully completed", extra=context)
                if isinstance(output, HttpApiResponse):
                    return output.dict()

                if isinstance(output, BaseModel):
                    api_response = output
                else:
                    api_response = ApiResponse(message=str(output))
                response = HttpApiResponse(body=api_response.json())
                return response.dict()

            except Exception as ex:
                logger.exception("Exception raised from event handler", extra=context)
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