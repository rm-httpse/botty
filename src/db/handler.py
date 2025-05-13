import psycopg2
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
from src.utils.logger import get_logger

logger = get_logger("DBHandler")


def connect_to_db(db_url: str):
  parsed = urlparse(db_url)
  db_name = parsed.path.lstrip("/")
  user = parsed.username
  password = parsed.password
  host = parsed.hostname or "localhost"
  port = parsed.port or 5432
  return {
      "db_name": db_name,
      "user": user,
      "password": password,
      "host": host,
      "port": port,
      "admin_url": db_url.replace(f"/{db_name}", "/postgres")
  }


def check_db(config: dict):
  db_name = config["db_name"]
  try:
    conn = psycopg2.connect(config["admin_url"])
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name, ))
    exists = cursor.fetchone()

    if not exists:
      logger.info('No database found. Creating a new one')
      _create_db(config)
    else:
      logger.debug('Database found. Skip')

    cursor.close()
    conn.close()
  except Exception as e:
    logger.info('Error creating DB')
    logger.debug(e)


def _create_db(config: dict):
  db_name = config["db_name"]
  user = config["user"]
  password = config["password"]
  host = config["host"]
  port = config["port"]

  # Paso 1: crear base de datos desde postgres
  conn = psycopg2.connect(dbname="postgres",
                          user=user,
                          password=password,
                          host=host,
                          port=port)
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()

  try:
    cursor.execute(f"CREATE DATABASE {db_name}")
    logger.info(f'Database {db_name} created!')
  except psycopg2.errors.DuplicateDatabase:
    logger.debug(f'Database already exists')
  finally:
    cursor.close()
    conn.close()

  # Paso 2: crear schemas dentro de la nueva base
  conn = psycopg2.connect(dbname=db_name,
                          user=user,
                          password=password,
                          host=host,
                          port=port)
  cursor = conn.cursor()

  for schema in ["machine", "os", "apps"]:
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    print(f"[✔] Schema '{schema}' creado.")

  conn.commit()
  cursor.close()
  conn.close()
  print("[✔] Todo listo.")
