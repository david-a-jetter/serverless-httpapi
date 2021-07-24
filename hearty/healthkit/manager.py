from typing import Iterable, Dict

from hearty.healthkit.constants import HEART_RATE_TABLE, STEPS_TABLE
from hearty.models import IntegerTimeSeries, TIME_SERIES_START
from hearty.utils.aws.dynamo import DynamoFacetKeyedRepository
from hearty.utils.constants import USER_KEY_ATTRIBUTE
from hearty.utils.storage import FacetKeyedRepository


class HealthKitManager:
    @classmethod
    def build(cls, environment: str):
        hr_repo = DynamoFacetKeyedRepository[IntegerTimeSeries, int].build(
            item_class=IntegerTimeSeries,
            key_attribute=USER_KEY_ATTRIBUTE,
            facet_attribute=TIME_SERIES_START,
            environment=environment,
            table_name=HEART_RATE_TABLE,
        )
        steps_repo = DynamoFacetKeyedRepository[IntegerTimeSeries, int].build(
            item_class=IntegerTimeSeries,
            key_attribute=USER_KEY_ATTRIBUTE,
            facet_attribute=TIME_SERIES_START,
            environment=environment,
            table_name=STEPS_TABLE,
        )

        return cls(hr_repo=hr_repo, steps_repo=steps_repo)

    def __init__(
        self,
        hr_repo: FacetKeyedRepository[IntegerTimeSeries, int],
        steps_repo: FacetKeyedRepository[IntegerTimeSeries, int],
    ):
        self.hr_repo = hr_repo
        self.steps_repo = steps_repo

    def save_heart_rates(self, user_id: str, heart_rates: Iterable[IntegerTimeSeries]) -> None:
        self.hr_repo.save_items(user_id, heart_rates)

    def get_heart_rates(self, user_id: str) -> Dict[int, IntegerTimeSeries]:
        return self.hr_repo.get_items(user_id)

    def save_steps(self, user_id: str, steps: Iterable[IntegerTimeSeries]) -> None:
        self.steps_repo.save_items(user_id, steps)

    def get_steps(self, user_id: str) -> Dict[int, IntegerTimeSeries]:
        return self.steps_repo.get_items(user_id)
