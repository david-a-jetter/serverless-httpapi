import logging
from typing import Dict
from hearty.lifecycle import startup

startup()

logger = logging.getLogger(__name__)


def echo(event: Dict, context) -> Dict:

    logger.info("Received event", extra={"request_body": event.get("body")})

    return event
