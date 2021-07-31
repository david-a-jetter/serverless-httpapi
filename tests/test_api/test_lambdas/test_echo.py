from unittest.mock import MagicMock

from hearty.api.lambdas.echo import echo
from hearty.utils.aws.models import HttpApiPostRequest
from tests.factories import HttpApiPostRequestFactory


def test_echo():
    request = HttpApiPostRequestFactory()
    response = echo(request.dict(), MagicMock())
    assert HttpApiPostRequest.parse_raw(response["body"]) == request
