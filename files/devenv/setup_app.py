#!/usr/bin/python3
import subprocess

with open(".env", "r") as input_file:
    lines = input_file.readlines()
    env_variables = {
        key: value.strip('"\n') for (key, value) in [line.split("=") for line in lines]
    }

DB_NAME = env_variables.get("AHERNP_DATABASE_NAME")
DB_USER = env_variables.get("AHERNP_DATABASE_USER")
DB_PASSWORD = env_variables.get("AHERNP_DATABASE_PASSWORD")


def run(command):
    try:
        print(command)
        subprocess.call(command, shell=True)
    except OSError as e:
        print(f"{command} {e}")


def setup_postgres():
    commands = [
        f"CREATE DATABASE {DB_NAME};",
        f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';",
        f"ALTER ROLE {DB_USER} SET client_encoding TO 'utf8';",
        f"ALTER ROLE {DB_USER} SET default_transaction_isolation TO 'read committed';",
        f"ALTER ROLE {DB_USER} SET timezone TO 'UTC';",
        f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};",
        f"ALTER USER {DB_USER} CREATEDB;",
    ]
    for command in commands:
        run(f'sudo docker-compose exec db psql -U postgres -c "{command}"')


def setup_webapp():
    commands = [
        "migrate",
        "loaddata project/fixtures/live_snapshot.json",
        # "poll_feeds --verbose",
        "createsuperuser",
        "collectstatic",
    ]
    for command in commands:
        run(f"sudo docker-compose exec webapp python manage.py {command}")


if __name__ == "__main__":
    setup_postgres()
    setup_webapp()
