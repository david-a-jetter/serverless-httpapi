from unittest.mock import patch, MagicMock

from faker import Faker

from hearty.healthkit.manager import HealthKitManager
from hearty.models import IntegerTimeSeries
from tests.factories import IntegerTimeSeriesFactory

fake = Faker()


@patch("hearty.healthkit.manager.DynamoFacetKeyedRepository.build")
def test_build(db_build):
    hr_repo = MagicMock()
    steps_repo = MagicMock()
    db_build.side_effect = [hr_repo, steps_repo]
    environment = fake.bothify()
    manager = HealthKitManager.build(environment)

    assert manager.hr_repo == hr_repo
    assert manager.steps_repo == steps_repo

    call_list = db_build.call_args_list

    hr_args, hr_kwargs = call_list[0]
    steps_args, steps_kwargs = call_list[1]

    assert hr_kwargs["item_class"] == IntegerTimeSeries
    assert hr_kwargs["key_attribute"] == "user_id"
    assert hr_kwargs["facet_attribute"] == "start_epoch_seconds"
    assert hr_kwargs["environment"] == environment
    assert hr_kwargs["table_name"] == "HealthKitHeartRate"

    assert steps_kwargs["item_class"] == IntegerTimeSeries
    assert steps_kwargs["key_attribute"] == "user_id"
    assert steps_kwargs["facet_attribute"] == "start_epoch_seconds"
    assert steps_kwargs["environment"] == environment
    assert steps_kwargs["table_name"] == "HealthKitSteps"


def test_save_heart_rates():
    hr_repo = MagicMock()
    manager = HealthKitManager(hr_repo, MagicMock())
    heart_rates = IntegerTimeSeriesFactory.build_batch(5)
    user_id = fake.bothify()
    manager.save_heart_rates(user_id, heart_rates)

    args, kwargs = hr_repo.save_items.call_args

    assert args[0] == user_id
    assert args[1] == heart_rates


def test_get_heart_rates():
    hr_repo = MagicMock()
    expected_heart_rates = IntegerTimeSeriesFactory.build_batch(5)
    hr_repo.get_items.return_value = expected_heart_rates
    manager = HealthKitManager(hr_repo, MagicMock())
    user_id = fake.bothify()
    actual_heart_rates = manager.get_heart_rates(user_id)

    args, kwargs = hr_repo.get_items.call_args

    assert args[0] == user_id
    assert actual_heart_rates == expected_heart_rates


def test_save_steps():
    steps_repo = MagicMock()
    manager = HealthKitManager(MagicMock(), steps_repo)
    steps = IntegerTimeSeriesFactory.build_batch(5)
    user_id = fake.bothify()
    manager.save_steps(user_id, steps)

    args, kwargs = steps_repo.save_items.call_args

    assert args[0] == user_id
    assert args[1] == steps


def test_get_steps():
    steps_repo = MagicMock()
    expected_steps = IntegerTimeSeriesFactory.build_batch(5)
    steps_repo.get_items.return_value = expected_steps
    manager = HealthKitManager(MagicMock(), steps_repo)
    user_id = fake.bothify()
    actual_heart_rates = manager.get_steps(user_id)

    args, kwargs = steps_repo.get_items.call_args

    assert args[0] == user_id
    assert actual_heart_rates == expected_steps
