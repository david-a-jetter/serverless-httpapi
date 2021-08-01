from typing import Dict

from hearty.healthkit.manager import HealthKitManager
from hearty.models import IntegerTimeSeriesBatch
from hearty.utils.environment import get_app_environment
from hearty.utils.lifecycle import HttpLifecycle
from hearty.utils.aws.models import HttpApiPostRequest


@HttpLifecycle()
def save_heart_rates(event: Dict, context) -> None:

    http_request = HttpApiPostRequest(**event)
    username = http_request.jwt.username
    heart_rates = IntegerTimeSeriesBatch.parse_raw(http_request.body)

    manager = HealthKitManager.build(get_app_environment())
    manager.save_heart_rates(username, heart_rates.batch)


@HttpLifecycle()
def save_steps(event: Dict, context) -> None:

    http_request = HttpApiPostRequest(**event)
    username = http_request.jwt.username
    heart_rates = IntegerTimeSeriesBatch.parse_raw(http_request.body)

    manager = HealthKitManager.build(get_app_environment())
    manager.save_steps(username, heart_rates.batch)
