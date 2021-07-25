from typing import Dict

from hearty.healthkit.manager import HealthKitManager
from hearty.models import IntegerTimeSeriesBatch
from hearty.utils.environment import get_app_environment
from hearty.utils.lifecycle import HttpLifecycle
from hearty.utils.aws.models import HttpApiRequest


@HttpLifecycle()
def get_heart_rates(event: Dict, context) -> IntegerTimeSeriesBatch:

    http_request = HttpApiRequest(**event)
    user_id = http_request.pathParameters["userId"]
    manager = HealthKitManager.build(get_app_environment())
    heart_rates = manager.get_heart_rates(user_id)
    response = IntegerTimeSeriesBatch(batch=[v for k, v in heart_rates.items()])
    return response
