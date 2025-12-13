import random
import sqlite3
from datetime import date, timedelta
import datetime 

DATABASE_NAME = "gym_tracker.db"

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    print("Connecting to Database...")

    c.execute("""CREATE TABLE IF NOT EXISTS event_log (
              event_id INTEGER PRIMARY KEY AUTOINCREMENT,
              log_datetime TEXT NOT NULL,
              exercise_day TEXT NOT NULL,
              exercise_type TEXT NOT NULL,
              value_numeric REAL DEFAULT NULL,
              value_text TEXT DEFAULT NULL,
              weight_lbs REAL DEFAULT NULL  -- NEW COLUMN ADDED HERE
              )""")
    
    conn.commit()
    conn.close()
    print("Database ready...")

# --- 2. Update Logging Function ---
def log_movements(exercise_day, exercise_type, reps, weight): # Added 'weight' parameter
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat()

    # Updated SQL to include 'weight_lbs' column and a new placeholder (?)
    c.execute("""INSERT INTO event_log (log_datetime
              , exercise_day
              ,exercise_type,
              value_numeric,
              weight_lbs) VALUES (?,?,?,?,?) 
              """,(current_datetime, exercise_day, exercise_type, reps, weight)) # Added 'weight' value

    conn.commit()
    conn.close()
    time_str = current_datetime.split('T')[1].split('.')[0]
    # Updated print statement to show both reps and weight
    print(f"[DB Logged: new entry of {reps} reps @ {weight:.0f} lbs for {exercise_type} on {exercise_day} day at {time_str}.]")


# --- 3. Update Input/Logging Flow ---
def log_exercise_set(day_name, exercise_name):
    """Handles the repetitive logging of sets for a single, dynamically named exercise."""
    set_num = 1
    
    # Prompt for weight once per exercise
    weight = get_numeric_input(f"Enter the weight (lbs) for {exercise_name}: ")

    while True:
        prompt = f"Enter reps for {exercise_name} (Set {set_num}) or type DONE: "
        
        reps_input = input(prompt).strip().upper()
        
        if reps_input == "DONE":
            break 
            
        try:
            reps = float(reps_input)
            if reps >= 0:
                # Pass weight to the logging function
                log_movements(day_name, exercise_name, reps, weight) 
                set_num += 1
            else:
                print("Reps must be zero or a positive number.")
        except ValueError:
            print("Invalid input. Enter a number or DONE.")

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


# --- 4. Update Reporting Functions ---
def get_movement_history():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Updated SELECT statement to retrieve the new 'weight_lbs' column
    c.execute("""SELECT log_datetime,
              exercise_type,
              value_numeric,
              weight_lbs,          -- NEW COLUMN RETRIEVED
              exercise_day
              FROM event_log
              ORDER BY log_datetime DESC
              LIMIT 10
              """)
    
    data = c.fetchall()
    conn.close()
    # Returning in chronological order for easier reading
    return data[::-1] 

def display_report():
    print("\n--- RECENT GYM LOGS (LAST 10 ENTRIES) ---")
    data = get_movement_history()

    if not data:
        print("No gym history logged.")
        return
    
    # Updated header to include Weight
    print(f"{'Date':<10} | {'Time':<8} | {'Day':<8} | {'Exercise':<20} | {'Reps':<5} | {'Weight (lbs)':<12}")
    print("-" * 75)
    
    for row in data:
        # Adjusted unpacking to retrieve weight: (datetime, type, reps, weight, day)
        log_datetime, exercise_type, reps, weight, exercise_day = row
        
        log_date = log_datetime.split('T')[0]
        log_time = log_datetime.split('T')[1].split('.')[0]

        # Updated print line to include weight
        print(f"{log_date:<10} | {log_time:<8} | {exercise_day:<8} | {exercise_type:<20} | {reps:<5.0f} | {weight:<12.0f}")
    
    print("-" * 75)


## --- DB portion of code ^ --- 
        
def get_numeric_input(prompt):
    # This helper is used to read both reps and weight inputs
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


## --- Helper functions ^ ----

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