import streamlit as st
from unify import ChatBot


def main():
    # Sidebar for user configuration
    st.sidebar.title("Configuration")
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", value="")

    # Initialize ChatBot only if UNIFY_KEY is provided
    if unify_key:
        chatbot = ChatBot(model="gpt=3.5-turbo",
                          provider="anyscale", api_key=unify_key)
        st.title("Chat with Our Bot")

        # Session state to store chat history
        if 'history' not in st.session_state:
            st.session_state.history = []

        # User input for the message
        user_input = st.text_input("Type your message here:", key="user_input")

        # Handling sending message
        send_button = st.button("Send")
        if send_button and user_input:
            # Append user's message to history
            st.session_state.history.append("You: " + user_input)

            # Get the bot's response
            response = chatbot.respond(user_input)
            st.session_state.history.append("Bot: " + response)

            # Clear the input box after sending
            st.session_state.user_input = ""

            # Display the chat history
            for message in st.session_state.history:
                st.text(message)
    else:
        st.error("Please enter a valid UNIFY_KEY in the sidebar to start chatting.")


if __name__ == "__main__":
    main()
