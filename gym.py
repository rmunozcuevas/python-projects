import random
import sqlite3
from datetime import date, timedelta
import datetime 

DATABASE_NAME = "gym_tracker.db"

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    print("Connecting to Database...")

    # c.execute("DROP TABLE IF EXISTS event_log")

    c.execute("""CREATE TABLE IF NOT EXISTS event_log (
              event_id INTEGER PRIMARY KEY,  
              log_datetime TEXT NOT NULL,
              exercise_day TEXT NOT NULL,
              exercise_type TEXT NOT NULL,
              value_numeric REAL DEFAULT NULL,
              value_text TEXT DEFAULT NULL,   
              weight_lbs REAL DEFAULT NULL
              )""")
    
    conn.commit()
    conn.close()
    print("Database ready...")


def log_movements(exercise_day, exercise_type, reps, weight, message): 
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat()

    c.execute("""INSERT INTO event_log (log_datetime
              , exercise_day
              ,exercise_type,
              value_numeric,
              weight_lbs,
              value_text) VALUES (?,?,?,?,?,?) 
              """,(current_datetime, exercise_day, exercise_type, reps, weight, message)) 

    conn.commit()
    conn.close()
    time_str = current_datetime.split('T')[1].split('.')[0]
    
    message_snippet = f" Note: '{message[:20]}...'" if message else ""
    print(f"[DB Logged: new entry of {reps} reps @ {weight:.0f} lbs for {exercise_type} on {exercise_day} day at {time_str}.{message_snippet}]")


# --- MODIFIED FUNCTION: Weight prompt moved INSIDE the loop ---
def log_exercise_set(day_name, exercise_name):
    """Handles the repetitive logging of sets, prompting for weight per set."""
    set_num = 1
    last_weight = 0.0 # Initialize last_weight
    

    while True:
        
        # 1. PROMPT FOR WEIGHT (FIRST INPUT INSIDE THE LOOP)
        weight_prompt = f"Enter weight (lbs) for {exercise_name} (Set {set_num}, Last: {last_weight:.0f} lbs, or type DONE): "
        weight_input = input(weight_prompt).strip()
        
        if weight_input.upper() == "DONE":
            break

        # 2. HANDLE WEIGHT INPUT & VALIDATION
        try:
            if weight_input == "" and set_num > 1:
                weight = last_weight # Reuse last weight if user hits Enter
            else:
                weight = float(weight_input)
                
            if weight < 0:
                print("Weight must be zero or a positive number.")
                continue

        except ValueError:
            print("Invalid weight input. Enter a number or DONE.")
            continue


        # 3. PROMPT FOR REPS
        reps_prompt = f"Enter reps for {exercise_name} (Set {set_num}): "
        reps_input = input(reps_prompt).strip()
        
        if reps_input.upper() == "DONE":
            break # User can still type DONE here, though it's less likely

        # 4. HANDLE REPS INPUT & VALIDATION
        try:
            reps = float(reps_input)
            
            if reps >= 0:
                # 5. Add a new prompt for the optional descriptive message
                message = input(f"Add a note for Set {set_num} (Optional): ").strip()
                
                # 6. Log the movement
                log_movements(day_name, exercise_name, reps, weight, message)
                
                # Update tracker variables
                last_weight = weight
                set_num += 1
                
                # 3-Set Auto-stop Logic
                if set_num > 3: 
                    print("\n--- You have completed 3 sets for this exercise. ---")
                    continue_ans = yes_or_no("Do you want to continue for another set (yes/no)? ")
                    if continue_ans == "no":
                        break
                
            else:
                print("Reps must be zero or a positive number.")
        except ValueError:
            print("Invalid reps input. Enter a number.")


def handle_workout_day(day_name):
    """Loops, prompting the user for exercises until they type 'DONE'."""
    print(f"\n--- Starting {day_name} Day Workout ---")
    while True:
        exercise_name = input(f"Enter the exercise for {day_name} (e.g., Bench Press, or type DONE): ").strip()
        
        if exercise_name.upper() == "DONE":
            break
        
        if not exercise_name:
            continue

        log_exercise_set(day_name, exercise_name)
    
    print(f"\n{day_name} Day workout finished and logged!")

def get_movement_history():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("""SELECT log_datetime,
              exercise_type,
              value_numeric,
              weight_lbs,
              exercise_day,
              value_text
              FROM event_log
              ORDER BY log_datetime DESC
              LIMIT 10
              """)
    
    data = c.fetchall()
    conn.close()
    return data[::-1] 

def display_report():
    print("\n--- RECENT GYM LOGS (LAST 10 ENTRIES) ---")
    data = get_movement_history()

    if not data:
        print("No gym history logged.")
        return
    
    print(f"{'Date':<10} | {'Time':<8} | {'Day':<8} | {'Exercise':<20} | {'Reps':<5} | {'Weight (lbs)':<12} | {'Note/Message':<25}")
    print("-" * 105) 
    
    for row in data:
        log_datetime, exercise_type, reps, weight, exercise_day, message = row
        
        log_date = log_datetime.split('T')[0]
        log_time = log_datetime.split('T')[1].split('.')[0]
        
        display_message = message if message else ""

        print(f"{log_date:<10} | {log_time:<8} | {exercise_day:<8} | {exercise_type:<20} | {reps:<5.0f} | {weight:<12.0f} | {display_message:<25}")
    
    print("-" * 105)

        
def get_numeric_input(prompt):
    # NOTE: This function is currently unused, but kept for general utility.
    while True:
        x = input(prompt).strip()
        try:
            return float(x)
        except ValueError:
            print("Please enter a valid number (reps, weight, etc)")
        
def yes_or_no(ans):
    while True:
        x = input(ans).strip().lower()
        if x in ["yes","no"]:
            return x
        print("Yes or No answers please")


def main():
    while True:
        user_input = input("Enter the day (Push | Pull | Legs) or type REPORT/QUIT: ").strip().lower()

        if user_input == "quit":
            print("Exiting Gym Tracker ... Have a Great Day!")
            break
            
        elif user_input == "report":
            display_report()
            continue
            
        if user_input in ["push","pull","legs"]:
            day_name = user_input.capitalize()
            handle_workout_day(day_name)
        else:
            print("Invalid input. Please choose Push, Pull, Legs, or type REPORT/QUIT.")
            

if __name__ == "__main__":
    setup_database()
    main()