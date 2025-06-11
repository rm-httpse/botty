import asyncio
import sys
import logging
from new.Botty.src.controller import AppController

from src.utils.logger import get_logger

logger = get_logger("CLI")


async def user_listener(controller: AppController):
  stop = False
  while controller.is_running():
    print("Waiting for input...\n")
    cmd = await asyncio.get_event_loop().run_in_executor(
        None, sys.stdin.readline)
    cmd = cmd.strip().lower()
    if cmd == '1':
      logger.debug('Calling onInit')
      # logic for loading user
      pass
    if cmd == '2':
      logger.debug('Calling onConnect')
      # connect / disconnect from socket
      pass
    if cmd == '3':
      logger.debug('Calling onStart')
      # start botting
      pass
    if cmd == '4':
      logger.debug('Calling onPause')
      # suspend botting
      pass
    if cmd == '5':
      logger.debug('Calling onStop')
      # quit program
      pass

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
