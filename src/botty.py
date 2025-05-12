# Dependencies
# from PIL import Image
# import cv2
# import torch
# import logging
# import numpy
# import pyautogui
import asyncio

from src.utils.config_loader import ConfigLoader
from src.utils.network import SocketClient
from src.db.handler import check_db, connect_to_db

async def main():
  config = ConfigLoader()
  sclient = SocketClient(config.ms_uri)

  conn = connect_to_db(config.db_url)
  user = config.load_or_create_user()
  
  check_db(conn)
  config.run_migrations()
  await sclient.connect()

  while True:
    if sclient.connected:
      await sclient.send('bot-data', 'yo mf')
    else:
      print('Still connecting...')
    await asyncio.sleep(1)

# config_logger()
