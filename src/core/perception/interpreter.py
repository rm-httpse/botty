import logging

from PIL import ImageGrab
from src.core.shared.state import BotState
from src.utils.logger import get_logger

logger = get_logger("Interpreter", logging.DEBUG)

def interpret(task: dict | None = None) -> BotState:
  try:
    logger.debug('Grabbing image')
    screen = ImageGrab.grab()
    logger.debug('Returning state')
    return BotState(screen=screen, task=task or {}, status='idle')
  except Exception as e:
    return BotState(screen=None, task=task or {}, status=f"error: {e}")
