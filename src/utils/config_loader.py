import os
import platform
import getpass
import socket
import re
import logging
from pathlib import Path
from dotenv import load_dotenv
from src.db.flyway import run_migrations
from src.utils.logger import get_logger

logger = get_logger("ConfigLoader")


class ConfigLoader:

  def __init__(self, env_path: str = ".env"):
    load_dotenv(env_path)
    self._load_config()

  def _load_config(self):
    self.db_url = self._get("DB_URL")
    self.ms_uri = self._get("MS_URI")
    self.namespace = self._get("IO_NAMESPACE")

  def _get(self, key: str, default=None):
    return os.getenv(key, default)

  def run_migrations(self):
    run_migrations(self.db_url, str(self.migrations_path))
