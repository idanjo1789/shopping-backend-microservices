import os
import requests
import streamlit as st

USER_SERVICE_BASE_URL = os.getenv("USER_SERVICE_BASE_URL", "http://user-service:8001")
STORE_SERVICE_BASE_URL = os.getenv("STORE_SERVICE_BASE_URL", "http://store-service:8002")

TIMEOUT = 10


def _get_base_url(service: str) -> str:
    return STORE_SERVICE_BASE_URL if service == "store" else USER_SERVICE_BASE_URL


def _get_headers(auth: bool = True, is_form: bool = False) -> dict:
    headers = {}

    if not is_form:
        headers["Content-Type"] = "application/json"

    if auth:
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    return headers


def get(endpoint: str, service: str = "store", auth: bool = True, params: dict | None = None):
    url = f"{_get_base_url(service)}{endpoint}"

    try:
        response = requests.get(
            url,
            headers=_get_headers(auth=auth),
            params=params,
            timeout=TIMEOUT,
        )

        _handle_401(response)
        return response
    except requests.RequestException as error:
        return _dummy_response(error)


def post(
    endpoint: str,
    data: dict | None = None,
    service: str = "store",
    auth: bool = True,
    is_form: bool = False,
):
    url = f"{_get_base_url(service)}{endpoint}"

    try:
        if is_form:
            response = requests.post(
                url,
                data=data,
                headers=_get_headers(auth=auth, is_form=True),
                timeout=TIMEOUT,
            )
        else:
            response = requests.post(
                url,
                json=data,
                headers=_get_headers(auth=auth),
                timeout=TIMEOUT,
            )

        _handle_401(response)
        return response
    except requests.RequestException as error:
        return _dummy_response(error)


def delete(endpoint: str, service: str = "store", auth: bool = True):
    url = f"{_get_base_url(service)}{endpoint}"

    try:
        response = requests.delete(
            url,
            headers=_get_headers(auth=auth),
            timeout=TIMEOUT,
        )

        _handle_401(response)
        return response
    except requests.RequestException as error:
        return _dummy_response(error)


def _handle_401(response) -> None:
    if response.status_code == 401:
        st.warning("Session expired. Please login again.")
        st.session_state["token"] = None
        st.session_state["user"] = None


def _dummy_response(error: Exception):
    class DummyResponse:
        status_code = 500
        text = str(error)

        def json(self):
            return {"error": str(error)}

    return DummyResponse()