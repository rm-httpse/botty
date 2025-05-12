# from PIL import Image
# import cv2
# import torch
# import numpy
# import pyautogui
import asyncio
import logging
import sys

from src.utils.config_loader import ConfigLoader
from src.utils.network import SocketClient
from src.db.handler import check_db, connect_to_db
from src.utils.logger import get_logger
from src.core.bot import BotClient
from src.ui.cli import user_listener

logger = get_logger("BottyMain")

async def main():
  config = ConfigLoader()
  bot = BotClient()
  socket = SocketClient(config.ms_uri, config.namespace)

  conn = connect_to_db(config.db_url)
  check_db(conn)
  user = config.load_or_create_user()
  config.run_migrations()

  await socket.connect()

  def onStart():
    bot.start(lambda output: socket.send("bot-data", output))

  def onPause():
    bot.stop()

  async def onStop():
    bot.stop()
    await socket.disconnect()

  try:
    await user_listener(onStart, onPause, onStop)
  except asyncio.CancelledError:
    logger.info("Program Error")
  finally:
    await socket.disconnect()