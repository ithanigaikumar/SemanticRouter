
from unify import AsyncUnify


async def process_query(query, unify_key):
    route_choice = (query)
    print(f"Route chosen: {route_choice}")

    if route_choice == "math":
        # Initialize Unify with the endpoint for math queries
        unify = AsyncUnify(
            api_key=unify_key,
            # Use the correct endpoint for math queries
            endpoint="llama-2-13b-chat@anyscale"
        )
        # Generate the response using Unify
        response = unify.generate(user_prompt=query)
        return response

    elif route_choice == "coding":
        # Initialize Unify with the endpoint for coding queries
        unify = AsyncUnify(
            api_key=unify_key,
            # Use the correct endpoint for coding queries
            endpoint="codellama-34b-instruct@anyscale"
        )
        # Generate the response using Unify
        response = await unify.generate(user_prompt=query)
        return response

    else:
        unify = AsyncUnify(
            api_key=unify_key,
            # Use the correct endpoint for coding queries
            endpoint="llama-2-13b-chat@anyscale"
        )
        # Generate the response using Unify
        response = await unify.generate(user_prompt=query)
        return response
