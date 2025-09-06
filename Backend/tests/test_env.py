import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

print(f"Directorio actual: {BASE_DIR}")
print(f"Buscando .env en: {env_path}")
print(f"Archivo .env existe: {env_path.exists()}")

if env_path.exists():
    with open(env_path, 'r') as f:
        print(f"Contenido del .env:")
        print(f.read())

print("\n--- Cargando variables ---")
load_dotenv(env_path)

print(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB')}")
print(f"POSTGRES_USER: {os.environ.get('POSTGRES_USER')}")
print(f"POSTGRES_PASSWORD: {os.environ.get('POSTGRES_PASSWORD')}")
print(f"DB_HOST: {os.environ.get('DB_HOST')}")
print(f"DB_PORT: {os.environ.get('DB_PORT')}")