from fastapi import FastAPI
import asyncio

from app.repository.database import database
from app.controller.user_controller import router as user_router
from app.controller.auth_controller import router as auth_router
from app.repository.migration_runner import run_migrations

app = FastAPI()


@app.on_event("startup")
async def startup():
    for i in range(10):
        try:
            if not database.is_connected:
                await database.connect()
            print("DB connected")
            break
        except Exception as e:
            print(f"DB not ready... retry {i + 1}/10 | error: {e}")
            await asyncio.sleep(2)
    else:
        raise Exception("Failed to connect to DB after retries")

    await run_migrations()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(auth_router)
app.include_router(user_router)


@app.get("/health")
async def health():
    return {"status": "ok"}