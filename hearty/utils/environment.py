import os

from hearty.constants import APP_NAME


def get_app_environment():
    stage = os.environ.get("stage", "dev")
    return f"{APP_NAME}-{stage}"
