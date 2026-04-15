from app.repository.database import database


ITEMS = [
    {"name": "JBL Charge 6", "description": "Portable Bluetooth speaker", "price": 750, "stock": 30},
    {"name": "JBL Cinema SB580 3.1 Dolby Atmos", "description": "Soundbar system", "price": 1800, "stock": 10},
    {"name": "JBL FLIP 7", "description": "Compact waterproof speaker", "price": 550, "stock": 40},
    {"name": "JBL PartyBox 720", "description": "Party speaker with lights", "price": 3200, "stock": 5},
    {"name": "JBL PartyBox On-The-Go 2", "description": "Portable party speaker with mic", "price": 1400, "stock": 12},
    {"name": "JBL Tune 510BT", "description": "Wireless headphones", "price": 220, "stock": 60},
    {"name": "JBL Tune Beam 2 In-Ear True Wireless", "description": "True wireless earbuds", "price": 450, "stock": 50},
    {"name": "PartyBox Club 120", "description": "Party speaker battery", "price": 300, "stock": 25},
    {"name": "PartyBox", "description": "General party speaker", "price": 2000, "stock": 8},
    {"name": "Tune Buds 2 Ghost Edition", "description": "Wireless earbuds special edition", "price": 450, "stock": 50},
]


async def seed_items():
    print("START SEED ITEMS")

    count_query = "SELECT COUNT(*) as count FROM items"
    result = await database.fetch_one(count_query)

    if result["count"] > 0:
        print("⏩ Items already exist, skipping seed")
        return

    insert_query = """
    INSERT INTO items (name, description, price, stock, is_active)
    VALUES (:name, :description, :price, :stock, 1)
    """

    for item in ITEMS:
        try:
            await database.execute(query=insert_query, values=item)
            print(f"Inserted: {item['name']}")
        except Exception as e:
            print(f"Failed: {item['name']} | {e}")

    print("SEED DONE")