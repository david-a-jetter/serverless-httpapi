import logging
from typing import Dict
from hearty.lifecycle import startup
from hearty.oura.models import AuthCodeRequest

startup()
logger = logging.getLogger(__name__)


def echo(event: Dict, context) -> Dict:

    pass
