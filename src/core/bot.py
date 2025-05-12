# bot.py
import asyncio
import logging

from src.utils.logger import get_logger

logger = get_logger("BotCore", logging.DEBUG)

class BotClient:
    def __init__(self):
        logger.debug("Bot created")
        self.running = False
        self._task = None
        self._send_callback = None

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
                logger.debug("Bot started, ticking:")
                output = self.tick()
                if self._send_callback:
                    await self._send_callback(output)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.debug("Bot task cancelled")

    def tick(self):
        return "Bot is ticking"
