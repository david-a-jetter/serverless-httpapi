import logging
from typing import Dict
from hearty.utils.lifecycle import HttpLifecycle
from hearty.oura.manager import OuraUserAuthManager
from hearty.api.client.models import OuraAuthCodeRequest
from hearty.utils.aws.models import HttpApiRequest
from hearty.utils.environment import get_app_environment

logger = logging.getLogger(__name__)


@HttpLifecycle()
def authorize_user(event: Dict, context) -> None:

    http_request = HttpApiRequest(**event)
    username = http_request.username
    if username is None:
        raise ValueError("No username provided")
    auth_request = OuraAuthCodeRequest.parse_raw(http_request.body or "")
    auth_manager = OuraUserAuthManager.build(get_app_environment())
    auth_manager.authorize_first_time(username, auth_request)