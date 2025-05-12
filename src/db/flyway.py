import subprocess
import urllib.parse
import logging

from src.utils.logger import get_logger

logger = get_logger("Flyway", logging.INFO)


def run_migrations(db_url: str, migrations_path: str = "src/db/migrations"):
  parsed = urllib.parse.urlparse(db_url)

  flyway_cmd = [
      "flyway",
      f"-url=jdbc:postgresql://{parsed.hostname}:{parsed.port}{parsed.path}",
      f"-user={parsed.username}", f"-password={parsed.password}",
      f"-locations=filesystem:{migrations_path}", "migrate"
  ]

  try:
    logger.info(f'Flyway on its way')
    result = subprocess.run(flyway_cmd,
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    logger.info(f'Migrations applied!')
    logger.debug({result.stdout.decode()})
  except subprocess.CalledProcessError as e:
    print(f"[!] Error aplicando migraciones: {e.stderr.decode()}")
    logger.debug(f'Error while running migrations')
    logger.debug({result.stdout.decode()})
