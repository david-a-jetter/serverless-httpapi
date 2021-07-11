import logging
from typing import Dict
from hearty.utils.lifecycle import HttpLifecycle
from hearty.utils.aws.models import HttpApiRequest


logger = logging.getLogger(__name__)


@HttpLifecycle()
def echo(event: Dict, context) -> Dict:

    request = HttpApiRequest(**event)
    logger.info("Received event", extra={"request_body": request.body})

    return event
