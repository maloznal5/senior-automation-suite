import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("SAS_MONITOR")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler("logs/bot_core.log")
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger
