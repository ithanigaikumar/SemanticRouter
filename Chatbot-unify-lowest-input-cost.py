from unify import ChatBot
agent = ChatBot(
    # This is the default and optional to include.
    api_key=os.environ.get("UNIFY_KEY"),
    endpoint="llama-2-13b-chat@lowest-input-cost"
)
agent.run()
