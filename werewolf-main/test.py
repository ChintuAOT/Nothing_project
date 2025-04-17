from utils import *
import monologue

# generate the json file, you can check at the monologue.py
monologue.main() 

# a list for roles in the werewolf game, it is flexible, you can change at any time
roles = ["Villager", "Villager", "Villager", "Hunter", "Seer", "Wolf", "Wolf", "Wolf", "Witch"]

# parameters for ai api
llm_config = {
    "model_name": 'gpt-4o-mini',
    "api_key" : os.environ.get("OPENAI_API_KEY"),
    "temperature": 0.8,      
    "max_tokens": 800,
}

# generate agent class for each role and put them in a list
agents = [WerewolfAgent(name=f"Player{i+1}",llm_config = llm_config, roles=roles) for i in range(len(roles))]

# Create a group chat class, which is one parameter for the Host class
groupchat = GroupChat(agents, messages = ["you are a host for a werewolf game"])

# Initialize the host class
host = Host(groupchat, roles)

# Start the game
host.start_game()

