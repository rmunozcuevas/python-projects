# Procrastination Central Program
import random
import sqlite3
from datetime import date, timedelta
import datetime 


# --- DATABASE SETUP (SIMPLE FILENAME USED) ---
DATABASE_NAME = "habits.db" 

def setup_database():
    """Initializes the SQLite database and creates the single event_log table."""
    conn = sqlite3.connect(DATABASE_NAME) 
    c = conn.cursor()
    print("Connecting to database...")
    
    # NEW: Single, high-frequency Event Log table
    # This replaces daily_log and music_log
    c.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_datetime TEXT NOT NULL,
            event_type TEXT NOT NULL,  -- e.g., 'study', 'scroll', 'room', 'music'
            value_numeric REAL DEFAULT NULL, -- for minutes (study/scroll)
            value_text TEXT DEFAULT NULL     -- for genre (music) or status (room)
        )
    """)
    
    # Note: Previous tables (daily_log, music_log) will be ignored by this new setup, 
    # but the old code for column migration is removed for simplicity.
        
    conn.commit()
    conn.close()
    print("Database ready.")

# --- UPDATED LOGGER FOR NUMERIC VALUES (SCROLL/STUDY) ---
def log_minutes(event_type, minutes):
    """Inserts a new event log entry for study or scroll minutes."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat()
    
    # Inserts a brand new row every time!
    c.execute("""
        INSERT INTO event_log (log_datetime, event_type, value_numeric)
        VALUES (?, ?, ?)
    """, (current_datetime, event_type, minutes))
    
    conn.commit()
    conn.close()
    print(f"\n[DB Logged: New entry of {minutes} minutes for {event_type} at {current_datetime.split('T')[1].split('.')[0]}.]")

# --- UPDATED LOGGER FOR ROOM STATUS ---
def log_room_clean_status(status):
    """Logs the room cleaning status as a new event."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat()
    
    status_text = 'Clean' if status == 1 else 'Messy'

    c.execute("""
        INSERT INTO event_log (log_datetime, event_type, value_text)
        VALUES (?, ?, ?)
    """, (current_datetime, 'room_clean', status_text))
    
    conn.commit()
    conn.close()
    print(f"\n[DB logged: Room status set to {status_text} at {current_datetime.split('T')[1].split('.')[0]}.]")

# --- UPDATED LOGGER FOR MUSIC GENRE ---
def log_random_music_genre_history(genre_name):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    current_datetime = datetime.datetime.now().isoformat() 
    
    # Inserts a brand new row every time!
    c.execute("""
        INSERT INTO event_log (log_datetime, event_type, value_text)
        VALUES (?, ?, ?)
    """, (current_datetime, 'music_genre', genre_name))
    
    conn.commit()
    conn.close()
    
    print(f"[DB Logged: Music genre '{genre_name}' logged at {current_datetime.split('T')[1].split('.')[0]}.]")

# --- UPDATED GETTER FOR REPORT DATA (SUMS EVENTS BY DATE) ---
def get_report_data():
    """Retrieves the last 7 unique days of aggregated logged data."""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    # SQL aggregates the data by day and pivots the event types into columns
    c.execute("""
        SELECT 
            STRFTIME('%Y-%m-%d', log_datetime) as log_date,
            SUM(CASE WHEN event_type = 'study' THEN value_numeric ELSE 0 END) as study_minutes,
            SUM(CASE WHEN event_type = 'scroll' THEN value_numeric ELSE 0 END) as scroll_minutes
        FROM event_log
        GROUP BY log_date
        ORDER BY log_date DESC 
        LIMIT 7
    """)
    
    data = c.fetchall()
    conn.close()
    
    return data[::-1]

# --- UPDATED GETTER FOR MUSIC HISTORY (GETS ALL EVENTS) ---
def get_random_music_genre_history():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    # Pulls the 15 most recent music events
    c.execute("""SELECT log_datetime, value_text
              FROM event_log 
              WHERE event_type = 'music_genre'
              ORDER BY event_id DESC
              LIMIT 15""")
    
    data = c.fetchall()
    conn.close()
    
    return data[::-1]

# --- UPDATED GETTER FOR ROOM HISTORY (GETS LATEST STATUS PER DAY) ---
def get_room_history():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    # Use a subquery to find the latest room status for each unique day
    c.execute("""
        SELECT t1.log_date, t1.value_text
        FROM (
            SELECT 
                STRFTIME('%Y-%m-%d', log_datetime) as log_date, 
                value_text,
                MAX(event_id) as max_id
            FROM event_log
            WHERE event_type = 'room_clean'
            GROUP BY log_date
        ) AS t1
        ORDER BY t1.log_date DESC
        LIMIT 7
    """)
    
    data = c.fetchall()
    conn.close()

    # Convert status text ('Clean'/'Messy') back to 1/0 for streak calculation
    processed_data = []
    for log_date, status_text in data:
        status = 1 if status_text == 'Clean' else 0
        processed_data.append((log_date, status))
        
    return processed_data[::-1]


# --- HISTORICAL INPUT FUNCTION (NOW INSERTS INTO EVENT_LOG) ---
def add_historical_log():
    """Allows manual entry of past dates for testing report functionality."""
    print("\n--- HISTORICAL DATA INPUT ---")
    
    # Get the date
    while True:
        date_str = input("Enter date for log (YYYY-MM-DD, e.g., 2023-12-10, or QUIT): ").strip()
        if date_str.upper() == "QUIT":
            return
        try:
            date.fromisoformat(date_str)
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Get study and scroll minutes
    study = get_numeric_input("Enter study minutes for this date: ")
    scroll = get_numeric_input("Enter scroll minutes for this date: ")

    # Get room status
    cleaned_input = get_yes_no_input("Was the room clean on this date? (yes/no): ").lower()
    room_clean_status_text = 'Clean' if cleaned_input == "yes" else 'Messy'
    
    # Get music genre (Optional)
    music_genre_input = input("Enter music genre (or leave blank): ").strip()

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # 1. Log Study Minutes (must be done this way to emulate logging)
    if study > 0:
        c.execute("INSERT INTO event_log (log_datetime, event_type, value_numeric) VALUES (?, ?, ?)", 
                  (f"{date_str}T00:00:00", 'study', study))
    
    # 2. Log Scroll Minutes
    if scroll > 0:
        c.execute("INSERT INTO event_log (log_datetime, event_type, value_numeric) VALUES (?, ?, ?)", 
                  (f"{date_str}T00:00:01", 'scroll', scroll))
                  
    # 3. Log Room Status
    c.execute("INSERT INTO event_log (log_datetime, event_type, value_text) VALUES (?, ?, ?)", 
              (f"{date_str}T00:00:02", 'room_clean', room_clean_status_text))
    
    # 4. Log Music Genre
    if music_genre_input:
        c.execute("INSERT INTO event_log (log_datetime, event_type, value_text) VALUES (?, ?, ?)", 
                  (f"{date_str}T00:00:03", 'music_genre', music_genre_input))


    conn.commit()
    conn.close()
    print(f"\n[DB Logged: Historical data added for {date_str}.]")


# --- Remaining functions (progress_report, music_genre_report, etc.) are below, 
# --- as they call the updated getters.

def music_genre_report():
    """Calculates and displays the most frequent genres listened to in the last 15 entries."""
    print("\n--- MUSIC GENRE REPORT ---")
    
    data = get_random_music_genre_history()
    
    if not data or all(genre is None for date, genre in data):
        print("No music genre data logged in the last 15 entries.")
        return

    # Count the frequency of each genre
    genre_counts = {}
    
    # Track the chronological history to print
    history = []
    
    for log_datetime, genre in data:
        # Extract date and time for cleaner display
        log_date = log_datetime.split('T')[0]
        # Check if time exists before splitting
        if 'T' in log_datetime:
            log_time = log_datetime.split('T')[1].split('.')[0]
        else:
            log_time = "N/A"
        
        if genre: # Only process non-NULL genres
            history.append(f"Date {log_date} @ {log_time}: {genre}")
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    print("---- Last 15 Detailed Genre History Entries ----")
    for line in history:
        print(line)
    
    print("-" * 30)

    if genre_counts:
        # Find the most frequent genre
        most_frequent_genre = max(genre_counts, key=genre_counts.get)
        max_count = genre_counts[most_frequent_genre]
        
        print(f"🎶 Most Frequent Genre (Last 15 Entries): **{most_frequent_genre}** (Listened to {max_count} time(s))")
    else:
        print("No music genres were logged successfully.")

    print("--------------------------------\n")


def room_streak_report():
    print("\n --- ROOM CLEANLINESS REPORT ---")
    # get_room_history now returns (log_date, 1 or 0)
    data = get_room_history()

    if not data:
        print("No room cleanliness logged")
        return
    
    current_streak = 0

    # Streak is calculated based on the last 7 unique days returned by get_room_history
    for log_date, status in reversed(data):
        if status == 1:
            current_streak += 1
        else:
            break

    print("-" * 30)
    if current_streak > 0:
        print(f"Current clean streak {current_streak} day(s) KEEP IT GOING!!!")
    else:
        if data and data[-1][1] == 0:
            print("Current clean streak: 0 days. Let's make today a new beginning!")
        else:
            print("Current clean streak: 0 days (check your logs!)")
    
    print("---- Last 7 Days Status ----")
    for log_date, status in data:
        status_text = "Clean" if status == 1 else "Messy"
        print(f"Date {log_date}: {status_text} (Last status recorded)")

    print("-----------------------------\n")


def progress_report():
    """Calculates and displays weekly average study and scroll times, including debug data."""
    print("\n--- WEEKLY PROGRESS REPORT ---")
    
    data = get_report_data() # Data is now aggregated study/scroll minutes per day
    
    # DEBUGGING PRINT TO VERIFY DATA IS READ
    print("\n--- RAW DATABASE DATA (LAST 7 DAYS) ---")
    if data:
        for row in data:
            print(f"Date: {row[0]}, Study: {row[1]}, Scroll: {row[2]}")
    else:
        print("Raw data check: DATABASE IS EMPTY.")
    print("--------------------------------------\n")
    
    if not data:
        print("No habit data logged in the last 7 days. Go track some habits!")
        print("----------------------------\n")
        return

    total_study = sum(row[1] for row in data)
    total_scroll = sum(row[2] for row in data)
    
    # Days logged is based on how many unique dates have data
    days_logged = len(data) 
    
    # Average calculation needs the actual number of days logged, not a fixed 7
    if days_logged > 0:
        avg_study = total_study / days_logged
        avg_scroll = total_scroll / days_logged
    else:
        avg_study = 0
        avg_scroll = 0
    
    print(f"Days Logged: {days_logged} (unique days with data)")
    print("-" * 30)
    
    # Study Report
    print(f"✅ Avg Daily Study: {avg_study:.2f} minutes")
    if avg_study >= SENSEI_STUDY_MINUTES:
        print("    Status: Excellent! You are hitting SENSEI average!")
    elif avg_study >= NOVICE_STUDY_MINUTES:
        print("    Status: Solid effort! Keep pushing for the next tier.")
    else:
        print("    Status: You can aim higher! Let's hit 60 mins average this week.")
        
    print("-" * 30)

    # Scroll Report
    print(f"📱 Avg Daily Scroll: {avg_scroll:.2f} minutes")
    if avg_scroll <= SCROLL_LIMIT_MINUTES:
        print("    Status: Great Control! Stay under the 120-minute limit.")
    else:
        print(f"    Status: Warning! Avg scroll time is {avg_scroll - SCROLL_LIMIT_MINUTES:.2f} mins over the healthy limit!")

    
    room_streak_report()

    music_genre_report()
        
    print("----------------------------\n")


# Global variables and Constants
song_limit = 10  # for scroll_time_punishment
SCROLL_LIMIT_MINUTES = 120
MASTER_STUDY_MINUTES = 180
SENSEI_STUDY_MINUTES = 120
NOVICE_STUDY_MINUTES = 60


# --- Helper Functions (No change) ---
def get_yes_no_input(prompt):
    while True:
        x = input(prompt).strip().lower()
        if x in ["yes", "no"]:
            return x
        print("Yes or No answers only, please.")

def get_numeric_input(prompt, exit_word="QUIT"):
    while True:
        x = input(prompt).strip()
        if x.upper() == exit_word:
            return x.upper()
        try:
            return float(x)
        except ValueError:
            print("Please enter a valid number or type " + exit_word + ".")

# --- End Helper Functions ---

# --- Core Functions (No change) ---

def lay_down():
    print("Well, you are up — that's a start!\n")

def on_social_media():
    print("You should probably get off of social media (Reddit | TikTok | X | Meta | Instagram | YouTube).\n")

def smells():
    print("Yeah, definitely make sure that the room doesn't smell.\n")

def room():
    print("Did you clean your room?\n")
    print("\n --Clothes are clean (washed and folded)\n")
    print("\n --Jackets are hung on the rack\n")
    print("\n --There are no items on the floor \n")
    print("\n --Items are put away in the area where they belong \n")

    cleaned = get_yes_no_input("Did you clean your room just now? (y/n):")

    if cleaned == "yes":
        log_room_clean_status(1)
        print("Amazing job! Your room is definitely clean, you may continue on to other things (: )")
    else:
        log_room_clean_status(0)
        print("Remember a room reflects the status of your mind, so if its dirty, then fix it ASAP (: )")


def scroll_time_punishment():
    global song_limit
    print("--- Scroll Time Check ---")

    # Event type is 'scroll'
    minutes = get_numeric_input("Enter the amount of time you have scrolled on your phone in minutes (or type QUIT to exit): ")

    if minutes == "QUIT":
        print("Exiting scroll check.\n")
        return

    log_minutes("scroll", minutes)

    if minutes > SCROLL_LIMIT_MINUTES:
        print("You must decrease the amount of time scrolling on your phone!")
        song_limit -= 5
        print("You can listen to this many songs today now:", song_limit, "\n")
    else:
        print("Good job! You are within a healthy scrolling limit.\n")

def music_genre():
    genres = ["Pop","Trap","Underground","EDM","J-Pop","Shoegaze","Emo","Math Rock","hyperpop","Rage","Midwest Emo","Dariacore","Bossa Nova","Breakcore","Alternative Indie"]
    suggest_genres = random.choice(genres) 
    
    log_random_music_genre_history(suggest_genres)

    print(f"Top suggestion for the day: {suggest_genres}\n")


def achievements():
    print("--- Study Achievements Check ---")

    # Event type is 'study'
    minutes = get_numeric_input("Enter the amount of time you have studied in minutes (or type QUIT to exit): ")

    if minutes == "QUIT":
        print("Exiting achievements check.\n")
        return

    log_minutes("study", minutes)

    if minutes >= MASTER_STUDY_MINUTES:
        print("You have reached MASTER level (>= 180 minutes of studying)\n")
    elif minutes >= SENSEI_STUDY_MINUTES:
        print("You have reached SENSEI level (>= 120 minutes)\n")
    elif minutes >= NOVICE_STUDY_MINUTES:
        print("You have reached NOVICE level (>= 60 minutes)\n")
    else:
        print("Go harder bro, you got this!\n")

# Main program
def main():
    while True:
        person = input(
            "What are you currently doing right now? (Laying on bed | On Social Media | Studying | listening to music | Other | HISTORY | REPORT | QUIT to exit): "
        ).strip().lower()

        if person == "quit":
            print("Exiting the program. Stay productive!\n")
            break

        elif person == "laying on bed":
            lay_down()
            on_social_media()
            smells()
            room()
            
        elif person == "on social media":
            on_social_media()
            scroll_time_punishment()

        elif person == "studying":
            achievements()

        elif person == "listening to music":
            music_genre()
        
        elif person == "history":
            add_historical_log()
            
        elif person == "report":
            progress_report()

        else:
            print("Ok, just making sure you are staying aware of your habits!\n")
            
        if person != "quit":
            print("--- Choose your next activity or type QUIT to exit ---\n")


# Run the program
if __name__ == "__main__":
    setup_database() 
    main()