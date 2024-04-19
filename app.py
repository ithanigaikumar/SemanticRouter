import os
import streamlit as st
from unify import ChatBot


def main():
    st.sidebar.title("Configuration")
    # Load API key from environment or prompt for it if not available
    unify_key = st.sidebar.text_input(
        "Enter your UNIFY_KEY", value="")

    if unify_key:
        try:
            # Initialize the ChatBot with the specified endpoint and API key
            chatbot = ChatBot(
                api_key=unify_key,
                endpoint="llama-2-13b-chat@anyscale"
            )
            st.title("Streaming Router ChatBot")

            # Initialize or retrieve chat history from session state
            if 'history' not in st.session_state:
                st.session_state.history = []

            # Display chat history
            for idx, message in enumerate(st.session_state.history):
                sender, text = message.split(": ", 1)
                st.container().markdown(f"**{sender}**: {text}")

            # User input for the message
            user_input = st.text_input(
                "Type your message here:", key="user_input")
            print(f"This is {user_input}")
            # Handling sending message
            if st.button("Send") and user_input:
                st.session_state.history.append(f"You: {user_input}")
                print(
                    f"Session state before response{st.session_state.history}")
                # Get the bot's response
                # Ensure .run() is an existing method
                response = chatbot.run(user_input)
                print(f"This is {response}")
                st.session_state.history.append(f"Bot: {response}")
                print(f"After response{st.session_state.history}")
                # Refresh to show updated chat history
                st.experimental_rerun()
        except Exception as e:
            st.error(
                f"Error initializing ChatBot with provided UNIFY_KEY: {str(e)}")
    else:
        st.error("Please enter a valid UNIFY_KEY to start chatting.")


if __name__ == "__main__":
    main()
