from unittest.mock import MagicMock

from hearty.api.lambdas.echo import echo
from hearty.utils.aws.models import HttpApiRequest
from tests.factories import HttpApiRequestFactory


def test_echo():
    request = HttpApiRequestFactory()
    response = echo(request.dict(), MagicMock())
    assert HttpApiRequest.parse_raw(response["body"]) == request
