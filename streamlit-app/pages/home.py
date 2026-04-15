import streamlit as st

from services.auth import set_auth, is_authenticated
from services.api_client import post, get


def render() -> None:
    st.title("Account")

    if is_authenticated():
        _render_logged_in_view()
        return

    st.info("Please login or create an account.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        _render_login()

    with tab2:
        _render_register()

    st.divider()
    _render_system_status()


def _render_logged_in_view() -> None:
    st.success("You are logged in.")

    response = get("/users/me", service="user")

    if response.status_code != 200:
        st.warning("Could not load user details.")
        _render_system_status()
        return

    user = response.json()

    st.subheader("User Details")
    st.write(f"**Username:** {user.get('username', '-')}")
    st.write(f"**First Name:** {user.get('first_name', '-')}")
    st.write(f"**Last Name:** {user.get('last_name', '-')}")
    st.write(f"**Email:** {user.get('email', '-')}")
    st.write(f"**Phone:** {user.get('phone', '-')}")
    st.write(f"**Country:** {user.get('country', '-')}")
    st.write(f"**City:** {user.get('city', '-')}")

    st.divider()
    _render_system_status()


def _render_login() -> None:
    st.subheader("Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if not username or not password:
            st.warning("Please enter username and password.")
            return

        response = post(
            endpoint="/auth/login",
            data={
                "username": username,
                "password": password,
            },
            service="user",
            auth=False,
            is_form=True,
        )

        if response.status_code == 200:
            token = response.json().get("access_token")

            if not token:
                st.error("No token returned.")
                return

            set_auth(token)
            st.session_state["page"] = "Shop"
            st.success("Login successful.")
            st.rerun()

        st.error(f"Login failed: {response.text}")


def _render_register() -> None:
    st.subheader("Register")

    username = st.text_input("Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    first_name = st.text_input("First Name", key="reg_first_name")
    last_name = st.text_input("Last Name", key="reg_last_name")
    phone = st.text_input("Phone", key="reg_phone")
    country = st.text_input("Country", key="reg_country")
    city = st.text_input("City", key="reg_city")
    password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Create Account", key="register_button"):
        if not username or not email or not first_name or not last_name or not phone or not country or not city or not password:
            st.warning("Please fill all fields.")
            return

        response = post(
            endpoint="/users",
            data={
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "country": country,
                "city": city,
                "password": password,
            },
            service="user",
            auth=False,
        )

        if response.status_code in (200, 201):
            st.success("Account created successfully. You can login now.")
        else:
            st.error(f"Registration failed: {response.text}")


def _render_system_status() -> None:
    st.subheader("System Status")

    user_health = get("/health", service="user", auth=False)
    store_health = get("/health", service="store", auth=False)

    col1, col2 = st.columns(2)

    with col1:
        if user_health.status_code == 200:
            st.success("User Service OK")
        else:
            st.error("User Service Down")

    with col2:
        if store_health.status_code == 200:
            st.success("Store Service OK")
        else:
            st.error("Store Service Down")