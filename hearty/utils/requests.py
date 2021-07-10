import logging
from typing import Any, Optional, List
from uuid import uuid4
from requests import Response, PreparedRequest, Session
from requests.adapters import HTTPAdapter


logger = logging.getLogger(__name__)


class LoggingAdapter(HTTPAdapter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(LoggingAdapter, self).__init__(*args, kwargs)

    def send(self, request: PreparedRequest, *args: Any, **kwargs: Any) -> Response:

        request_id = str(uuid4())
        request_context = {"logging_adapter_request_id": request_id, "request_url": request.url}
        logger.info("Initiating HTTPAdapter request", extra=request_context)
        logger.debug(
            "Initiating HTTP Adapter request with body",
            extra={"request_body": request.body, **request_context},
        )

        response = super(LoggingAdapter, self).send(request, *args, **kwargs)

        logger.info(
            "Received HTTPAdapter response",
            extra={"response_status_code": response.status_code, **request_context},
        )
        logger.debug(
            "Received HTTPAdapter response with body",
            extra={
                "response_status_code": response.status_code,
                "response_body": response.text,
                **request_context,
            },
        )

        return response


def mount_logging_adapters(session: Session, skip_prefixes: Optional[List[str]] = None) -> None:

    for prefix, adapter in session.adapters.items():
        if isinstance(adapter, HTTPAdapter):
            session.adapters[prefix] = LoggingAdapter()

    if skip_prefixes is not None:
        for prefix in skip_prefixes:
            session.mount(prefix, HTTPAdapter())
