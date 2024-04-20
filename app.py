import streamlit as st
import asyncio
from unify import AsyncUnify
import os
from semantic_router import Route
from getpass import getpass
from semantic_router import RouteLayer
from semantic_router.encoders import OpenAIEncoder


# Asynchronously handle chat operations


async def async_chat(openai_api_key, api_key, user_input, routes):
    # encoder = CohereEncoder()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    encoder = OpenAIEncoder()

    rl = RouteLayer(encoder=encoder, routes=routes)
    route_choice = rl(user_input)
    print(f"Route chosen: {route_choice}")

    if route_choice.name == "math":
        # Initialize Unify with the endpoint for math queries
        unify = AsyncUnify(
            api_key=api_key,
            # Use the correct endpoint for math queries
            endpoint="llama-2-13b-chat@anyscale"
        )
        # Generate the response using Unify
        response = await unify.generate(user_prompt=user_input)
        # If response is a string and not a stream, handle it directly
        if isinstance(response, str):
            return response

        # If response is a stream, then iterate over it
        response_text = ''
        async for chunk in response:
            response_text += chunk
        return response_text

    elif route_choice.name == "coding":
        # Initialize Unify with the endpoint for coding queries
        unify = AsyncUnify(
            api_key=api_key,
            # Use the correct endpoint for coding queries
            endpoint="codellama-34b-instruct@anyscale"
        )
        # Generate the response using Unify
        response = await unify.generate(user_prompt=user_input)
        # If response is a string and not a stream, handle it directly
        if isinstance(response, str):
            return response

        # If response is a stream, then iterate over it
        response_text = ''
        async for chunk in response:
            response_text += chunk
        return response_text

    else:
        unify = AsyncUnify(
            api_key=api_key,
            # Use the correct endpoint for coding queries
            endpoint="llama-2-13b-chat@anyscale"
        )
        # Generate the response using Unify
        response = await unify.generate(user_prompt=user_input)
        # If response is a string and not a stream, handle it directly
        if isinstance(response, str):
            return response

        # If response is a stream, then iterate over it
        response_text = ''
        async for chunk in response:
            response_text += chunk
        return response_text


def defineRoutes():
    math_route = Route(
        name="math",
        utterances=[
            "solve for x in the equation",
            "what is the integral of",
            "how to calculate the derivative",
            "mathematical proofs",
            "how do you find the percentage of this number",
            "how do you solve the determinant of a 2x2 matrix?"
        ],
    )

    coding_route = Route(
        name="coding",
        utterances=[
            "how to code a for loop in Python",
            "explain the use of classes in Java",
            "what is recursion in programming",
            "how do i optimise this problem using hash tables",
            "suggest a more efficient data structure for this problem"
        ],
    )

    # List of all routes
    routes = [math_route, coding_route]
    return routes


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
        route_list = defineRoutes()
        # Button to send the message
        if st.button("Send") and user_input:
            st.session_state.history.append(f"You: {user_input}")
            # Process chat asynchronously
            response = asyncio.run(async_chat(openai_api_key,
                                              unify_key, user_input, route_list))
            st.session_state.history.append(f"Bot: {response}")
            # Trigger a rerun of the app to update the conversation display
            st.rerun()
    else:
        st.error("Please enter valid keys to start chatting.")


if __name__ == "__main__":
    main()
