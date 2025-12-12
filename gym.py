import random
import sqlite3
from datetime import date, timedelta
import datetime 

DATABASE_NAME = "gym_tracker"

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    print("Connecting to Database...")

    c.execute("""CREATE TABLE IF NOT EXISTS event_log (
              event_id INTEGER PRIMARY KEY AUTOINCREMENT,
              log_datetime TEXT NOT NULL,
              exercise_type TEXT NOT NULL,
              value_numeric REAL DEFAULT NULL,
              value_text TEXT DEFAULT NULL)""")
    
    conn.commit()
    conn.close()
    print("Database ready...")

def log_movements(event_type, reps):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat()

    c.execute("""INSERT INTO event_log (log_datetime, event_type, value_numeric) VALUES (?,?,?)""",(current_datetime, event_type, reps))

    conn.commit()
    conn.close()
    print(f"[DB Logged: new entry of {reps} repetitions for {event_type} at {current_datetime.split('T')[1].split['.'][0]}.]")

def get_movement_history():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("""SELECT log_datetime,
              exercise_type,
              value_numeric,
              value_text""")
    
    data = c.fetchall()

    conn.close()

    return data[::-1]

## --- DB portion of code ^ --- 

def get_num_input(num):
    if type(num) == int:
        return True
    else:
        if num.is_integer():
            return True
        else:
            return False




## --- Helper functions ^ ----

def add_gym_log():
    print("\n --- GYM DATA INPUT ---")

    while True:
        date_str = input("Enter the date (YYYY-MM-DD): ")
        if date_str.upper() == "QUIT":
            return
        try:
            date.isoformat(date_str)
            break
        except ValueError:
            print("Date is invalid please input in format (YYYY-MM-DD)")

    reps = input()




