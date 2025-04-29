from PIL import Image
import cv2
import pyautogui
import torch
import logging
import websockets
import numpy
import requests
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
x = os.getenv("HELLO")
print(x)

# Connect to Microservice, instance websocket
# ...
# ...

# Run bot