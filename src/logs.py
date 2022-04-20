import logging
from typing import Callable

from sqlalchemy import func


def get_logger(function: Callable):
    return logging.getLogger(
        "{classname}.{function}".format(
            classname=function.__self__.__class__.__name__, function=function.__name__
        )
    )
