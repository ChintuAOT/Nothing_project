from witchview import *
import os


roles = ["Villager", "Villager", "Villager", "Hunter", "Seer", "Wolf", "Wolf", "Wolf", "Witch"]

# Create agents

llm_config = {
    "model_name": 'gpt-4',
    "api_key" : os.environ.get("OPENAI_API_KEY"),
    "temperature": 0.8,      
    "max_tokens": 800,
}

agents = [WerewolfAgent(name=f"Player{i+1}",llm_config = llm_config, roles=roles) for i in range(len(roles))]

# Create a group chat

# Initialize the host
host = Host(agents, roles)

# Start the game
host.start_game()