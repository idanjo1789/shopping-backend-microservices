from services.api_client import post


def ask_store_chat(message: str) -> dict:
    response = post(
        "/chat/ask",
        data={"message": message},
        service="store",
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()