import logging

logger = logging.getLogger("filemover")
logger.setLevel(logging.INFO)

logger.propagate = False

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)