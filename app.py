import streamlit as st
import asyncio
from unify import AsyncUnify
import os
import json
from semantic_router import Route
from getpass import getpass
from semantic_router import RouteLayer
from concurrent.futures import ThreadPoolExecutor
from semantic_router.encoders.huggingface import HuggingFaceEncoder
import logging
import time
# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Example usage of logging in your script
logging.debug("This is a debug message")
logging.info("This is an informational message")
logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")


huggingface_logo = "data:image/png;base64,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"
unify_logo = "https://raw.githubusercontent.com/unifyai/unifyai.github.io/main/img/externally_linked/logo.png?raw=true#gh-light-mode-only"

# readfiles


def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Now you can load this data in any other file
# res_math = load_from_json('questionsmaths.json')
# res_code = load_from_json("questionscode.json")


async def semantic_route(api_key, route_endpoint, user_input):
    logging.debug(
        f"Starting semantic_route for input: {user_input} with endpoint: {route_endpoint}")
    unify = AsyncUnify(
        api_key=api_key,
        endpoint=route_endpoint
    )
    # Generate the response using Unify
    response = await unify.generate(user_prompt=user_input)
    # If response is a string and not a stream, handle it directly
    if isinstance(response, str):
        logging.debug("Received a direct response from the API")
        return response

    # If response is a stream, then use st.write_stream
    logging.debug("Processing response stream")

    async def response_stream():
        async for chunk in response:
            yield chunk
    return st.write_stream(response_stream())
# Re-implemented async_chat to include custom endpoints and response information with styling.


async def async_chat(huggingface_apikey, api_key, user_input, routes, endpoint="llama-2-13b-chat"):
    # Set API key environment variable at the beginning of the function, if not set globally
    os.environ["huggingface_apikey"] = huggingface_apikey
    encoder = HuggingFaceEncoder()
    # Assuming OpenAIEncoder and RouteLayer are defined and imported properly elsewhere
    rl = RouteLayer(encoder=encoder, routes=routes)
    updated_thresholds = {
        'math':  0.19191919191919193,
        'coding': 0.21
    }

    print(f"routes in async_chat:{routes}")
    print(f"endpoint chosen:{endpoint}")
    logging.debug(f"Starting routing for input: {user_input}")
    start_time = time.time()  # Import time module if not already imported
    # Assuming `rl` is your RouteLayer instance
    for route in rl.routes:
        if route.name in updated_thresholds:
            route.score_threshold = updated_thresholds[route.name]
        else:
            print(
                f"No updated threshold found for route {route.name}, using default.")

    route_choice = rl(user_input)
    print(f"Route chosen: {route_choice.name}")
    elapsed_time = time.time() - start_time
    logging.debug(
        f"Routing completed in {elapsed_time:.2f} seconds. Route chosen: {route_choice.name}")
    # Define specific endpoints for known route names
    endpoint_map = {
        "math": "llama-2-13b-chat",
        "coding": "codellama-34b-instruct"
    }

    # Check if the route name is in the endpoint map, otherwise use the user-provided endpoint
    if route_choice.name in endpoint_map:
        chosen_endpoint = endpoint_map[route_choice.name]
    else:
        # Strip any "@anyscale" from the endpoint
        chosen_endpoint = endpoint.rstrip("@anyscale")
    logging.debug(f"Endpoint for processing: {chosen_endpoint}")
    # Call the semantic route function with the chosen endpoint
    response = await semantic_route(api_key, f"{chosen_endpoint}@anyscale", user_input)

    response_info = f"🚀 Routed to: {route_choice.name}, {chosen_endpoint} was used to generate this response:🚀 {response}"

    return response_info
# Define routes function


def defineRoutes():
    math_route = Route(
        name="math",
        utterances=[
            "Solve for x in the equation 3x - 7 = 2x + 8",
            "Calculate the integral of x^2 from 0 to 1",
            "Determine the derivative of f(x) = 3x^3 - 5x + 6",
            "Provide a proof for the Pythagorean theorem",
            "How do you find the percentage of 50 in 200?",
            "Calculate the determinant of the 2x2 matrix [[1, 2], [3, 4]]",
            "What is the sum of 2 + 2?",
            "Expand the polynomial (x+1)^3",
            "Calculate the area of a circle with a radius of 5 units",
            "Explain the Pythagorean theorem and its applications",
            "Find the volume of a cone with a radius of 3 units and a height of 5 units",
            "Simplify the square root of 144",
            "Solve the system of equations 2x + 3y = 5 and 4x - y = 2",
            "Calculate the slope of the line passing through the points (2, 3) and (5, 7)",
            "Factorize the quadratic x^2 - 5x + 6",
            "Explain Euler's formula and its significance in complex analysis",
            "Calculate the cosine of a 45-degree angle",
            "List all prime numbers up to 100",
            "Solve the quadratic equation x^2 - 4x + 4 = 0",
            "Explain the concept of logarithms and their real-world applications",
            "Calculate the sum of the arithmetic series 3 + 7 + 11 + ... up to n terms",
            "Find the limit as x approaches 2 of the function (x^2 - 4)/(x - 2)",
            "Describe the binomial theorem and its use in algebra",
            "Compute the compound interest for an initial investment of 1000 dollars at 5% per year for 10 years",
            "Derive the formula for the circumference of a circle",
            "If set A = {1, 2, 3, 4} and set B = {3, 4, 5, 6}, what is the intersection of A and B?",
            "How many different ways can you rearrange the letters in the word 'MATH'?"
        ]
    )

    coding_route = Route(
        name="coding",
        utterances=[
            "How to reverse a string in Python?",
            "What is the difference between == and === in JavaScript?",
            "How to sort an array of integers in C++?",
            "Write a function in Java to check if a number is prime",
            "How to merge two dictionaries in Python?",
            "Explain the use of arrow functions in JavaScript.",
            "How to handle exceptions in Java?",
            "Write a program in C to find the Fibonacci sequence up to n terms",
            "How to read and write files in Python?",
            "Explain polymorphism in object-oriented programming with a C++ example",
            "What is recursion and provide a C# example?",
            "How to find the maximum value in a JavaScript array?",
            "How to implement a queue using arrays in C?",
            "What is a decorator in Python and how can you create one?",
            "How to check if two strings are anagrams in Java?",
            "Write a SQL query to find the second highest salary from the Employees table",
            "How to convert a JavaScript array of strings to integers?",
            "What is the difference between deep copy and shallow copy in Python?",
            "How to find the intersection of two arrays in JavaScript without using set operations?",
            "What is a lambda function in Python and how is it used?",
            "How to implement a simple linear search algorithm in C++?",
            "Write a JavaScript function to count the occurrences of a character in a string",
            "How to implement a binary search algorithm in Java?",
            "What are the different ways to iterate over a dictionary in Python?",
            "How to calculate the sum of elements in an array using a loop in C?"
        ]
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
    route_list.append(custom_route)
    return route_list
# handles send


def run_async_coroutine(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(coroutine)
        # This prints the actual result
        # print(f"Coroutine completed with result: {result}")
        return result
    finally:
        loop.close()


def async_chat_wrapper(user_input, huggingface_apikey, unify_key, routes, endpoint="llama-2-13b-chat"):
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

    # Set keys in session state after they are entered
    if unify_key and huggingface_apikey:
        st.session_state.unify_key = unify_key
        st.session_state.huggingface_apikey = huggingface_apikey

    if 'huggingface_apikey' in st.session_state and 'unify_key' in st.session_state:
        # Display Pre-defined Routes
        endpoint_map = {
            "math": "llama-2-13b-chat",
            "coding": "codellama-34b-instruct"
        }
        st.sidebar.title("Pre-defined Routes and Corresponding Models:")
        for route, model in endpoint_map.items():
            st.sidebar.text(f"{route}: {model}")

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

        custom_element = st.sidebar.checkbox("Create custom route?")
        custom_route_name = ""
        custom_utterances = ""
        if custom_element:
            custom_route_name = st.sidebar.text_input(
                "Enter the name of your custom route:")
            custom_utterances = st.sidebar.text_input(
                "Enter some examples to direct to this route (separate by comma):")
        st.title("🤖💬 Semantic Router ChatBot")

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

         # Button to reset the chat history
        if st.button("Reset Chat"):
            st.session_state.chat_history = []  # Clear the chat history
            st.experimental_rerun()  # Rerun the app to update the UI

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
