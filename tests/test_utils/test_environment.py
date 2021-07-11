from unittest.mock import patch

from faker import Faker
from hearty.utils.environment import get_app_environment

fake = Faker()


@patch("hearty.utils.environment.os")
def test_get_app_environment(os):
    stage = fake.bothify()
    os.environ = {"stage": stage}

    app_env = get_app_environment()

    assert app_env == f"hearty-{stage}"


@patch("hearty.utils.environment.os")
def test_get_app_environment_default(os):
    os.environ = {}

    app_env = get_app_environment()

    assert app_env == "hearty-dev"
