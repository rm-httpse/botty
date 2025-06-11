# src/control.py
import asyncio
from src.db.handler import get_db_config, check_db
from src.utils.logger import get_logger
from src.core.bot import BotClient
from src.utils.network import SocketClient

logger = get_logger("AppController")

class AppController:
    def __init__(self, config):
        self.config = config
        self.connector = get_db_config(self.config.db_url)
        self.socket = SocketClient(config.ms_uri, config.namespace)
        self.bot = BotClient()
        self.user = None
        self.running = False
        self.paused = False
        check_db(self.conn) # Always check if DB exists (create it if not exists)
        
    def is_running(self):
        return self.running

    def create_user(self):
        self.user = self.config.create_user()
    
    def load_user(self):
        logger.info("Loading configuration and database")
        self.user = self.config.load_user()
        self.config.run_migrations()

    def reset(self):
        logger.info("Reset not implemented yet")

    async def connect_to_socket(self):
        logger.info("Connecting to socket server")
        await self.socket.connect()

    def start_bot(self):
        if not self.running:
            logger.info("Starting bot")
            self.bot.start(lambda output: self.socket.send("bot-data", output))
            self.running = True
        else:
            logger.warning("Bot already running")

    def pause_bot(self):
        if self.running:
            logger.info("Pausing bot")
            self.bot.stop()
            self.running = False
        else:
            logger.warning("Bot is not running")

    async def stop_bot(self, force=False):
        logger.info("Stopping bot and closing connection")
        self.bot.stop()
        if self.socket.connected or force:
            await self.socket.disconnect()

