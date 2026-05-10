import sqlite3
import os

db_path = 'instance/campus_notes.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE note ADD COLUMN downloads INTEGER DEFAULT 0;")
        conn.commit()
        print("Column 'downloads' added successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database not found at {db_path}")
