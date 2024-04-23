import streamlit as st
import asyncio
from unify import AsyncUnify
import os
from semantic_router import Route
from getpass import getpass
from semantic_router import RouteLayer
from semantic_router.encoders import OpenAIEncoder


# Routes to the appropriate endpoint
async def semantic_route(api_key, route_endpoint, user_input):
    unify = AsyncUnify(
        api_key=api_key,
        # Use the correct endpoint for math queries
        endpoint=route_endpoint
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


# Asynchronously handle chat operations

async def async_chat(openai_api_key, api_key, user_input, routes):
   # encoder = CohereEncoder()
    os.environ["OPENAI_API_KEY"] = openai_api_key
    encoder = OpenAIEncoder()

    rl = RouteLayer(encoder=encoder, routes=routes)
    route_choice = rl(user_input)
    print(f"Route chosen: {route_choice}")

    if route_choice.name == "math":

        endpoint = "llama-2-13b-chat@anyscale"
        response = await semantic_route(api_key, endpoint, user_input)
        return response

    elif route_choice.name == "coding":
        # Use the correct endpoint for coding queries
        endpoint = "codellama-34b-instruct@anyscale"
        response = await semantic_route(api_key, endpoint, user_input)
        return response

    else:
        endpoint = "llama-2-13b-chat@anyscale"
        response = await semantic_route(api_key, endpoint, user_input)
        return response


# Define routes function
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

# handles send


def handle_send():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.history.append(f"You: {user_input}")
        # Asynchronously handle the chat response
        response = asyncio.run(async_chat(st.session_state.openai_api_key,
                                          st.session_state.unify_key, user_input, defineRoutes()))
        st.session_state.history.append(f"Bot: {response}")
    # Reset the input field after handling the send
    st.session_state.user_input = ""


# main function
def main():
    st.sidebar.title("Configuration")
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", type='password')
    openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

    if openai_api_key and not openai_api_key.startswith('sk-'):
        st.sidebar.warning('Please enter a valid OpenAI API key!', icon='⚠️')

    if unify_key and openai_api_key.startswith('sk-'):
        st.session_state.unify_key = unify_key
        st.session_state.openai_api_key = openai_api_key
        st.title("Streaming Router ChatBot")

        if 'history' not in st.session_state:
            st.session_state.history = []

        for message in st.session_state.history:
            sender, text = message.split(": ", 1)
            st.markdown(f"{sender}: {text}")

        user_input = st.text_input(
            "Type your message here:", key="input", value="")
        st.session_state.user_input = user_input

        if st.button("Send", on_click=handle_send):
            pass  # Button press is handled in the handle_send function
    else:
        st.error("Please enter valid keys to start chatting.")


if __name__ == "__main__":
    main()
