from unittest.mock import patch, MagicMock

from hearty.api.client.lambdas.healthkit import save_heart_rates
from tests.factories import IntegerTimeSeriesBatchFactory, HttpApiPostRequestFactory


@patch("hearty.healthkit.manager.HealthKitManager.build")
def test_save_heart_rates(build_manager):
    manager = MagicMock()
    build_manager.return_value = manager
    request_body = IntegerTimeSeriesBatchFactory()
    request = HttpApiPostRequestFactory(body=request_body.json())

    save_heart_rates(request.dict(), MagicMock())

    args, kwargs = manager.save_heart_rates.call_args
    assert args[0] == request.jwt.username
    assert args[1] == request_body.batch
