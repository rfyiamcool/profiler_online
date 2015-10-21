import logging

def init_logger(logfile):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = '%(asctime)s - %(process)s - %(levelname)s: - %(message)s'
    formatter = logging.Formatter(fmt)
    handler = logging.FileHandler(logfile)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
