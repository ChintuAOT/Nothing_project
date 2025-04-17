# Werewolf

Experience a dynamic simulation of the Werewolf game, where players assume roles such as Hunter, Villager, Seer, Witch, and Wolf. This project features a group chat manager as the host of the game to coordinate gameplay, while each player utilizes JSON-based memory management to continuously update the game state and mimic human-like decision-making in every phase.

## Project Structure

- **test.py**  
  - Serves as the \_\_main\_\_ function to start the game.
  - Utilizes the class in `monologue.py` to generate and save memory for each game player.
  - Leverages the group chat manager class in `utils.py` to manage players and run the game.

- **monologue.py**  
  - Handles the creation of JSON files for each player's inner sketch pad.
  - Manages memory or state for each Werewolf agent.

- **utils.py**  
  1. **Class: WerewolfAgent**
  Provides a universal framework for Werewolf agent classes, enabling different game roles to utilize the same general class.
    - Hunter
    - Villager
    - Seer
    - Witch
    - Wolf
  2.  **Class: Host**
  Implements a group chat manager class that serves as the host by consolidating all mimic player agents from the `WerewolfAgent` class within the Host class and orchestrating the overall game process.






## General Game Process

1. **Setup:**
   - Each player is randomly assigned a role: Villager, Seer, Witch, Hunter, or Wolf.
   - The game initializes the private (night) and public (day) phases where specific actions occur.

2. **Night Phase:**
   - **Wolves:** Secretly convene to select a victim.
   - **Seer:** Privately inspects a player to determine their role.
   - **Witch:** Reviews the night's events and decides whether to use her healing potion to save a victim or her poison potion to eliminate a target.
   - **Hunter:** Decide to retaliate or not if killed by another player.

3. **Day Phase:**
   - The victim from the night is revealed to all players.
   - Players discuss their suspicions and observations, attempting to identify the wolves.
   - A vote is held to eliminate the player most suspected of being a wolf.

4. **Special Role Considerations:**
   - **Hunter:** Upon elimination, may choose to shoot another player as a final act.
   - **Witch:** Must use her potions judiciously, balancing between saving key players and strategically eliminating threats.
   - **Seer:** Provides crucial insights that influence group discussions, though the role remains hidden from other players.

5. **Winning Conditions:**
   - **Villagers win:** If all wolves are eliminated.
   - **Wolves win:** If their numbers equal or exceed those of the villagers.

6. **Game Loop:**
   - The cycle of night and day phases continues until one side meets their winning condition.
   - Throughout, mimic player agents simulate human decision-making based on their role-specific abilities and the evolving game state.
