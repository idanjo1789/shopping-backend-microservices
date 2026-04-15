import streamlit as st


def init_session_state() -> None:
    if "token" not in st.session_state:
        st.session_state["token"] = None

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"


def set_auth(token: str) -> None:
    st.session_state["token"] = token


def is_authenticated() -> bool:
    return bool(st.session_state.get("token"))


def require_auth() -> None:
    if not is_authenticated():
        st.warning("Please login to continue.")
        st.stop()


def logout() -> None:
    st.session_state["token"] = None
    st.session_state["page"] = "Home"

    keys_to_clear = [
        "store_chat_messages",
        "store_chat_session_key",
        "chat_messages_by_item",
        "chat_count_by_item",
        "selected_chat_item_id",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]