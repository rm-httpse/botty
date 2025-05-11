import subprocess
import os

def run_migrations(db_url: str, migrations_path: str = "src/db/migrations"):
    """
    Ejecuta las migraciones usando Flyway desde el código, sin necesidad de interactuar con CLI.
    Asegúrate de que Flyway esté instalado y disponible en el entorno donde se ejecute este código.
    """
    # Configura los parámetros de Flyway
    flyway_cmd = [
        "flyway",
        f"-url={db_url}",
        f"-user=postgres",
        f"-password=masterkey",
        f"-locations=filesystem:{migrations_path}",
        "migrate"
    ]

    try:
        # Ejecuta el comando Flyway
        print("[*] Ejecutando migraciones con Flyway...")
        result = subprocess.run(flyway_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[✔] Migraciones aplicadas correctamente:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error aplicando migraciones: {e.stderr.decode()}")
