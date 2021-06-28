import logging
from pythonjsonlogger import jsonlogger


def startup() -> None:
    logger = logging.getLogger()
    [logger.removeHandler(h) for h in logger.handlers]
    logger.setLevel(logging.INFO)
    logHandler = logging.StreamHandler()
    logHandler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(logHandler)
