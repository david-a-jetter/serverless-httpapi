import logging
from typing import Dict
from hearty.utils.lifecycle import HttpLifecycle
from hearty.utils.aws_models import HttpApiRequest


logger = logging.getLogger(__name__)


def echo(event: Dict, context) -> Dict:

    with HttpLifecycle(event, context):
        request = HttpApiRequest(**event)
        logger.info("Received event", extra={"request_body": request.body})

        return event
