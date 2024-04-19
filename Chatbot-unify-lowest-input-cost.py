from unify import ChatBot
import os
agent = ChatBot(
    # This is the default and optional to include.
    api_key="X99eQzqYps-83ouRX-9ELhM+BhDAY4tpXIkTFFXibs4=",
    endpoint="llama-2-13b-chat@anyscale"
)
agent.run()
print(agent._message_history)
