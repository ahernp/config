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
        print("{command} {e}".format(command=command, e=e))


def setup_postgres():
    sql_execute = 'sudo docker-compose exec db psql -U postgres -c "{command}"'
    commands = [
        "CREATE DATABASE {db_name};".format(db_name=DB_NAME),
        "CREATE USER {db_user} WITH PASSWORD '{db_password}';".format(
            db_user=DB_USER, db_password=DB_PASSWORD
        ),
        "ALTER ROLE {db_user} SET client_encoding TO 'utf8';".format(db_user=DB_USER),
        "ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';".format(
            db_user=DB_USER
        ),
        "ALTER ROLE {db_user} SET timezone TO 'UTC';".format(db_user=DB_USER),
        "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};".format(
            db_name=DB_NAME, db_user=DB_USER
        ),
        "ALTER USER {db_user} CREATEDB;".format(db_user=DB_USER),
    ]
    for command in commands:
        run(sql_execute.format(command=command))


def setup_webapp():
    execute = "sudo docker-compose exec webapp python manage.py {command}"
    commands = [
        "migrate",
        "loaddata project/fixtures/live_snapshot.json",
        # "poll_feeds --verbose",
        "createsuperuser",
        "collectstatic",
    ]
    for command in commands:
        run(execute.format(command=command))


if __name__ == "__main__":
    setup_postgres()
    setup_webapp()
