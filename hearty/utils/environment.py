import os

from hearty.constants import APP_NAME


def get_stage() -> str:
    return os.environ.get("stage", "dev")


def get_app_environment() -> str:
    return f"{APP_NAME}-{get_stage()}"
