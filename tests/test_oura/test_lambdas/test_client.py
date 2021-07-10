from unittest.mock import patch, MagicMock

from hearty.oura.lambdas.client import authorize_user
from tests.factories import HttpApiRequestFactory
from tests.test_oura.factories import AuthCodeRequestFactory


@patch("hearty.oura.lambdas.client.OuraUserAuthManager")
def test_authorize_user(auth_mgr):
    manager = MagicMock()
    auth_mgr.build.return_value = manager

    auth_request = AuthCodeRequestFactory()
    http_request = HttpApiRequestFactory(body=auth_request.json())

    authorize_user(http_request.dict(), MagicMock())

    args, kwargs = manager.authorize_first_time.call_args

    assert args[0] == http_request.username
    assert args[1] == auth_request
