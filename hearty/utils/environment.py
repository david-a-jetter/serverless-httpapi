import os


def get_app_environment():
    stage = os.environ.get("stage", "dev")
    return f"hearty-{stage}"
