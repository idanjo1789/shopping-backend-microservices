import streamlit as st

from services.auth import require_auth
from services.chat_service import ask_store_chat

MAX_QUESTIONS = 5


def _init_chat_state() -> None:
    if "store_chat_messages" not in st.session_state:
        st.session_state["store_chat_messages"] = []

    if "store_chat_count" not in st.session_state:
        st.session_state["store_chat_count"] = 0


def render() -> None:
    require_auth()
    _init_chat_state()

    st.title("Chat Assistant")
    st.write("Ask questions about the store products.")
    st.write("You can use up to 5 prompts in this session.")

    messages = st.session_state["store_chat_messages"]
    questions_used = st.session_state["store_chat_count"]
    questions_left = MAX_QUESTIONS - questions_used

    st.caption(f"Questions left: {questions_left}")

    for message in messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")

    st.divider()

    if questions_used < MAX_QUESTIONS:
        user_input = st.text_input("Your question", key="store_chat_input")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Send", key="send_store_chat"):
                clean_input = user_input.strip()

                if not clean_input:
                    st.warning("Please enter a question.")
                    return

                messages.append({"role": "user", "content": clean_input})

                try:
                    result = ask_store_chat(clean_input)
                    answer = result.get("answer", "No answer returned.")

                    messages.append({"role": "assistant", "content": answer})
                    st.session_state["store_chat_count"] += 1
                    st.rerun()

                except Exception as error:
                    messages.pop()
                    st.error(f"Chat failed: {error}")

        with col2:
            if st.button("Reset Chat", key="reset_store_chat"):
                st.session_state["store_chat_messages"] = []
                st.session_state["store_chat_count"] = 0
                st.rerun()
    else:
        st.error("You have reached the maximum of 5 questions in this session.")

        if st.button("Reset Chat", key="reset_store_chat_after_limit"):
            st.session_state["store_chat_messages"] = []
            st.session_state["store_chat_count"] = 0
            st.rerun()