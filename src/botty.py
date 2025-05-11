# Dependencies
# from PIL import Image
# import cv2
# import pyautogui
# import torch
# import logging
# import websockets
# import numpy
# import requests
# import os
import time

from src.utils.config_loader import ConfigLoader
from src.utils.network import SocketClient
from src.db.handler import check_db, connect_to_db

def main():
  config = ConfigLoader()
  conn = connect_to_db(config.db_url)
  config.load_or_create_user()
  check_db(conn)

  config.run_migrations()

  sclient = SocketClient(config.ms_uri)
  sclient.connect()

  while True:
    sclient.send('bot-data', 'yo mf')
    time.sleep(1)

# config_logger()
