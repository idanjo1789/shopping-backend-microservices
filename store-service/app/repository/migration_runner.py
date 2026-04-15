import os

from app.repository.database import database

MIGRATIONS_DIR = "app/resources/db-migrations"


async def run_migrations() -> None:
    if not os.path.isdir(MIGRATIONS_DIR):
        print(f"Migrations directory not found: {MIGRATIONS_DIR}")
        return

    sql_files = sorted(
        [
            file_name
            for file_name in os.listdir(MIGRATIONS_DIR)
            if file_name.endswith(".sql")
        ]
    )

    for file_name in sql_files:
        file_path = os.path.join(MIGRATIONS_DIR, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            sql_content = file.read()

        statements = [
            statement.strip()
            for statement in sql_content.split(";")
            if statement.strip()
        ]

        for statement in statements:
            await database.execute(statement)

        print(f"Migration applied: {file_name}")