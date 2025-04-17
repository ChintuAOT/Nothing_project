# this class is for each werewolf agent, like Seer, Hunter, Witch, Villager, Wolf
class WerewolfAgent(ConversableAgent):
    def __init__(self, name, llm_config,roles, role="Villager",**kwargs):
        super().__init__(name=name,llm_config=llm_config, **kwargs)
        self.role = role
        self.roles = roles
        self.identity = ""
        self.round = 0
        self.llm_config = llm_config
        self.sketch_pad_file = f"{self.name}_sketch_pad.json"
        self.sketch_pad = self.initialize_sketch_pad()
        self.inner_sketch_pad_file = f"{self.name}_inner_sketch_pad.json"
        self.inner_sketch_pad = None
        self.healing = True
        self.poison = True
        self.pretend = None
        self.teammate = None


# functions to generate the sketch_pad, everytime when you want to generate something, you need to get the information from this sketch_pad

    def initialize_sketch_pad(self):
        """Initialize the sketch pad with a default structure."""

        default_sketch_pad = {
            "name": self.name,
            "role": self.role,
            "roles" : self.roles, # all roles in this werewolf games 
            "players" : [f"Player{i+1}" for i in range(len(self.roles))],  # player name in this werewolf game
        }

        ## IMPORTANT: SOME INFORMATION CAN NOT BE KNOWN BY PLAYER: LIKE MURDERER!!!

        with open(self.sketch_pad_file, 'w') as file:
            json.dump(default_sketch_pad, file, indent=4)
        return default_sketch_pad
    

    def update_sketch_pad(self):
        with open(self.sketch_pad_file, 'w') as file:
            json.dump(self.sketch_pad, file, indent=4)


# functions to generate the inner_sketch_pad, everytime when you want to generate something, you need to get the information from this inner_sketch_pad
# different information from the sketch_pad above, inner_sketch_pad are generated from the monologue.py as you can see
# so here you already have two json dictionary to save information for each player like this
# Player1_sketch_pad.json and Player1_inner_sketch_pad.json
    def initial_inner_sketch_pad(self, role):
        with open(f"{role}_inner_sketch_pad.json", "r") as temp:
            data = json.load(temp)  # Load the JSON content into a Python object
        with open(self.inner_sketch_pad_file, 'w') as file:
            json.dump(data, file, indent=4)
        self.inner_sketch_pad = data

    def update_inner_sketch_pad(self):
        with open(self.inner_sketch_pad_file, 'w') as file:
            json.dump(self.inner_sketch_pad, file, indent=4)


# this function only used by seer in night when seer is checking other player's identity, here we only let seer check the identiy in order

    def check_next_player(self, name, alive) -> str:
        # only part of the code for easy understanding
        return next_player


# this function only used by seer in night after seer decide who to check and update the information inside the two json file

    def inspect_player(self, player):
        # only part of the code for easy understanding
        self.update_sketch_pad()
        self.update_inner_sketch_pad()

    
# this function only used by the witch in night after witch decide whether to heal or not and  whether to poison or not
# be careful you  need the information here for updating the number of healing potion and the poison potion in the gui
# the return victims means in that game round, which player is killed after witch's action (because witch can poison player)
    def witch_potion(self, round, isWitchKilled, victims, alive, info_witch):    
        self.update_sketch_pad()
        self.update_inner_sketch_pad()
        return victims


# this function here passing what have happened to all the alive player at that time (like passing who is killed in the night to all the player)
    def broadcast(self, result, str):
        self.update_sketch_pad()
        self.update_inner_sketch_pad()

# this function here generate the note when player is killed and meet the situation to say the note. 
# note is a string here
    def note(self):
        # generate by ai api by using the information in the inner_skech_pad and skech_pad, returns a string
        # you should put it in the gui let every player see the note later
        return note


# this function only used by the huntet if hunter is killed in the situation allowed for retaliation

    def hunter_action(self, victims, alive):
        # return the player hunter want to kill by using ai api by analyze using the information in the inner_skech_pad and skech_pad
        return huntered_player
        


# this function is used by all the player when they generate who to vote or abstain during the vote session
    def vote_action(self, alive):
        return player_to_vote or None for abstain
        #  statistics on who vote who 


## Above is all the function for each player in the game


###############################################################3

## Below is the class for the host of the game, it let each player (WerewolfAgent) to call their function to continue the game


class Host(GroupChatManager):
    def __init__(self, groupchat, roles, name="god", human_input_mode="NEVER", system_message="god in werewolf game, help to organize the game", silent=False, time = 1, **kwargs):
        super().__init__(groupchat, name, human_input_mode, system_message, silent, **kwargs)

# this function here is for assigning the role and initialize the inner_sketch_pad and sketch_pad at the beginning of the game
# literally, this function prepare all the need for this game before start
# you probably need to build a start game gui here when running this function

    def assign_roles(self):
        pass

# this function is for starting the game, you can see in the test.py


    def start_game(self):
        """Start the Werewolf game sequence."""
        self.assign_roles()
        self.night_phase()


# this function check whether there is a side (villager side or wolf side) has won, if won end the game
# you may need to consider what to show as the ending of the game in the api.
    def check_status(self, alive=None):
        if ###### then
            sys.exit()
            


# this function is for the public discussion part and for each agent's public discussion you should shown in the gui
    def public_discussion(self):

        
        # public
        for ix, agent in enumerate(circular_order):  # circular_order is generated by host randomly, it is the sequence for public speaking
            response = generated by ai api prompting 
            # this response you should show in the gui
            print(response)

        # update sketch_pad based on the response
        for agent in circular_order:
            agent.update_inner_sketch_pad()
            agent.update_sketch_pad()
# this function return the chosen_player for the whole voting period
    def vote(self):
        return chosen_player 
    



# this function have defined the process in the night, there is also an introduction of what to do in the night for the game in readme ##General Game Process part

    def night_phase(self):
        self.round += 1

# you may print those print in the gui as the host to make game continue and give instructions to each player

        print(f"This is round {self.round}")
        print("🌙 Night falls on the village... Everyone, close your eyes.")


        print(
            """
                🐺 Wolves, open your eyes.
                - Look around, find your fellow wolves.
                - Silently agree on a villager to eliminate.
                - When you have chosen, point to your target.
                🐺 Wolves, close your eyes.
            """
            )
####################### Wolf Part #################################
###################################################################

        # the victims is generate by prompting from wolf or generate randomly
        victims = generate by ai api based on the inner_sketch_pad and sketch_pad in wolf (a string name like "Player1")


        # check game status here, this function is explained above
        self.check_status(alive)


####################### Seer Part #################################
###################################################################
        # you may need to show this in the gui
        print("Seer please open your eyes and decide who to check")

        seer = next((agent for agent in self.groupchat.agents if agent.role == "Seer"), None)  # select until you find seer
    
        # seer can choose who to decide who to inspect 1. based on the inner_sketch_pad and prompt with ai api
                                                        # 2. based on the sequence from the function check_next_player

        # then update the information for seer in its inner_sketch_pad and sketch_pad
        check_player = generated from ai api (a string name like "Player1")

        inspected = next((agent for agent in self.groupchat.agents if agent.name == check_player), None)
        seer.inspect_player(inspected)
        seer.update_inner_sketch_pad()


####################### Witch Part #################################
###################################################################
        witch = next((agent for agent in self.groupchat.agents if agent.role == "Witch"), None)  # select until you find witch

        # you may need to show this in the gui as host
        print("Witch please open your eyes")

        # this function decide whether to heal and poison based on the inner_sketch_pad with ai api.
        victims = witch.witch_potion(self.round, isWitchKilled, victims, alive, info_witch)

        # update information for witch
        witch.update_inner_sketch_pad()
        witch.update_sketch_pad()



        # check game status
        self.check_status(alive)

        print(
        """
            🌙 Night is over... The village awakens.
            - The narrator will now reveal if someone was eliminated.
        """
        )

        # broadcast the information to everyone
        death_information = f"In the round {self.round}, "
        for player in victims:
            death_information += f"{player.name} is dead during the night, "
            player.sketch_pad["timeline"] += f"you are killed during the night of round {self.round}, "
            player.update_sketch_pad()

        for player in alive:
            player.sketch_pad["timeline"] += f"you are survived during the the night of round {self.round}, "

        for agent in alive + victims:
            agent.broadcast(death_information, "history")

        
        # from the night going to the day phase
        self.day_phase(victims, alive, death_information)



####################### day phase Part #################################
###################################################################
    def day_phase(self, victims, alive, death_information):  

        # you may need to print it in gui
        print(last_night_info) # this string last_night_info is generate by a function
    
        
        print(new_broadcast)  # this string new_broadcast is generate by a function like hunter is killed in the night and hunter decide to retaliate and causing new victim
        
        # broadcast new information to everyone
        for agent in alive:
            agent.broadcast(new_broadcast, "history")


        # updaete new information to everyone in inner_sketch_pad

        for agent in alive:
            for victim in victims_name:
                agent.inner_sketch_pad["alive_status"][victim] = "dead"
            
            agent.update_inner_sketch_pad()
            


        self.groupchat.agents = alive


        self.check_status()

        # go to the public_discussion() function
        self.public_discussion()



        # go to the vote() function

        victim_name = self.vote()

        # you may need to print it in the gui
        print(f"the player is voted from the game is {victim_name}")

        # for the death or banished to say the note, you may need to pay atthention to the note part in the gui

        if victim_name != None:
            for player in alive:
                if player.name == victim_name:
                    temp_note = player.note()

                    # you may need to print here in the gui
                    print(temp_note, "the note")

                    for player in alive:
                        # you may need to print here in the gui
                        vote_information = f"In the round {self.round} {player.name} is banished and said"  + temp_note



        self.check_status()

        # going to the night phase again
        self.night_phase()



        