import logging
from typing import Dict

from hearty.lifecycle import HttpLifecycle
from hearty.oura.manager import OuraUserAuthManager
from hearty.oura.models import AuthCodeRequest
from hearty.utils.aws_models import HttpApiRequest
from hearty.utils.environment import get_app_environment

logger = logging.getLogger(__name__)


def authorize_user(event: Dict, context) -> None:

    with HttpLifecycle(event, context):
        http_request = HttpApiRequest(**event)
        username = http_request.username
        if username is None:
            raise ValueError("No username provided")
        auth_request = AuthCodeRequest.parse_raw(http_request.body)
        auth_manager = OuraUserAuthManager.build(get_app_environment())
        auth_manager.authorize_first_time(username, auth_request)