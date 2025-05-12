import socketio
import logging

from src.utils.logger import get_logger

logger = get_logger("Network")


class SocketClient:

  def __init__(self, server_url, namespace):
    self.server_url = server_url
    self.client = socketio.AsyncClient()
    self.connected = False
    self.namespace = namespace

    self.client.on("connect", self._on_connect, namespace=self.namespace)
    self.client.on("disconnect", self._on_disconnect, namespace=self.namespace)

  async def connect(self):
    try:
      logger.info(f'Connecting to: {self.server_url}')
      await self.client.connect(self.server_url,
                                namespaces=["/bot"],
                                socketio_path="web/socket.io",
                                wait=True)
    except Exception as e:
      logger.info(f'Error while trying to connect')
      logger.debug(e)
  
  async def disconnect(self):
    logger.info('Disconnect socket')
    await self.client.disconnect()

  async def _on_connect(self):
    self.connected = True
    logger.info(f'Connection established!')

  async def _on_disconnect(self):
    self.connected = False
    logger.info(f'Connection ended')

  async def send(self, event_name, data):
    if self.connected:
      await self.client.emit(event_name, data, namespace=self.namespace)
    else:
      logger.info(f'Cannot send if no connection is established')
