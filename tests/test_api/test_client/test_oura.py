from unittest.mock import patch, MagicMock

from faker import Faker

from hearty.api.client.lambdas.oura import authorize_user
from tests.factories import HttpApiRequestFactory
from tests.test_oura.factories import OuraAuthCodeRequestFactory


fake = Faker()


@patch("hearty.api.client.lambdas.oura.OuraUserAuthManager")
def test_authorize_user(auth_mgr):
    manager = MagicMock()
    auth_mgr.build.return_value = manager

    auth_request = OuraAuthCodeRequestFactory()
    http_request = HttpApiRequestFactory(body=auth_request.json())

    authorize_user(http_request.dict(), MagicMock())

    args, kwargs = manager.authorize_first_time.call_args

    assert args[0] == http_request.jwt.username
    assert args[1] == auth_request


def test_authorize_user_no_username():

    http_request = HttpApiRequestFactory()
    del http_request.requestContext.authorizer.jwt.claims["username"]

    try:
        authorize_user(http_request.dict(), MagicMock())
    except Exception as ex:
        assert isinstance(ex, KeyError)
