import sqlite3
import os

db_path = 'instance/campus_notes.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Update User table
        cursor.execute("ALTER TABLE user ADD COLUMN avatar VARCHAR(100) DEFAULT 'default.jpg' NOT NULL;")
        
        # Create Like table
        cursor.execute("""
        CREATE TABLE like (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        # Create Bookmark table
        cursor.execute("""
        CREATE TABLE bookmark (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        # Create Comment table
        cursor.execute("""
        CREATE TABLE comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (note_id) REFERENCES note (id)
        );
        """)
        
        # Create Notification table
        cursor.execute("""
        CREATE TABLE notification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message VARCHAR(255) NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            link VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        );
        """)
        
        conn.commit()
        print("Phase 3 database updates completed successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database not found at {db_path}")
