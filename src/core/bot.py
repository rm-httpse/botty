# bot.py
import asyncio
import logging
import time

from src.core.perception.interpreter import interpret
from src.core.shared.state import BotState
from src.utils.logger import get_logger

logger = get_logger("BotCore", logging.DEBUG)


class BotClient:

  def __init__(self):
    logger.debug("Bot created")
    self.running = False
    self._task = None
    self._send_callback = None
    self._pending_tasks = []
    self._current_task = {}
    self._tick_rate = 1           # change later

  def start(self, send_callback):
    if not self.running:
      logger.debug("Starting bot")
      self.running = True
      self._send_callback = send_callback
      self._task = asyncio.create_task(self._run())

  def stop(self):
    if self.running:
      logger.debug("Stopping bot")
      self.running = False
      if self._task:
        self._task.cancel()

  async def _run(self):
    try:
      while self.running:
        start = time.perf_counter()
        logger.debug("Bot started, ticking:")
        output = self.tick()
        if self._send_callback:
          logger.debug("Sending callback")
          try:
            await self._send_callback(output.to_dict())
          except Exception as e:
            logger.error(f"Callback failed: {e}", exc_info=True)
        elapsed = time.perf_counter() - start
        remaining = self._tick_rate - elapsed
        if remaining > 0:
          logger.debug("Tick finished on time")
          await asyncio.sleep(remaining)
        else:
          logger.warning(f"Tick took too long ({elapsed:.2f}s)")
    except asyncio.CancelledError:
      logger.debug("Bot task cancelled")

  def tick(self):
    logger.debug('inside tick function')
    return interpret(self._current_task)
