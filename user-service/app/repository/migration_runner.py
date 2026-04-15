from pathlib import Path

from app.repository.database import database


MIGRATIONS_PATH = Path(__file__).resolve().parent.parent / "resources" / "db-migrations"


async def run_migrations():
    if not MIGRATIONS_PATH.exists():
        raise FileNotFoundError(f"Migrations path not found: {MIGRATIONS_PATH}")

    files = sorted(MIGRATIONS_PATH.glob("*.sql"))

    for file_path in files:
        query = file_path.read_text(encoding="utf-8")
        statements = [q.strip() for q in query.split(";") if q.strip()]

        for stmt in statements:
            await database.execute(stmt)