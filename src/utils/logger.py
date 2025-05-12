import logging


def get_logger(name="bot", level=logging.INFO):
  logger = logging.getLogger(name)
  if not logger.hasHandlers():
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

  return logger
