import asyncio
import sys
import logging

from src.utils.logger import get_logger

logger = get_logger("CLI")

async def user_listener(onStart, onPause, onStop):
    stop = False
    while not stop:
        cmd = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        cmd = cmd.strip().lower()
        if cmd == "s":
          logger.debug('Calling onStart')
          onStart()
        elif cmd == "p":
            logger.debug('Calling onPause')
            onPause()
        elif cmd == "q":
            logger.info("Calling onStop")
            stop = True
            await onStop()
        else:
            logger.warning("s|p|q are the only possible options")
