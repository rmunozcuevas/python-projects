# Procrastination Central Program

# Global variables and Constants
song_limit = 10  # for scroll_time_punishment

# --- Helper Functions (Retained for other parts of the program) ---
def get_yes_no_input(prompt):
    """Repeatedly prompts the user until a valid 'yes' or 'no' is entered."""
    while True:
        x = input(prompt).strip().lower()
        if x in ["yes", "no"]:
            return x
        print("Yes or No answers only, please.")

def get_numeric_input(prompt, exit_word="QUIT"):
    """
    Repeatedly prompts the user for a number or the exit_word.
    Returns the float value or the exit_word (as a string).
    """
    while True:
        x = input(prompt).strip()
        if x.upper() == exit_word:
            return x.upper()
        try:
            return float(x)
        except ValueError:
            print("Please enter a valid number or type " + exit_word + ".")
# --- End Helper Functions ---

# Main Functions (Modified to match user's requested output style)
def lay_down():
    # Modified output
    print("Well, you are up — that's a start!\n")

def on_social_media():
    # Modified output
    print("You should probably get off of social media (Reddit | TikTok | X | Meta | Instagram | YouTube).\n")

def smells():
    # To match user's output "Yeah, definitely make sure that the room doesn't smell."
    # We remove the interactive part and just provide the advice.
    print("Yeah, definitely make sure that the room doesn't smell.\n")

def room():
    # To match user's output sequence, we print the prompts/advice directly.
    print("Is your room messy? Be honest with yourself.")
    print("Definitely clean up your room.")
    print("If your bedsheets haven't been cleaned in over a month, throw them in the washer along with pillowcases and blankets.\n")


def scroll_time_punishment():
    global song_limit
    print("--- Scroll Time Check ---")

    # Uses the new helper function
    minutes = get_numeric_input("Enter the amount of time you have scrolled on your phone in minutes (or type QUIT to exit): ")

    if minutes == "QUIT":
        print("Exiting scroll check.\n")
        return

    if minutes > 120:
        print("You must decrease the amount of time scrolling on your phone!")
        song_limit -= 5
        print("You can listen to this many songs today now:", song_limit, "\n")
    else:
        print("Good job! You are within a healthy scrolling limit.\n")

def achievements():
    print("--- Study Achievements Check ---")

    # Uses the new helper function
    minutes = get_numeric_input("Enter the amount of time you have studied in minutes (or type QUIT to exit): ")

    if minutes == "QUIT":
        print("Exiting achievements check.\n")
        return

    if minutes >= 180:
        print("You have reached MASTER level (>= 180 minutes of studying)\n")
    elif minutes >= 120:
        print("You have reached SENSEI level (>= 120 minutes)\n")
    elif minutes >= 60:
        print("You have reached NOVICE level (>= 60 minutes)\n")
    else:
        print("Go harder bro, you got this!\n")

# Main program
def main():
    # Note: I am removing the initial welcome messages to match your output exactly.
    while True:
        # Note: I've updated the initial prompt to match your output's line break exactly
        person = input(
            "What are you currently doing right now? (Laying on bed | On Social Media | Studying | Other | QUIT to exit): "
        ).strip().lower()

        if person == "quit":
            print("Exiting the program. Stay productive!\n")
            break

        elif person == "laying on bed":
            # Modified this block to remove the separator to match your desired output flow
            lay_down()
            on_social_media()
            smells()
            room()
            # The next prompt is printed by the main loop's continuation
            
        elif person == "on social media":
            on_social_media()
            scroll_time_punishment()
            print("--- Choose your next activity or type QUIT to exit ---\n")

        elif person == "studying":
            achievements()
            print("--- Choose your next activity or type QUIT to exit ---\n")

        else:
            print("Ok, just making sure you are staying aware of your habits!\n")
            print("--- Choose your next activity or type QUIT to exit ---\n")
            
        # Prints the prompt for the next loop iteration
        if person != "quit":
            print("What are you currently doing right now? (Laying on bed | On Social Media | Studying | Other | QUIT to exit):\n")

# Run the program
if __name__ == "__main__":
    main()