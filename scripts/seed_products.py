import asyncio
from databases import Database

DATABASE_URL = "mysql+aiomysql://root:root@mysql-store:3306/store_db"

database = Database(DATABASE_URL)

ITEMS = [
    {"name": "JBL Tune Buds 2 Ghost Edition", "price": 450, "stock": 50},
    {"name": "JBL Charge 6", "price": 750, "stock": 30},
    {"name": "JBL Cinema SB580 3.1 Dolby Atmos", "price": 1800, "stock": 10},
    {"name": "JBL Flip 7", "price": 550, "stock": 40},
    {"name": "JBL PartyBox 720", "price": 3200, "stock": 5},
    {"name": "JBL PartyBox On-The-Go 2", "price": 1400, "stock": 12},
    {"name": "JBL Tune 510BT", "price": 220, "stock": 60},
    {"name": "PartyBox Club 120 (Battery)", "price": 300, "stock": 25},
    {"name": "PartyBox Microphone", "price": 180, "stock": 40},
]


async def seed_items():
    await database.connect()

    for item in ITEMS:

        query_check = """
        SELECT id FROM items WHERE name = :name
        """

        exists = await database.fetch_one(query_check, values={"name": item["name"]})

        if exists:
            print(f"Item already exists: {item['name']}")
            continue

        query_insert = """
        INSERT INTO items (name, price, stock)
        VALUES (:name, :price, :stock)
        """

        await database.execute(query_insert, values=item)

        print(f"Inserted: {item['name']}")

    await database.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_items())