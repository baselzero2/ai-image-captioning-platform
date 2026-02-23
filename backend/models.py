import sqlite3
import os

DB_PATH = 'dashboard.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_url TEXT,
                caption TEXT NOT NULL,
                has_face INTEGER NOT NULL,
                language TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
print("✅ Database initialized and table 'images' created.")
