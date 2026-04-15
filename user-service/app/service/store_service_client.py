import os
import requests

STORE_SERVICE_BASE_URL = os.getenv("STORE_SERVICE_BASE_URL", "http://store-service:8002")
SECRET_KEY = os.getenv("SECRET_KEY", "")

TIMEOUT = 10


async def delete_user_data_in_store_service(user_id: int) -> None:
    url = f"{STORE_SERVICE_BASE_URL}/internal/users/{user_id}"

    response = requests.delete(
        url,
        headers={
            "X-Internal-Secret": SECRET_KEY,
        },
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to delete user data from store-service: "
            f"{response.status_code} {response.text}"
        )