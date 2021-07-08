import logging


def get_logger(module_name: str, session_id: str = None) -> logging.Logger:
    """Method to return the logger"""
    log_name = "dmai.log"
    if session_id:
        log_name = "dmai_{s}.log"
    logger = logging.getLogger(module_name)
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_name)

    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.WARNING)
    file_handler.setLevel(logging.DEBUG)

    return logger
