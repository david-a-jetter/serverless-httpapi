import json
import logging
from typing import Dict
from src.lifecycle import startup

startup()

logger = logging.getLogger(__name__)


def echo(event: Dict, context: Dict) -> Dict:

    logger.debug(
        "Received event",
        extra={"event": json.dumps(event), "request_id": context["aws_request_id "]},
    )

    return event
