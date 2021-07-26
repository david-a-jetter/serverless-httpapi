from unittest.mock import patch

from faker import Faker
from requests import Session, PreparedRequest
from hearty.utils.requests import mount_logging_adapters, LoggingAdapter


fake = Faker()


@patch("hearty.utils.requests.HTTPAdapter.__init__")
@patch("hearty.utils.requests.HTTPAdapter.send")
def test_logging_adapter_send(super_send, super_init):
    init_args = [fake.bs() for _ in range(0, 3)]
    init_kwargs = {fake.bs(): fake.bs() for _ in range(0, 3)}
    adapter = LoggingAdapter(*init_args, **init_kwargs)

    class Response:
        status_code = 204
        text = fake.bs()

    response = Response()
    super_send.send.return_value = response
    request = PreparedRequest()
    send_args = [fake.bs() for _ in range(0, 3)]
    send_kwargs = {fake.bs(): fake.bs() for _ in range(0, 3)}

    adapter.send(request, *send_args, **send_kwargs)

    assert list(super_init.call_args[0]) == init_args
    assert super_init.call_args[1] == init_kwargs

    assert list(super_send.call_args[0]) == [request, *send_args]
    assert super_send.call_args[1] == send_kwargs


def test_mount_logging_adapters():

    session = Session()
    mount_logging_adapters(session)

    for prefix, adapter in session.adapters.items():
        assert isinstance(adapter, LoggingAdapter)
