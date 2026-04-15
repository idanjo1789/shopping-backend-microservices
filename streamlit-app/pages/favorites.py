import os
import pandas as pd
import streamlit as st

from services.auth import require_auth
from services.api_client import get, post, delete

IMAGE_FOLDER = "assets/images"


def _get_image_path(item_name: str) -> str:
    safe_name = (item_name or "unknown").replace(" ", "_")
    return os.path.join(IMAGE_FOLDER, f"{safe_name}.jpg")


def render() -> None:
    require_auth()

    st.title("Favorite Items")

    response = get("/favorites", service="store")

    if response.status_code != 200:
        st.error(f"Failed to load favorites: {response.text}")
        return

    favorites = response.json()

    if not isinstance(favorites, list):
        st.error("Invalid favorites response.")
        return

    if not favorites:
        st.info("No favorite items yet.")
        return

    _render_favorites_dataframe(favorites)

    st.divider()

    for item in favorites:
        _render_favorite_card(item)


def _render_favorites_dataframe(items: list[dict]) -> None:
    rows = []

    for item in items:
        rows.append(
            {
                "ID": item.get("id"),
                "Name": item.get("name"),
                "Price (USD)": float(item.get("price", 0) or 0),
                "Stock": int(item.get("stock", 0) or 0),
                "Description": item.get("description") or "No description",
            }
        )

    df = pd.DataFrame(rows)
    st.subheader("Favorites Data")
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_favorite_card(item: dict) -> None:
    item_id = int(item.get("id", 0) or 0)
    item_name = item.get("name", "Unknown Item")
    price = float(item.get("price", 0) or 0)
    stock = int(item.get("stock", 0) or 0)
    description = item.get("description") or "No description"

    col1, col2 = st.columns([1, 3])

    with col1:
        image_path = _get_image_path(item_name)
        if os.path.exists(image_path):
            st.image(image_path, width=130)
        else:
            st.write("No image")

    with col2:
        st.subheader(item_name)
        st.write(f"Price: $ {price:.2f}")
        st.write(f"Stock: {stock}")
        st.write(f"Description: {description}")

        qty = st.number_input(
            f"Quantity for favorite item {item_id}",
            min_value=1,
            value=1,
            step=1,
            key=f"fav_qty_{item_id}",
        )

        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.button(
                "Add to Order",
                key=f"fav_add_{item_id}",
                disabled=stock <= 0,
            ):
                _add_to_order(item_id, int(qty))

        with btn_col2:
            if st.button("Remove from Favorites", key=f"fav_remove_{item_id}"):
                _remove_favorite(item_id)

    st.divider()


def _add_to_order(item_id: int, quantity: int) -> None:
    response = post(
        "/orders/temp/items",
        data={
            "item_id": item_id,
            "quantity": quantity,
        },
        service="store",
    )

    if response.status_code in (200, 201):
        st.success("Item added to order.")
    else:
        st.error(f"Failed: {response.text}")


def _remove_favorite(item_id: int) -> None:
    response = delete(f"/favorites/{item_id}", service="store")

    if response.status_code == 200:
        st.success("Removed from favorites.")
        st.rerun()
    else:
        st.error(f"Failed: {response.text}")