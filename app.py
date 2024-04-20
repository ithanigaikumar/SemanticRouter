import streamlit as st
import asyncio
from unify import AsyncUnify

# Asynchronously handle chat operations


async def async_chat(api_key, user_input):
    async_unify = AsyncUnify(
        api_key=api_key, endpoint="llama-2-13b-chat@anyscale")
    # Ensure this is async and properly awaited so doesn't block application
    response = await async_unify.generate(user_prompt=user_input)

    # If response is a string and not a stream, handle it directly
    if isinstance(response, str):
        return response

    # If response is a stream, then iterate over it
    response_text = ''
    async for chunk in response:
        response_text += chunk
    return response_text


def main():
    st.sidebar.title("Configuration")
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", value="")
    openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

    # Check if OpenAI API key starts with 'sk-'
    if openai_api_key and not openai_api_key.startswith('sk-'):
        st.sidebar.warning('Please enter a valid OpenAI API key!', icon='⚠️')

    # Proceed only if both keys are entered correctly
    if unify_key and openai_api_key.startswith('sk-'):
        st.title("Streaming Router ChatBot")

        # Initialize conversation history in session state if not already present
        if 'history' not in st.session_state:
            st.session_state.history = []

        # Display each message in the history
        for message in st.session_state.history:
            sender, text = message.split(": ", 1)
            st.text(f"{sender}: {text}")

        # Input for user message
        user_input = st.text_input("Type your message here:", key="user_input")

        # Button to send the message
        if st.button("Send") and user_input:
            st.session_state.history.append(f"You: {user_input}")
            # Process chat asynchronously
            response = asyncio.run(async_chat(unify_key, user_input))
            st.session_state.history.append(f"Bot: {response}")
            # Trigger a rerun of the app to update the conversation display
            st.experimental_rerun()
    else:
        st.error("Please enter valid keys to start chatting.")


if __name__ == "__main__":
    main()
