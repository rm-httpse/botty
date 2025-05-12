import os
import platform
import getpass
import socket
import re
from pathlib import Path
from dotenv import load_dotenv
from src.db.flyway import run_migrations, repair_migrations

class ConfigLoader:
    def __init__(self, env_path: str = ".env"):
        load_dotenv(env_path)
        self._load_config()

    def _load_config(self):
        self.db_url = self._get("DB_URL")
        self.ms_uri = self._get("MS_URI")
        self.namespace = self._get("IO_NAMESPACE")
        self.migrations_path = Path(self._get("DB_MIG_PATH", "src/db/migrations"))

    def _get(self, key: str, default=None):
        return os.getenv(key, default)
    
    def _get_next_version(self):
        existing_files = list(self.migrations_path.glob("V*__*.sql"))
        versions = []
        version_pattern = r"V(\d+)__"
        for file in existing_files:
            match = re.match(version_pattern, file.name)
            if match:
                versions.append(int(match.group(1)))
        return max(versions) + 1 if versions else 1

    def load_or_create_user(self):
        username = getpass.getuser()
        hostname = socket.gethostname()
        os_name = platform.system()
        os_version = platform.version()

        print(f"[*] Registrando usuario '{username}' en schema 'machine'...")

        self.migrations_path.mkdir(parents=True, exist_ok=True)

        user_mig_pattern = f"machine_create_user_{username}"
        existing = list(self.migrations_path.glob(f"*__{user_mig_pattern}.sql"))
        if not existing:
            version = self._get_next_version()
            mig_file = self.migrations_path / f"V{version}__{user_mig_pattern}.sql"
            mig_template = Path("src/db/init/machine.sql").read_text()
            mig_content = mig_template.format(
                          username=username,
                          hostname=hostname,
                          os_name=os_name,
                          os_version=os_version
                      )
            mig_file.write_text(mig_content.strip())
            print(f"  ✔ Creada migración de usuario: {mig_file.name}")
        else:
            print(f"  ~ Migración de usuario ya existe: {existing[0].name}")
        
        return {
            "username": getpass.getuser(),
            "hostname": socket.gethostname(),
            "os_name": platform.system(),
            "os_version": platform.version(),
        }

    def run_migrations(self):
        run_migrations(self.db_url, str(self.migrations_path))
