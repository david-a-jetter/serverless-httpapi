import logging
from typing import Dict
from hearty.utils.lifecycle import HttpLifecycle
from hearty.utils.aws.models import HttpApiPostRequest

logger = logging.getLogger(__name__)


@HttpLifecycle()
def echo(event: Dict, context):

    request = HttpApiPostRequest(**event)
    logger.info("Received event", extra={"request_body": request.body})

    return request
