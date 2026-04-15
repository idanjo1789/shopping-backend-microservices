import os
import re
import base64
import pandas as pd
import streamlit as st

from services.auth import is_authenticated
from services.api_client import get, post

IMAGE_FOLDER = "assets/images"
CARDS_PER_ROW = 4


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()


def _get_image_html(item_name: str) -> str:
    safe_name = (item_name or "unknown").replace(" ", "_")
    image_path = os.path.join(IMAGE_FOLDER, f"{safe_name}.jpg")

    if os.path.exists(image_path):
        encoded_image = _image_to_base64(image_path)
        return f'<img src="data:image/jpg;base64,{encoded_image}"/>'

    return "<div class='no-image'>No image</div>"


def _apply_style() -> None:
    st.markdown(
        """
        <style>
        .card {
            border: 1px solid #dddddd;
            border-radius: 16px;
            padding: 12px;
            height: 560px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-align: center;
            background-color: #fafafa;
            margin-bottom: 12px;
        }

        .img-container {
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .img-container img {
            max-height: 100%;
            max-width: 100%;
            object-fit: contain;
        }

        .no-image {
            color: gray;
            font-size: 13px;
        }

        .title {
            font-weight: bold;
            font-size: 15px;
            margin-top: 8px;
            min-height: 40px;
        }

        .price {
            color: green;
            font-weight: bold;
            font-size: 14px;
            margin-top: 6px;
        }

        .stock {
            font-size: 12px;
            color: gray;
            margin-top: 6px;
        }

        .description {
            font-size: 13px;
            color: #444444;
            margin-top: 10px;
            min-height: 72px;
            overflow: hidden;
        }

        .favorite-indicator {
            margin-top: 8px;
            font-size: 13px;
            font-weight: bold;
            color: #c2185b;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    st.title("Shopping Website")
    st.subheader("Shop")

    _apply_style()

    search_value = st.text_input(
        "Search",
        placeholder='Examples: JBL | >500 | =300 | Flip, Charge',
    )

    search_params = _parse_search_input(search_value)
    items = _load_items(search_params)

    if items is None:
        return

    if not items:
        st.warning("No items found.")
        return

    favorite_ids = _load_favorite_ids()

    st.subheader("Available Items")
    _render_items_dataframe(items, favorite_ids)

    st.divider()
    st.subheader("Items Grid")
    _render_items_grid(items, favorite_ids)


def _parse_search_input(search_value: str) -> dict:
    value = (search_value or "").strip()

    if not value:
        return {}

    price_match = re.fullmatch(r"([<>=])\s*(\d+(?:\.\d+)?)", value)
    if price_match:
        operator_symbol = price_match.group(1)
        numeric_value = float(price_match.group(2))

        operator_map = {
            "<": "lt",
            ">": "gt",
            "=": "eq",
        }

        return {
            "price_op": operator_map[operator_symbol],
            "price_value": numeric_value,
        }

    if "," in value:
        keywords = [part.strip() for part in value.split(",") if part.strip()]
        if keywords:
            return {"name": ",".join(keywords)}

    return {"name": value}


def _load_items(params: dict) -> list[dict] | None:
    if params:
        response = get(
            "/items/search",
            service="store",
            auth=False,
            params=params,
        )
    else:
        response = get("/items", service="store", auth=False)

    if response.status_code != 200:
        st.error(f"Failed to load items: {response.text}")
        return None

    return response.json()


def _load_favorite_ids() -> set[int]:
    if not is_authenticated():
        return set()

    response = get("/favorites", service="store")

    if response.status_code != 200:
        return set()

    favorites = response.json()

    if not isinstance(favorites, list):
        return set()

    return {
        int(item.get("id"))
        for item in favorites
        if item.get("id") is not None
    }


def _render_items_dataframe(items: list[dict], favorite_ids: set[int]) -> None:
    rows = []

    for item in items:
        item_id = int(item.get("id", 0) or 0)

        rows.append(
            {
                "ID": item_id,
                "Name": item.get("name"),
                "Price (USD)": float(item.get("price", 0) or 0),
                "Stock": int(item.get("stock", 0) or 0),
                "Favorite": "Yes" if item_id in favorite_ids else "No",
                "Description": item.get("description") or "No description",
            }
        )

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_items_grid(items: list[dict], favorite_ids: set[int]) -> None:
    for index in range(0, len(items), CARDS_PER_ROW):
        row_items = items[index:index + CARDS_PER_ROW]
        columns = st.columns(CARDS_PER_ROW)

        for column, item in zip(columns, row_items):
            with column:
                _render_item_card(item, favorite_ids)


def _render_item_card(item: dict, favorite_ids: set[int]) -> None:
    item_id = int(item.get("id", 0) or 0)
    item_name = item.get("name", "Unknown Item")
    description = item.get("description") or "No description available"
    stock = int(item.get("stock", 0) or 0)
    price = float(item.get("price", 0) or 0)
    is_favorite = item_id in favorite_ids

    image_html = _get_image_html(item_name)

    favorite_html = (
        "<div class='favorite-indicator'>♥ In Favorites</div>"
        if is_favorite
        else "<div class='favorite-indicator'>♡ Not in Favorites</div>"
    )

    card_html = f"""
    <div class="card">
        <div class="img-container">
            {image_html}
        </div>
        <div class="title">{item_name}</div>
        <div class="price">$ {price:.2f}</div>
        <div class="stock">
            {"In stock" if stock > 0 else "Out of stock"} | Stock: {stock}
        </div>
        <div class="description">
            {description}
        </div>
        {favorite_html}
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
    _render_actions(item, is_favorite)


def _render_actions(item: dict, is_favorite: bool) -> None:
    item_id = int(item.get("id", 0) or 0)
    stock = int(item.get("stock", 0) or 0)

    if not is_authenticated():
        st.info("Login to add items to order or favorites.")
        return

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Add to Order",
            key=f"cart_{item_id}",
            disabled=stock <= 0,
        ):
            response = post(
                "/orders/temp/items",
                data={
                    "item_id": item_id,
                    "quantity": 1,
                },
                service="store",
            )

            if response.status_code in (200, 201):
                st.success("Item added to order.")
            else:
                st.error(response.text)

    with col2:
        button_label = "In Favorites" if is_favorite else "Add to Favorites"

        if st.button(
            button_label,
            key=f"fav_{item_id}",
            disabled=is_favorite,
        ):
            response = post(
                "/favorites",
                data={"item_id": item_id},
                service="store",
            )

            if response.status_code in (200, 201):
                st.success("Item added to favorites.")
                st.rerun()
            else:
                st.error(response.text)