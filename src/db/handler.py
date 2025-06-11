import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from urllib.parse import urlparse
from src.utils.logger import get_logger

logger = get_logger("DBHandler")

class DBHandler:
  def __init__(self, db_url: str):
    self.conn_config = self.get_db_config(db_url)
    self.connection = self.get_connection(db_url)
    logger.debug("Database connection initialized")


def get_connection(db_url: str):
  parsed = urlparse(db_url)
  conn = None
  while not conn:
    try:
      conn = psycopg2.connect(
        dbname=parsed.dbname,
        user=parsed.user,
        password=parsed.password,
        host=parsed.host,
        port=parsed.port
      )
      conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
      return conn
    except psycopg2.OperationalError as err: # handle to create
      print(err)
  

  
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

    # cambiar para referenciar un archivo con esta query
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

  conn = psycopg2.connect(dbname="postgres",
                          user=user,
                          password=password,
                          host=host,
                          port=port)
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
  cursor = conn.cursor()

  try:
    # esto tambien cambiar a una query de un archivo
    cursor.execute(f"CREATE DATABASE {db_name}")
    logger.info(f'Database {db_name} created!')
  except psycopg2.errors.DuplicateDatabase:
    logger.debug(f'Database already exists')
  finally:
    cursor.close()
    conn.close()

  conn.commit()
  cursor.close()
  conn.close()
  print("[✔] Todo listo.")
