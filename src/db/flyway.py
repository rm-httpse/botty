import subprocess
import urllib.parse

def run_migrations(db_url: str, migrations_path: str = "src/db/migrations"):
    parsed = urllib.parse.urlparse(db_url)

    flyway_cmd = [
        "flyway",
        f"-url=jdbc:postgresql://{parsed.hostname}:{parsed.port}{parsed.path}",
        f"-user={parsed.username}",
        f"-password={parsed.password}",
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

def repair_migrations(db_url: str, migrations_path: str = "src/db/migrations"):
    parsed = urllib.parse.urlparse(db_url)
    
    flyway_cmd = [
        "flyway",
        f"-url=jdbc:postgresql://{parsed.hostname}:{parsed.port}{parsed.path}",
        f"-user={parsed.username}",
        f"-password={parsed.password}",
        f"-locations=filesystem:{migrations_path}",
        "repair"
    ]

    try:
        print("[*] Ejecutando reparación con Flyway...")
        result = subprocess.run(flyway_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[✔] Reparación completada:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error durante la reparación: {e.stderr.decode()}")
