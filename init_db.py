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
    
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS messages(
            id integer primary key AUTOINCREMENT,
            sender_id integer,
            receiver_id integer,
            message text,
            sent_at TIMESTAMP DEFAULT current_timestamp,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
    );
"""
    )

    cursor.execute("""
        create table if not exists rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER,
        room_name TEXT,
        description TEXT,
        tech_stack TEXT,
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT current_timestamp,
        FOREIGN KEY (creator_id) REFERENCES users(id)
                   );
""")


    cursor.execute("""
        create table if not exists room_roles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER,
        role_name TEXT,
        role_description TEXT,
        skill_level TEXT,
        total_seats INTEGER,
        FOREIGN KEY(room_id) REFERENCES rooms(id)
                   );
""")
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_applications(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   room_id INTEGER,
                   role_id INTEGER,
                   applicant_id INTEGER,
                   github TEXT,
                   message TEXT,
                   status TEXT default 'pending',
                   applied_at TIMESTAMP default current_timestamp,
                   FOREIGN KEY (room_id) REFERENCES rooms(id),
                   FOREIGN KEY (role_id) REFERENCES room_roles(id),
                   FOREIGN KEY (applicant_id) REFERENCES users(id)
                   );
""")
 

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database Initialized")