import asyncio
from fastapi import FastAPI

from app.repository.database import database
from app.repository.migration_runner import run_migrations
from app.scripts.seed_items import seed_items

from app.controller.items_controller import router as items_router
from app.controller.orders_controller import router as orders_router
from app.controller.auth_controller import router as auth_router
from app.controller.favorites_controller import router as favorites_router
from app.controller.chat_controller import router as chat_router
from app.controller.internal_controller import router as internal_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    for i in range(10):
        try:
            await database.connect()
            print("DB connected")
            break
        except Exception:
            print(f"DB not ready {i + 1}/10")
            await asyncio.sleep(2)
    else:
        raise Exception("Failed to connect to DB after retries")

    await run_migrations()
    await seed_items()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router)
app.include_router(items_router)
app.include_router(orders_router)
app.include_router(favorites_router)
app.include_router(chat_router)
app.include_router(internal_router)


@app.get("/health")
async def health():
    return {"status": "ok"}