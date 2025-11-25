import logging
from typing import Dict, Any

def setup_logger(name: str = 'study_agent'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

def log_event(level: str, message: str, data: Dict[str, Any] = None):
    if data is None:
        data = {}
    msg = f"{message} | data={data}"
    if level.lower() == 'info':
        logger.info(msg)
    elif level.lower() == 'debug':
        logger.debug(msg)
    elif level.lower() == 'error':
        logger.error(msg)
    else:
        logger.warning(msg)
