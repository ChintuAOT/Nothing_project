## part of the file is hidden for easy understanding
import json


def main():

############# seer ######################
######################################3##
    seer = {
        "inner": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
        "outer": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
    }

    with open("Seer_inner_sketch_pad.json", "w") as file:
        json.dump(seer, file, indent = 4)


############# Witch ######################
######################################3###
    witch = {
        "inner": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
        "outer": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
    }
    with open("Witch_inner_sketch_pad.json", "w") as file:
        json.dump(witch, file, indent = 4)





############# Hunter ######################
######################################3####

    hunter = {
        "inner": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
        "outer": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
    }

    with open("Hunter_inner_sketch_pad.json", "w") as file:
        json.dump(hunter, file, indent = 4)




############# Villager ######################
######################################3######

    villager = {
        "inner": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
        "outer": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
    }
    with open("Villager_inner_sketch_pad.json", "w") as file:
        json.dump(villager, file, indent = 4)




############# Wolf ######################
######################################3##
    
    wolf = {
        "inner": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
        "outer": {
            "Player1": "none",
            "Player2": "none",
            "Player3": "none",
        },
    }

    with open("Wolf_inner_sketch_pad.json", "w") as file:
        json.dump(wolf, file, indent = 4)

if __name__ == "__main__":
    main()