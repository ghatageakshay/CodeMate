import sqlite3


def init_db(db_path: str = "database.db") -> None:
    """Create the `users` table if it does not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            skill_level TEXT,
            interests TEXT
        );
        """
    )

    cursor.execute("""
              CREATE TABLE IF NOT EXISTS connections(
                   id integer primary key AUTOINCREMENT,
                   sender_id integer,
                   receiver_id integer,
                   status TEXT DEFAULT 'pending',
                   created_at TIMESTAMP DEFAULT current_timestamp
                   );
""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database Initialized")