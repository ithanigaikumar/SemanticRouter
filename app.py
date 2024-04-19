import streamlit as st
import asyncio
from unify import AsyncUnify

# Asynchronously handle chat operations


async def async_chat(api_key, user_input):
    async_unify = AsyncUnify(
        api_key=api_key, endpoint="llama-2-13b-chat@anyscale")
    # Ensure this is async and properly awaited
    response = await async_unify.generate(user_prompt=user_input)

    # If response is a string and not a stream, handle it directly
    if isinstance(response, str):
        return response

    # If response is indeed a stream, then iterate over it
    response_text = ''
    async for chunk in response:
        response_text += chunk
    return response_text


def main():
    st.sidebar.title("Configuration")
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", value="")

    if unify_key:
        st.title("Streaming Router ChatBot")

        if 'history' not in st.session_state:
            st.session_state.history = []

        for message in st.session_state.history:
            sender, text = message.split(": ", 1)
            st.text(f"{sender}: {text}")

        user_input = st.text_input("Type your message here:", key="user_input")

        if st.button("Send") and user_input:
            st.session_state.history.append(f"You: {user_input}")
            # Process chat asynchronously
            response = asyncio.run(async_chat(unify_key, user_input))
            st.session_state.history.append(f"Bot: {response}")
            st.rerun()
    else:
        st.error("Please enter a valid UNIFY_KEY to start chatting.")


if __name__ == "__main__":
    main()
