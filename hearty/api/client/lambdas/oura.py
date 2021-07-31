from typing import Dict
from hearty.utils.lifecycle import HttpLifecycle
from hearty.oura.manager import OuraUserAuthManager
from hearty.api.client.models import OuraAuthCodeRequest
from hearty.utils.aws.models import HttpApiPostRequest
from hearty.utils.environment import get_app_environment


@HttpLifecycle()
def authorize_user(event: Dict, context) -> None:

    http_request = HttpApiPostRequest(**event)
    auth_request = OuraAuthCodeRequest.parse_raw(http_request.body)
    auth_manager = OuraUserAuthManager.build(get_app_environment())
    auth_manager.authorize_first_time(http_request.jwt.username, auth_request)
