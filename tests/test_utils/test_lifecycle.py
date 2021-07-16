from http import HTTPStatus
from unittest.mock import MagicMock

from faker import Faker

from hearty.api.models import ApiResponse, ApiError
from hearty.utils.aws.models import HttpApiResponse
from hearty.utils.lifecycle import HttpLifecycle

fake = Faker()


def test_none_response():
    @HttpLifecycle()
    def wrapped(event, context):
        return None

    actual = wrapped(MagicMock(), MagicMock())

    assert actual == HttpApiResponse().dict()


def test_successful_http_api_response():
    expected = HttpApiResponse(statusCode=HTTPStatus.ACCEPTED.value, body=fake.bothify())

    @HttpLifecycle()
    def wrapped(event, context):
        return expected

    actual = wrapped(MagicMock(), MagicMock())

    assert actual == expected


def test_successful_base_model():
    expected = ApiResponse(message=fake.bothify())

    @HttpLifecycle()
    def wrapped(event, context):
        return expected

    actual = wrapped(MagicMock(), MagicMock())

    assert actual["statusCode"] == HTTPStatus.OK.value
    response = ApiResponse.parse_raw(actual["body"])
    assert response == expected


def test_successful_simple_response():

    expected = fake.random_int()

    @HttpLifecycle()
    def wrapped(event, context):
        return expected

    actual = wrapped(MagicMock(), MagicMock())

    assert actual["statusCode"] == HTTPStatus.OK.value
    response = ApiResponse.parse_raw(actual["body"])
    assert response.message == str(expected)


def test_exception_response():

    error_message = fake.bothify()

    @HttpLifecycle()
    def wrapped(event, context):
        raise Exception(error_message)

    actual = wrapped(MagicMock(), MagicMock())

    assert actual["statusCode"] == HTTPStatus.INTERNAL_SERVER_ERROR.value
    response = ApiError.parse_raw(actual["body"])
    assert response.error == str(Exception(error_message))
