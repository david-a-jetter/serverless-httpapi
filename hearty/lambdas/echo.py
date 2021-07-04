import logging
from typing import Dict
from hearty.lifecycle import Lifecycle
from hearty.utils.aws_models import ApiRequest


logger = logging.getLogger(__name__)


def echo(event: Dict, context) -> Dict:

    with Lifecycle(event, context):
        request = ApiRequest(**event)
        logger.info("Received event", extra={"request_body": request.body})

        return event
