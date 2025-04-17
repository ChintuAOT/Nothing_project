import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
import time
import random
import threading
import re

pause_playback = threading.Event()
pause_playback.set()  # Playback starts as enabled

roles = ["Host", "Seer", "Witch", "Hunter", "Wolf", "Villager", "WitchHealing", "WitchPoison", "WitchVote", "Banished", "Killed", "Poisoned",
            "Player1", "Player2", "Player3", "Player4", "Player5",
            "Player6", "Player7", "Player8", "Player9"] # Define the roles in the conversation

# round 3 delete, delete (gpt)

healing = 1
poison = 1

def load_conversation(file_path, roles=roles):
    """
    Reads the conversation file line by line and extracts tuples (sender, message)
    for lines matching the pattern "Role: message".
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    conversation = []
    role_pattern = "|".join(re.escape(role) for role in roles)
    for line in lines:
        if line.strip():
            # Only match lines that start with a role followed by a colon.
            match = re.match(fr"^({role_pattern})['\-\_s]*?:", line)
            if match:
                sender = match.group(1).strip()
                message = line.split(":", 1)[-1].strip()
                conversation.append((sender, message))
    return conversation


root = tk.Tk()
root.title("Witch's View - Werewolf Game")
root.geometry("650x900")

############################################################################################################################
# ============ 1) Action Frame ============
############################################################################################################################

action_frame = ttk.Frame(root, padding="5 5 5 5", height=400)
action_frame.pack(fill='both', padx=10, pady=5)
action_frame.pack_propagate(False)

# Add a label above the canvas
action_label = ttk.Label(action_frame, text="Action Interface")
action_label.pack(side=tk.TOP, anchor="w", pady=(0, 5))  # some padding below the label

action_canvas = tk.Canvas(action_frame, bg="white", highlightthickness=0)
action_scrollbar = tk.Scrollbar(action_frame, command=action_canvas.yview)
action_history = tk.Frame(action_canvas, bg="white")
action_canvas.config(yscrollcommand=action_scrollbar.set)

action_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
action_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
action_canvas.create_window((0, 0), window=action_history, anchor="nw")

def on_frame_configure(event):
    """Update the scroll region when the frame resizes."""
    action_canvas.configure(scrollregion=action_canvas.bbox("all"))


action_history.bind("<Configure>", on_frame_configure)



############################################################################################################################
# ======= 2) Player Status Frame  =========
############################################################################################################################

avatar_paths = {
    1:  "/Users/dennis/Desktop/src/tkinder/avatars/Player1.png", 
    2: "/Users/dennis/Desktop/src/tkinder/avatars/Player2.png", 
    3:  "/Users/dennis/Desktop/src/tkinder/avatars/Player3.png", 
    4:  "/Users/dennis/Desktop/src/tkinder/avatars/Player4.png", 
    5: "/Users/dennis/Desktop/src/tkinder/avatars/Player5.png", 
    6:  "/Users/dennis/Desktop/src/tkinder/avatars/Player6.png", 
    7: "/Users/dennis/Desktop/src/tkinder/avatars/Player7.png", 
    8: "/Users/dennis/Desktop/src/tkinder/avatars/Player8.png", 
    9:  "/Users/dennis/Desktop/src/tkinder/avatars/Player9.png", 
    10: "/Users/dennis/Desktop/src/ideatrix/hard_code/avatars/witch.png",
}

avatar_banished = {
    1: "/Users/dennis/Desktop/src/tkinder/avatars/Player1_banished.png", 
    2: "/Users/dennis/Desktop/src/tkinder/avatars/Player2_banished.png", 
}


avatar_poisoned = {
    7: "/Users/dennis/Desktop/src/tkinder/avatars/Player7_poisoned.png", 
}

avatar_killed = {
    3: "/Users/dennis/Desktop/src/tkinder/avatars/Player3_killed.png", 
    4: "/Users/dennis/Desktop/src/tkinder/avatars/Player4_killed.png", 
    5: "/Users/dennis/Desktop/src/tkinder/avatars/Player5_killed.png", 
}


avatars = {
    "Host" : "/Users/dennis/Desktop/src/tkinder/avatars/host.png", 
    "Seer" : "/Users/dennis/Desktop/src/tkinder/avatars/seer.png", 
    "Witch" : "/Users/dennis/Desktop/src/tkinder/avatars/witch.png", 
    "Hunter" :"/Users/dennis/Desktop/src/tkinder/avatars/hunter.png", 
    "Wolf" :"/Users/dennis/Desktop/src/tkinder/avatars/wolf.png", 
    "Villager" :"/Users/dennis/Desktop/src/tkinder/avatars/hunter.png", 
    "Player1" : "/Users/dennis/Desktop/src/tkinder/avatars/Player1.png", 
    "Player2" : "/Users/dennis/Desktop/src/tkinder/avatars/Player2.png", 
    "Player3" : "/Users/dennis/Desktop/src/tkinder/avatars/Player3.png", 
    "Player4" : "/Users/dennis/Desktop/src/tkinder/avatars/Player4.png", 
    "Player5" : "/Users/dennis/Desktop/src/tkinder/avatars/Player5.png", 
    "Player6" : "/Users/dennis/Desktop/src/tkinder/avatars/Player6.png", 
    "Player7" : "/Users/dennis/Desktop/src/tkinder/avatars/Player7.png", 
    "Player8" : "/Users/dennis/Desktop/src/tkinder/avatars/Player8.png", 
    "Player9" : "/Users/dennis/Desktop/src/tkinder/avatars/Player9.png", 
}

# Frame to hold the avatars
boxes_frame = ttk.Frame(root, padding="5 5 5 5", height=60)
boxes_frame.pack(fill='x', padx=10, pady=5)
boxes_frame.pack_propagate(False)


# We will store the PhotoImage references so they don't get garbage collected.
# We can store them in a list or dictionary. Here, let's use a list:
avatar_images = []

# Create 9 avatars

avatar_buttons = []  # We'll store the avatar buttons here
def on_vote_avatar_click(player_id):
    """
    Called when an avatar is clicked during the WitchVote phase.
    Draws a bubble showing the vote and resumes the conversation.
    """
    draw_bubble(action_history, "Player6", f"You voted for Player {player_id}", role_alignment="right")

    pause_playback.set()  # Resume the conversation

def on_avatar_click(player_id):

    print(f"Avatar {player_id} clicked")

for player_id in range(1, 10):
    # Load the image
    image_path = avatar_paths[player_id]
    pil_image = Image.open(image_path)
    # Optionally, resize the image if it's too large
    pil_image = pil_image.resize((50, 50))
    # Convert to a PhotoImage
    avatar_image = ImageTk.PhotoImage(pil_image)
    avatar_images.append(avatar_image)
    # Create a Button (so it's clickable)
    # Use lambda to capture the current player_id.
    btn = tk.Button(
        boxes_frame,
        image=avatar_image,
        command=lambda pid=player_id: on_avatar_click(pid),
    )
    btn.pack(side='left', padx=5)
    avatar_buttons.append(btn)

############################################################################################################################
# ====== 3) User-Interactive Frame ========
############################################################################################################################

typing_label = tk.Label(root, text="Click Start Game Button to  start the game", font=("Arial", 14), fg="gray")
typing_label.pack(padx=20, pady=0, anchor="w")

user_frame = ttk.Frame(root, padding=0, height=300)
user_frame.pack(fill='both', padx=10, pady=0, expand=True)
user_frame.pack_propagate(False)

input_frame = ttk.Frame(user_frame,width=220, height=300)
input_frame.pack(side='left', fill='both', expand=True, padx=(0, 0))
input_frame.pack_propagate(False)

input_scrollbar = tk.Scrollbar(input_frame, orient=tk.VERTICAL)

input_text_box = tk.Text(
    input_frame, height=16, width=50, wrap=tk.WORD, 
    yscrollcommand=input_scrollbar.set
)
input_text_box.pack(fill='x', pady=0, expand= True)

input_scrollbar.config(command=input_text_box.yview)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def adjust_input_height():
    """Adjust the height of the input box based on its content."""
    lines = int(input_text_box.index("end-1c").split(".")[0])  # Get the number of lines
    input_text_box.config(height=max(20, min(10, lines)))  # Ensure height is between 5 and 10 lines

input_text_box.bind("<KeyRelease>", lambda event: adjust_input_height())

button_frame = ttk.Frame(input_frame, width=220, height=30)
button_frame.pack(fill='x', pady=0)
button_frame.pack_propagate(False)


submit_button = ttk.Button(button_frame, text="Submit", width=12)
submit_button.pack(side=tk.LEFT, padx=5, pady=0)

# AI-reply button
ai_reply_button = ttk.Button(button_frame, text="AI-reply", width=12)
ai_reply_button.pack(side=tk.LEFT, padx=5, pady=0)

def simulate_typing_in_input_box(message):
    """Simulates typing letter by letter in the input box."""
    input_text_box.delete("1.0", tk.END)  # Clear the input box
    for char in message:
        input_text_box.insert(tk.END, char)  # Insert character at the end
        input_text_box.update_idletasks()  # Update the display
        time.sleep(random.uniform(0.05, 0.1))  # Random delay between 50ms and 100ms


def ai_reply():
    """Simulates an AI-generated reply with typing effect in the input box."""
    suggested_text = "This is Witch's suggested AI reply."  # Replace with generated text if needed
    threading.Thread(target=simulate_typing_in_input_box, args=(suggested_text,), daemon=True).start()

# Assign the function to the AI-reply button
ai_reply_button.config(command=ai_reply)

info_label = ttk.Label(user_frame, text="Player Info", font=("Arial", 12, "bold"))
info_label.pack(side='top', anchor='center', pady=(0, 5))  # Adjust padding as needed

info_frame = ttk.Frame(user_frame)
info_frame.pack(side='right', fill='y', padx=(5, 0), pady= 0)

# Potions section
potions_frame = ttk.Frame(info_frame)
potions_frame.pack(fill='x', pady=2)

def select_potion(potion_name):
    print(f"Potion selected: {potion_name}")


def on_heal_click(decision):
    global healing
    # Create a bubble on the action canvas with the user's decision.
    # Here we assume draw_bubble(action_history, sender, message) exists.
    if decision == "Heal":
        draw_bubble(action_history, "Witch", f"Your Choice: {decision}", role_alignment="right")
        healing = healing - 1  # Now healing becomes 0
        potion_info_label.config(text=f"Healing: {healing}   Poison: {poison}")
        pause_playback.set()
    else:
        draw_bubble(action_history, "Witch", f"Your Choice: {decision}", role_alignment="right")
        pause_playback.set()


def on_poison_click(decision):
    global poison
    """
    When the poison button is clicked, reconfigure all avatar buttons so that they
    become enabled and their command will record the user's choice along with the poison decision.
    """
    # Enable each avatar button and reconfigure its command.

    if decision == "Not Poison":
        draw_bubble(action_history, "Witch", f"You choose not to poison in this round", role_alignment="right")
        pause_playback.set()
    else:
        for i, btn in enumerate(avatar_buttons, start=1):
            btn.config(state="normal", command=lambda pid=i: on_poison_avatar_click(pid, decision))


        poison = poison - 1  # Now healing becomes 0
        potion_info_label.config(text=f"Healing: {healing}   Poison: {poison}")
        # Optionally update the typing label to prompt the avatar selection.
        typing_label.config(text="Now, CLICK an avatar to select the target to poison!")

def on_poison_avatar_click(player_id, decision):
    """
    Called when an avatar button is clicked during the poison phase.
    Draws a bubble showing the user's choice and resumes the conversation.
    """
    draw_bubble(action_history, "Witch", f"Your Choice: Player {player_id} ({decision})", role_alignment="right")
    pause_playback.set()



heal_button = ttk.Button(potions_frame, text="Heal", command=lambda: select_potion("Heal"), width=12)
heal_button.pack(anchor='w', pady=2)

not_heal_button = ttk.Button(potions_frame, text="Not Heal", command=lambda: select_potion("Not Heal"), width=12)
not_heal_button.pack(anchor='w', pady=2)

poison_button = ttk.Button(potions_frame, text="Poison", command=lambda: select_potion("Poison"), width=12)
poison_button.pack(anchor='w', pady=2)

not_poison_button = ttk.Button(potions_frame, text="Not Poison", command=lambda: select_potion("Not Poison"), width=12)
not_poison_button.pack(anchor='w', pady=2)

# Role info and start game area under the potions
bottom_right_frame = ttk.Frame(info_frame)
bottom_right_frame.pack(fill='x', pady=5)

role_label = ttk.Label(bottom_right_frame, text="Your role: Witch")
role_label.pack(anchor='w')

name_label = ttk.Label(bottom_right_frame, text="Your name: Player6")
name_label.pack(anchor='w')

potion_info_label = ttk.Label(bottom_right_frame, text="Healing: 1   Poison: 1")
potion_info_label.pack(anchor='w')

# poison_info_label = ttk.Label(bottom_right_frame, text="Poison: 1")
# poison_info_label.pack(anchor='w')

witch_avatar_frame = ttk.Frame(bottom_right_frame)
witch_avatar_frame.pack(pady=0)
try:
    witch_image = Image.open("/Users/dennis/Desktop/src/tkinder/avatars/witch1.png").resize((120,120))
    witch_photo = ImageTk.PhotoImage(witch_image)
except Exception as e:
    print("Error loading witch.png:", e)
    witch_photo = None

# Create a Label with the image and pack it into the frame
if witch_photo:
    witch_avatar_label = ttk.Label(witch_avatar_frame, image=witch_photo, padding=0)
    witch_avatar_label.image = witch_photo  # Keep a reference to prevent garbage collection
    witch_avatar_label.pack()
else:
    witch_avatar_label = ttk.Label(witch_avatar_frame, text="[Witch Image]")
    witch_avatar_label.pack()


############################################################################################################################
# ========== 4) Console Frame =============
############################################################################################################################



console_frame = ttk.Frame(root, padding="5 5 5 5", height=50)
console_frame.pack(fill="x", padx=10, pady=5)
console_frame.pack_propagate(False)  # Prevent frame from resizing to fit its content

# Create and pack the Start, Pause, and Resume buttons
start_button = ttk.Button(console_frame, text="Start Game")
start_button.pack(side="left", padx=5, pady=0)
# Load conversation button

def pause_task():
    # Clear the event to pause the task
    pause_playback.clear()
    print("Task paused")

def resume_task():
    # Set the event to resume the task
    pause_playback.set()
    print("Task resumed")



pause_button = ttk.Button(console_frame, text="Pause Game", command=pause_task)
pause_button.pack(side="left", padx=5, pady=0)

resume_button = ttk.Button(console_frame, text="Resume Game", command= resume_task)
resume_button.pack(side="left", padx=5, pady=0)

quit_button = ttk.Button(console_frame, text="Quit Game", command=root.destroy)
quit_button.pack(side="left", padx=5, pady=0)

def draw_bubble(parent, sender, message, role_alignment="left"):
    # Create a frame for the bubble and avatar
    bubble_frame = tk.Frame(parent, bg="white", pady=5)
    bubble_frame.pack(fill=tk.X, padx=5, pady=5, anchor="e" if role_alignment == "right" else "w")

    # Add sender's name above the bubble
    name_label = tk.Label(bubble_frame, text=sender, font=("Arial", 10, "bold"), bg="white")
    name_label.pack(anchor="e" if role_alignment == "right" else "w", padx=(5, 0) if role_alignment == "right" else (0, 5))

    # Container for avatar and bubble
    content_frame = tk.Frame(bubble_frame, bg="white")
    content_frame.pack(anchor="e" if role_alignment == "right" else "w", padx=5)

    if sender in avatars:
        avatar_image = Image.open(avatars[sender]).resize((40, 40))
        avatar = ImageTk.PhotoImage(avatar_image)

        # Place avatar based on alignment
        avatar_label = tk.Label(content_frame, image=avatar, bg="white")
        avatar_label.image = avatar
        avatar_label.pack(side=tk.RIGHT if role_alignment == "right" else tk.LEFT, padx=5)

    bubble_canvas = Canvas(content_frame, bg="white", highlightthickness=0)

    # Set margin for text
    text_margin = 15  # Margin between text and bubble boundary

    # Initialize the bubble rectangle and text
    bubble_rect = bubble_canvas.create_rectangle(
        0, 0, 0, 0, fill="#f0f0f0", outline="#c0c0c0", width=2
    )
    text_id = bubble_canvas.create_text(
        text_margin, text_margin, text="", font=("Arial", 12), anchor="nw", fill="black", width=500
    )

    # Pack bubble to the right for Ethan
    bubble_canvas.pack(side=tk.RIGHT if role_alignment == "right" else tk.LEFT)

    def resize_bubble():
        """Resize the bubble dynamically based on text content."""
        text_bbox = bubble_canvas.bbox(text_id)
        if text_bbox:  # Ensure bbox exists
            bubble_width = (text_bbox[2] - text_bbox[0]) + text_margin * 2
            bubble_height = (text_bbox[3] - text_bbox[1]) + text_margin * 2
            bubble_canvas.coords(bubble_rect, 0, 0, bubble_width, bubble_height)
            bubble_canvas.config(width=bubble_width, height=bubble_height)

    def type_letter_by_letter():
        """Type the text letter by letter with random speed."""
        displayed_text = ""
        for char in message:
            displayed_text += char
            bubble_canvas.itemconfigure(text_id, text=displayed_text)
            resize_bubble()  # Resize bubble after updating text
            parent.update_idletasks()
            action_canvas.yview_moveto(1.0)
            time.sleep(random.uniform(0.001, 0.005))  # Typing speed

    if sender == "Witch":
        # For Ethan, directly display the full message without typing effect
        bubble_canvas.itemconfigure(text_id, text=message)
        resize_bubble()
    else:
        # For other roles, emulate typing effect
        type_letter_by_letter()

    # Automatically scroll to the bottom
    parent.update_idletasks()
    action_canvas.yview_moveto(1.0)


def thinking_effect(sender, delay):
    dots = [".", "..", "...", "....", ".....", "......"]
    for _ in range(delay * 1):  # Simulate thinking for `delay` seconds
        for dot in dots:
            typing_label.config(text=f"{sender} is thinking{dot}")
            time.sleep(0.3)
    typing_label.config(text="")  # Clear after thinking


# Function to simulate message playback with thinking effect
def play_conversation(conversation, delay=0.5):
    """Plays the conversation sequentially, ensuring one person types at a time."""
    for sender, message in conversation:
        if sender == "Witch":
            # Pause playback for Witch's turn
            pause_playback.clear()  # Player6 can submit his message manually
            typing_label.config(text="Your turn to respond in the public discussion!")
            ai_reply_button.config(command=lambda: input_text_box.insert("1.0", message))  # Insert AI reply
            pause_playback.wait()  # Wait for Ethan to submit before continuing
        elif sender == "Player6":
            # Pause playback for Witch's turn
            pause_playback.clear()  # Player6 can submit his message manually
            typing_label.config(text="Your turn to respond in the public discussion!")
            ai_reply_button.config(command=lambda: input_text_box.insert("1.0", message))  # Insert AI reply
            pause_playback.wait()  # Wait for Ethan to submit before continuing

        elif sender == "WitchHealing":
            typing_label.config(text="Your turn to CLICK the Healing Button! Choose to heal or not")
            
            # Reconfigure the healing buttons to record the user's decision.
            heal_button.config(command=lambda: on_heal_click("Heal"))
            not_heal_button.config(command=lambda: on_heal_click("Not Heal"))
            
            # Clear the event so the conversation waits until a decision is made.
            pause_playback.clear()
            pause_playback.wait() 

        elif sender == "WitchPoison":
            typing_label.config(text="Your turn to CLICK the Poison Button! Choose to poison or not")
            for btn in avatar_buttons:
                btn.config(state="disabled")
    
            
            # Reconfigure the healing buttons to record the user's decision.
            poison_button.config(command=lambda: on_poison_click("Poison"))
            not_poison_button.config(command=lambda: on_poison_click("Not Poison"))
            
            # Clear the event so the conversation waits until a decision is made.
            pause_playback.clear()
            pause_playback.wait() 
        
        elif sender == "WitchVote":
            typing_label.config(text="Your turn to Vote for the Player to Banish! Choose a player through the avatar")
            
            # Reconfigure all avatar buttons for the vote action.
            # When clicked, each avatar button will call on_vote_avatar_click with its player id.

            for i, btn in enumerate(avatar_buttons, start=1):
                btn.config(state="normal", command=lambda pid=i: on_vote_avatar_click(pid))
            
            pause_playback.clear()  # Pause the conversation until a vote is made
            pause_playback.wait() 

            pause_playback.set()            
            for btn in avatar_buttons:
                btn.config(state="disabled")
    
        elif sender == "Killed":
            # Assume message is formatted like "Player6"
            match = re.search(r'\d+', message)
    
            if match:
                player_id = int(match.group())  # Extract the number, e.g., 6
                # Check if the dead avatar for that player exists in avatar_dead
                if player_id in avatar_killed:
                    dead_avatar_path = avatar_killed[player_id]
                    # Load the dead avatar image
                    dead_image = Image.open(dead_avatar_path)
                    dead_image = dead_image.resize((50, 50))
                    dead_photo = ImageTk.PhotoImage(dead_image)
                    # Update the corresponding avatar button's image:
                    # Since players are numbered from 1, and our list is 0-indexed:
                    avatar_buttons[player_id - 1].config(image=dead_photo)
                    avatar_buttons[player_id - 1].image = dead_photo  # keep a reference so it's not garbage collected
                else:
                    print(f"No dead avatar found for player {player_id}")
            else:
                print("No player number found in message")

        elif sender == "Banished":
            # Assume message is formatted like "Player6"
            match = re.search(r'\d+', message)
    
            if match:
                player_id = int(match.group())  # Extract the number, e.g., 6
                # Check if the dead avatar for that player exists in avatar_dead
                if player_id in avatar_banished:
                    dead_avatar_path = avatar_banished[player_id]
                    # Load the dead avatar image
                    dead_image = Image.open(dead_avatar_path)
                    dead_image = dead_image.resize((50, 50))
                    dead_photo = ImageTk.PhotoImage(dead_image)
                    # Update the corresponding avatar button's image:
                    # Since players are numbered from 1, and our list is 0-indexed:
                    avatar_buttons[player_id - 1].config(image=dead_photo)
                    avatar_buttons[player_id - 1].image = dead_photo  # keep a reference so it's not garbage collected
                else:
                    print(f"No dead avatar found for player {player_id}")
            else:
                print("No player number found in message")


        elif sender == "Poisoned":
            # Assume message is formatted like "Player6"
            match = re.search(r'\d+', message)
    
            if match:
                player_id = int(match.group())  # Extract the number, e.g., 6
                # Check if the dead avatar for that player exists in avatar_dead
                if player_id in avatar_poisoned:
                    dead_avatar_path = avatar_poisoned[player_id]
                    # Load the dead avatar image
                    dead_image = Image.open(dead_avatar_path)
                    dead_image = dead_image.resize((50, 50))
                    dead_photo = ImageTk.PhotoImage(dead_image)
                    # Update the corresponding avatar button's image:
                    # Since players are numbered from 1, and our list is 0-indexed:
                    avatar_buttons[player_id - 1].config(image=dead_photo)
                    avatar_buttons[player_id - 1].image = dead_photo  # keep a reference so it's not garbage collected
                else:
                    print(f"No dead avatar found for player {player_id}")
            else:
                print("No player number found in message")
        else:
            # Show thinking effect before speaking
            thinking_effect(sender, delay)
            # Draw the bubble for the current role
            draw_bubble(action_history, sender, message)

        # Clear the typing indicator after the role finishes speaking
        typing_label.config(text="")
        action_canvas.update_idletasks()  # Refresh the interface to reflect the changes


# Function to load and play conversation history
def load_and_play_conversation():
    """Loads and plays the conversation in a separate thread."""
    file_path = "/Users/dennis/Desktop/src/tkinder/werewolf_game_script copy.txt"  # Update to the correct file path
    conversation = load_conversation(file_path, roles)
    threading.Thread(target=play_conversation, args=(conversation, 2), daemon=True).start()


# Submit button functionality
def submit_message():
    """Handles user submission and resumes conversation playback."""
    global pause_playback
    message = input_text_box.get("1.0", "end-1c")  # Fetch text from the input box
    if message.strip():  # Ensure the message is not empty
        draw_bubble(action_history, "Player6", message, role_alignment="right")
        input_text_box.delete("1.0", tk.END)  # Clear the input box
        adjust_input_height()  # Reset height to 3 lines
        pause_playback.set()  # Resume playback


submit_button.config(command=submit_message)


def load_and_play_conversation():
    """Loads and plays the conversation in a separate thread."""
    file_path = "/Users/dennis/Desktop/src/tkinder/werewolf_game_script copy.txt"  # Update to the correct file path
    conversation = load_conversation(file_path, roles)
    threading.Thread(target=play_conversation, args=(conversation, 2), daemon=True).start()

start_button.config(command=load_and_play_conversation)
root.mainloop()

# def play_conversation(conversation, delay=0.5):
#     """Plays the conversation sequentially, ensuring one person types at a time."""
#     for sender, message in conversation:
#         if sender == "Ethan_Turner":
#             # Pause playback for Ethan's turn
#             pause_playback.clear()  # Ethan can submit his message manually
#             typing_label.config(text="Your turn to respond!")
#             ai_reply_button.config(command=lambda: input_text.insert("1.0", message))  # Insert AI reply
#             pause_playback.wait()  # Wait for Ethan to submit before continuing
#         else:
#             # Show thinking effect before speaking
#             thinking_effect(sender, delay)
#             # Draw the bubble for the current role
#             draw_bubble(chat_history, sender, message)

#         # Clear the typing indicator after the role finishes speaking
#         typing_label.config(text="")
#         chat_canvas.update_idletasks()  # Refresh the interface to reflect the changes

# def load_conversation(file_path, roles=roles):
#     with open(file_path, "r") as file:
#         lines = file.readlines()

#     conversation = []
#     role_pattern = "|".join(re.escape(role) for role in roles)  # Create a regex pattern for all roles

#     for line in lines:
#         if line.strip():  # Ignore empty lines
#             # Match role names appearing at the start of the line
#             match = re.match(fr"^({role_pattern})['-_s ]?.*?:", line)
#             if match:
#                 role = match.group(1).strip()  # Extract the role name
#                 message = line.split(":", 1)[-1].strip()  # Extract the message after ":"
#                 conversation.append((role, message))

#     return conversation