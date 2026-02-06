import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import hashlib
# from utils.settings import BASE_LOG_PATH


def setup_logger():
    logger = logging.getLogger("jobtelem")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # don't bubble to root/uvicorn

    if logger.handlers:
        return logger  # avoid duplicates

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    os.makedirs("/log", exist_ok=True)
    fh = RotatingFileHandler(
        os.path.join("/log", "info.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        delay=True,               # open file lazily; helps with containers
    )
    fh.setFormatter(fmt)
    logger.addHandler(fh)


    return logger
