import streamlit as st
import asyncio
from unify import AsyncUnify
import os
from semantic_router import Route
from getpass import getpass
from semantic_router import RouteLayer
from concurrent.futures import ThreadPoolExecutor
from semantic_router.encoders.huggingface import HuggingFaceEncoder

huggingface_url = "https://api-inference.huggingface.co/models/gpt2"
# Routes to the appropriate endpoint
huggingface_logo = "https://cdn-lfs.huggingface.co/repos/96/a2/96a2c8468c1546e660ac2609e49404b8588fcf5a748761fa72c154b2836b4c83/9cf16f4f32604eaf76dabbdf47701eea5a768ebcc7296acc1d1758181f71db73?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27hf-logo.png%3B+filename%3D%22hf-logo.png%22%3B&response-content-type=image%2Fpng&Expires=1714669014&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxNDY2OTAxNH19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy5odWdnaW5nZmFjZS5jby9yZXBvcy85Ni9hMi85NmEyYzg0NjhjMTU0NmU2NjBhYzI2MDllNDk0MDRiODU4OGZjZjVhNzQ4NzYxZmE3MmMxNTRiMjgzNmI0YzgzLzljZjE2ZjRmMzI2MDRlYWY3NmRhYmJkZjQ3NzAxZWVhNWE3NjhlYmNjNzI5NmFjYzFkMTc1ODE4MWY3MWRiNzM%7EcmVzcG9uc2UtY29udGVudC1kaXNwb3NpdGlvbj0qJnJlc3BvbnNlLWNvbnRlbnQtdHlwZT0qIn1dfQ__&Signature=XlyzK%7EHZi9Vmf-w3gi8X7aNEFuV4m7qxNKtiKphVMpryDKpaZ708r1xZgMVn9tb56INExpW7gWQp9OWT1rsrcdhgB0T6WQiZvGQT4K9nl4eF8nglTJcQigmu8YOPDZqnBPOp%7E5IihQgm5-QYJfdxaMZT3JqDBsDRNiBhjj6GUHn7ye8QJu21dVsEqXL5ZU3qQUvh8Gdy%7EnPjip%7ET04mIzC0IEwPm3q7ZyA2BkeD-%7EL4LkWZ5wpsvejZQkoUU77Zklm1DcocZ8AZbRsejPshqbm%7E%7EGjhxmXHcz9Nu-AjBXDk3fnp11RDBRJlFwaTjOE9aPi8kXzL498vwUmcFzWynjg__&Key-Pair-Id=KVTP0A1DKRTAX"
unify_logo = "https://raw.githubusercontent.com/unifyai/unifyai.github.io/main/img/externally_linked/logo.png?raw=true#gh-light-mode-only"


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

# Re-implemented async_chat to include custom endpoints.


async def async_chat(huggingface_apikey, api_key, user_input, routes, endpoint="llama-2-13b-chat"):
    # Set API key environment variable at the beginning of the function, if not set globally
    os.environ["huggingface_apikey"] = huggingface_apikey
    encoder = HuggingFaceEncoder(
        huggingface_url=huggingface_url,
        huggingface_api_key=huggingface_apikey,
    )
    print(f"routes in async_chat:{routes}")
    print(f"endpoint chosen:{endpoint}")
    # Assuming OpenAIEncoder and RouteLayer are defined and imported properly elsewhere
    rl = RouteLayer(encoder=encoder, routes=routes)
    route_choice = rl(user_input)
    print(f"Route chosen: {route_choice.name}")

    # Define specific endpoints for known route names
    endpoint_map = {
        "math": "llama-2-13b-chat",
        "coding": "codellama-34b-instruct"
    }

    # Check if the route name is in the endpoint map, otherwise use the user-provided endpoint
    if route_choice.name in endpoint_map:
        chosen_endpoint = f"{endpoint_map[route_choice.name]}@anyscale"
    else:
        # Append "@anyscale" if not already included
        if "@anyscale" not in endpoint:
            endpoint += "@anyscale"
        chosen_endpoint = endpoint

    # Call the semantic route function with the chosen endpoint
    response = await semantic_route(api_key, chosen_endpoint, user_input)
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


# Custom routes function
def customRoutes(route_name, route_examples, route_list):
    custom_route = Route(
        name=route_name,
        utterances=route_examples.split(','),

    )
    print(f"custom route name:{custom_route.name}")
    print(f"custom route utteraqnces:{custom_route.utterances}")
    route_list.append(custom_route)
    print(f"Route list:{route_list}")
    return route_list
# handles send


def run_async_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


def async_chat_wrapper(user_input, huggingface_apikey, unify_key, routes, endpoint="llama-2-13b-chat"):
    # Pass the default endpoint if not provided
    coroutine = async_chat(huggingface_apikey, unify_key,
                           user_input, routes, endpoint)
    return run_async_coroutine(coroutine)


def main():
    # Include Font Awesome for styling
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">', unsafe_allow_html=True)
    logos_html = f"""
    <div style='display: flex; align-items: center; font-size: 26px; font-weight: bold;'>
        <img src='{huggingface_logo}' style='height: 40px; margin-right: 10px;' alt='HuggingFace Logo'/>
        Configuration
        <img src='{unify_logo}' style='height: 40px; margin-right: 10px;' alt='Unify Logo'/>
        
    </div>
    """
    # Using markdown to display what acts as a sidebar title with logos
    st.sidebar.markdown(logos_html, unsafe_allow_html=True)
    unify_key = st.sidebar.text_input("Enter your UNIFY_KEY", type='password')
    huggingface_apikey = st.sidebar.text_input(
        'Enter your HUGGING_FACE Key', type='password')

    # Dropdown for model selection, listing all available models
    model_list = [
        "mixtral-8x7b-instruct-v0.1", "llama-2-70b-chat", "llama-2-13b-chat",
        "mistral-7b-instruct-v0.2", "llama-2-7b-chat", "codellama-34b-instruct",
        "gemma-7b-it", "mistral-7b-instruct-v0.1", "mixtral-8x22b-instruct-v0.1",
        "codellama-13b-instruct", "codellama-7b-instruct", "yi-34b-chat",
        "llama-3-8b-chat", "llama-3-70b-chat", "pplx-7b-chat", "mistral-medium",
        "gpt-4", "pplx-70b-chat", "gpt-3.5-turbo", "deepseek-coder-33b-instruct",
        "gemma-2b-it", "gpt-4-turbo", "mistral-small", "mistral-large",
        "claude-3-haiku", "claude-3-opus", "claude-3-sonnet"
    ]
    selected_model = st.sidebar.selectbox(
        "Select a model for a custom route:", model_list)

    custom_element = st.sidebar.checkbox("Custom input?")
    custom_route_name = ""
    custom_utterances = ""
    if custom_element:
        custom_route_name = st.sidebar.text_input(
            "Enter the name of your custom route:")
        custom_utterances = st.sidebar.text_input(
            "Enter some examples to direct to this route (separate by comma):")

    if huggingface_apikey and unify_key:
        st.session_state.unify_key = unify_key
        st.session_state.huggingface_apikey = huggingface_apikey
        st.title("🤖💬 Streaming Router ChatBot")

        # Initialize or update the chat history in session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Display existing chat messages
        messages_container = st.container()
        for msg_type, msg_content in st.session_state.chat_history:
            if msg_type == "user":
                messages_container.chat_message("user").write(msg_content)
            elif msg_type == "assistant":
                messages_container.chat_message("assistant").write(msg_content)

        # Chat input at the bottom of the page
        user_input = st.chat_input("Say something", key="chat_input")

        if user_input:
            routes = defineRoutes()  # Load or define the routes applicable to this session
            if custom_element:
                # Adjust routes based on custom inputs
                routes = customRoutes(
                    custom_route_name, custom_utterances, routes)
            with ThreadPoolExecutor() as executor:
                future = executor.submit(
                    async_chat_wrapper, user_input, st.session_state.huggingface_apikey, st.session_state.unify_key, routes, selected_model)
                response = future.result()
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("assistant", response))
                st.rerun()
        else:
            st.warning("Type something to start chatting.")
    else:
        st.error("Please enter valid keys to start chatting.")


if __name__ == "__main__":
    main()
