import logging
from typing import Dict
from src.lifecycle import startup
startup()

logger = logging.getLogger(__name__)


def echo(event: Dict, context: Dict) -> Dict:

    return event
