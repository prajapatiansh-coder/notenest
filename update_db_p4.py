import sqlite3
import os

db_path = 'instance/campus_notes.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Update Note table
        cursor.execute("ALTER TABLE note ADD COLUMN ai_summary TEXT;")
        
        # Create AIChat table
        cursor.execute("""
        CREATE TABLE aichat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        # Create AIQuiz table
        cursor.execute("""
        CREATE TABLE aiquiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            options JSON,
            answer TEXT NOT NULL,
            question_type VARCHAR(20) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        # Create Flashcard table
        cursor.execute("""
        CREATE TABLE flashcard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_id INTEGER NOT NULL,
            front_text TEXT NOT NULL,
            back_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        conn.commit()
        print("Phase 4 database updates completed successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database not found at {db_path}")
