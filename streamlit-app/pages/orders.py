import os
import streamlit as st

from services.auth import require_auth
from services.api_client import get, post, delete

IMAGE_FOLDER = "assets/images"


def _get_image_path(item_name: str) -> str:
    safe_name = (item_name or "unknown").replace(" ", "_")
    return os.path.join(IMAGE_FOLDER, f"{safe_name}.jpg")


def render() -> None:
    require_auth()

    st.title("Orders")

    _render_temp_order()

    st.divider()

    _render_order_history()


def _render_temp_order() -> None:
    st.subheader("Current TEMP Order")

    response = get("/orders/temp", service="store")

    if response.status_code != 200:
        st.info("No active TEMP order.")
        return

    data = response.json()
    order = data.get("order", {})
    items = data.get("items", [])

    if not items:
        st.info("TEMP order is empty.")
        return

    st.write(f"**Order ID:** {order.get('id')}")
    st.write(f"**Status:** {order.get('status')}")
    st.write(f"**Total Price:** $ {float(order.get('total_price', 0) or 0):.2f}")
    st.write("**Shipping Address:** Not available yet")

    st.divider()

    for item in items:
        _render_order_item_card(item, width=120)

    st.subheader("Modify Item")

    item_options = {
        f"{item.get('name', 'Unknown Item')} (ID: {item.get('item_id')})": item
        for item in items
    }

    selected_label = st.selectbox("Select Item", list(item_options.keys()))
    selected_item = item_options[selected_label]

    selected_item_id = int(selected_item.get("item_id"))
    current_quantity = int(selected_item.get("quantity", 1) or 1)
    max_stock = int(selected_item.get("stock", 0) or 0)

    col1, col2 = st.columns(2)

    with col1:
        if max_stock <= 0:
            st.warning("This item is out of stock.")
        else:
            new_quantity = st.number_input(
                "New Quantity",
                min_value=1,
                max_value=max_stock,
                value=min(current_quantity, max_stock),
                step=1,
                key=f"qty_update_{selected_item_id}",
            )

            if st.button("Update Quantity", key=f"update_quantity_{selected_item_id}"):
                _update_quantity(selected_item_id, int(new_quantity), max_stock)

    with col2:
        if st.button("Remove Item", key=f"remove_item_{selected_item_id}"):
            _remove_item(selected_item_id)

    st.divider()

    if st.button("Purchase Order", key="close_order_button"):
        invalid_items = [
            item for item in items
            if int(item.get("quantity", 0) or 0) > int(item.get("stock", 0) or 0)
        ]

        if invalid_items:
            st.error("Cannot purchase order. One or more items exceed available stock.")
            return

        _close_order()


def _render_order_item_card(item: dict, width: int) -> None:
    item_name = item.get("name", "Unknown Item")
    price = float(item.get("price", 0) or 0)
    quantity = int(item.get("quantity", 0) or 0)
    stock = int(item.get("stock", 0) or 0)
    description = item.get("description") or "No description"

    col1, col2 = st.columns([1, 3])

    with col1:
        image_path = _get_image_path(item_name)
        if os.path.exists(image_path):
            st.image(image_path, width=width)
        else:
            st.write("No image")

    with col2:
        st.write(f"**{item_name}**")
        st.write(f"Price: $ {price:.2f}")
        st.write(f"Quantity: {quantity}")
        st.write(f"Stock: {stock}")
        st.write(f"Total: $ {price * quantity:.2f}")
        st.write(f"Description: {description}")

        if stock == 0:
            st.warning("This item is currently out of stock.")
        elif quantity > stock:
            st.error("Current quantity is higher than available stock.")


    st.divider()


def _update_quantity(item_id: int, quantity: int, max_stock: int) -> None:
    if quantity > max_stock:
        st.error(f"You cannot order more than available stock ({max_stock}).")
        return

    response = post(
        "/orders/temp/items/update",
        data={"item_id": item_id, "quantity": quantity},
        service="store",
    )

    if response.status_code == 200:
        st.success("Quantity updated.")
        st.rerun()
    else:
        st.error(f"Failed: {response.text}")


def _remove_item(item_id: int) -> None:
    response = delete(f"/orders/temp/items/{item_id}", service="store")

    if response.status_code != 200:
        st.error(f"Failed: {response.text}")
        return

    data = response.json()

    if data.get("order_deleted"):
        st.success("The TEMP order became empty and was deleted.")
    else:
        st.success("Item removed.")

    st.rerun()


def _close_order() -> None:
    response = post("/orders/temp/close", data={}, service="store")

    if response.status_code == 200:
        st.success("Order purchased successfully.")
        st.rerun()
    else:
        st.error(f"Purchase failed: {response.text}")


def _render_order_history() -> None:
    st.subheader("Closed Orders")

    response = get("/orders/history", service="store")

    if response.status_code != 200:
        st.warning("Could not load order history.")
        return

    orders = response.json()

    if not orders:
        st.info("No closed orders found.")
        return

    for order in orders:
        st.markdown(f"### Order ID: {order.get('id')}")
        st.write(f"**Status:** {order.get('status')}")
        st.write(f"**Total Price:** $ {float(order.get('total_price', 0) or 0):.2f}")
        st.write("**Shipping Address:** Not available yet")

        items = order.get("items", [])

        if not items:
            st.info("No items in this order.")
            st.divider()
            continue

        st.divider()

        for item in items:
            _render_order_item_card(item, width=100)