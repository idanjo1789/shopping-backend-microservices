import streamlit as st

from services.auth import init_session_state, is_authenticated, logout
from pages.shop import render as render_shop
from pages.favorites import render as render_favorites
from pages.orders import render as render_orders
from pages.chat import render as render_chat
from pages.home import render as render_home

PROTECTED_PAGES = {"Favorites", "Orders", "Chat"}


def main() -> None:
    st.set_page_config(
        page_title="Shopping Website",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_session_state()

    if "page" not in st.session_state:
        st.session_state["page"] = "Shop"

    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("Shop"):
        st.session_state["page"] = "Shop"

    if col2.button("Favorites"):
        st.session_state["page"] = "Favorites"

    if col3.button("Orders"):
        st.session_state["page"] = "Orders"

    if col4.button("Chat"):
        st.session_state["page"] = "Chat"

    if is_authenticated():
        if col5.button("Logout"):
            logout()
            st.rerun()
    else:
        if col5.button("Login"):
            st.session_state["page"] = "Login"

    page = st.session_state["page"]

    if page in PROTECTED_PAGES and not is_authenticated():
        st.warning("Please login to access this page.")
        page = "Shop"
        st.session_state["page"] = "Shop"

    st.divider()

    if page == "Shop":
        render_shop()
    elif page == "Favorites":
        render_favorites()
    elif page == "Orders":
        render_orders()
    elif page == "Chat":
        render_chat()
    elif page == "Login":
        render_home()
    else:
        render_shop()


if __name__ == "__main__":
    main()