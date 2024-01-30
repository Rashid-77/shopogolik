import logging
from datetime import datetime
from functools import lru_cache


@lru_cache
def get_logger(module_name, level=logging.DEBUG):
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh = logging.FileHandler(f"log/log-{datetime.now():%Y-%m-%d}.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(level)
    return logger

@lru_cache
def get_console_logger(module_name, level=logging.DEBUG):
    logging.basicConfig(
            level=level,
            format="[%(asctime)s] %(levelname).1s %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
        )
    return logging.getLogger(module_name)
