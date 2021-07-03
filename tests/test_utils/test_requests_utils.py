from requests import Session
from hearty.utils.requests_utils import mount_logging_adapters, LoggingAdapter


def test_mount_logging_adapters():

    session = Session()
    mount_logging_adapters(session)

    for prefix, adapter in session.adapters.items():
        assert isinstance(adapter, LoggingAdapter)
