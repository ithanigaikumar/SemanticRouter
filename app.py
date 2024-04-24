import streamlit as st
import asyncio
from unify import AsyncUnify
import os
from semantic_router import Route
from getpass import getpass
from semantic_router import RouteLayer
from concurrent.futures import ThreadPoolExecutor
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


def run_async_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


def async_chat_wrapper(user_input, openai_api_key, unify_key, routes):
    coroutine = async_chat(openai_api_key, unify_key, user_input, routes)
    return run_async_coroutine(coroutine)


def main():
    # Assuming that 'defineRoutes' and 'async_chat_wrapper' are defined elsewhere

    # Include Font Awesome
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">', unsafe_allow_html=True)

    st.sidebar.title("Configuration")
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", type='password')
    openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

    if openai_api_key and not openai_api_key.startswith('sk-'):
        st.sidebar.warning('Please enter a valid OpenAI API key!', icon='⚠️')

    if unify_key and openai_api_key.startswith('sk-'):
        st.session_state.unify_key = unify_key
        st.session_state.openai_api_key = openai_api_key
        st.title("🤖💬 Streaming Router ChatBot")

        if 'history' not in st.session_state:
            st.session_state.history = []

        for message in st.session_state.history:
            st.markdown(message, unsafe_allow_html=True)

        user_input = st.text_input("Type your message here:", key="input")

        if st.button("Send") and user_input:
            routes = defineRoutes()
            with ThreadPoolExecutor() as executor:
                future = executor.submit(
                    async_chat_wrapper, user_input, st.session_state.openai_api_key, st.session_state.unify_key, routes)
                response = future.result()
                st.session_state.history.append(
                    f'<i class="fas fa-user"></i> {user_input}')
                st.session_state.history.append(
                    f'<i class="fas fa-robot"></i> {response}')
                st.experimental_rerun()

    else:
        st.error("Please enter valid keys to start chatting.")


if __name__ == "__main__":
    main()
