from openai import OpenAI

from app.exceptions import bad_request
from app.repository import items_repository

client = OpenAI()


def _build_catalog_text(items: list) -> str:
    lines = []

    for item in items:
        stock = int(item.stock or 0)
        availability = "In stock" if stock > 0 else "Out of stock"

        lines.append(
            f"- Name: {item.name} | "
            f"Price: ${float(item.price):.2f} | "
            f"Stock: {stock} | "
            f"Availability: {availability} | "
            f"Description: {item.description or 'No description'}"
        )

    return "\n".join(lines)


async def ask_store_question(user_id: int, message: str) -> dict:
    clean_message = (message or "").strip()

    if not clean_message:
        raise bad_request("Message is required")

    items = await items_repository.get_all()
    catalog_text = _build_catalog_text(items)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a shopping assistant for an online store. "
                    "Answer only based on the provided catalog data. "
                    "You must know products that are in stock and out of stock. "
                    "Do not invent product details. "
                    "If the requested information does not exist in the catalog, say that clearly. "
                    "Keep answers short, clear, and helpful."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Store catalog:\n{catalog_text}\n\n"
                    f"User question:\n{clean_message}"
                ),
            },
        ],
        temperature=0.3,
    )

    answer = completion.choices[0].message.content.strip()

    return {
        "answer": answer,
    }