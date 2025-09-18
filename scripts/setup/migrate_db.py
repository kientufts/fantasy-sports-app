"""
Database migration script to add team management features
"""
import sqlite3
import os

def migrate_database():
    """Add is_on_my_team column to existing database"""
    db_path = 'fantasy_players.db'
    
    if not os.path.exists(db_path):
        print("Database does not exist yet. No migration needed.")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_on_my_team' not in columns:
            print("Adding is_on_my_team column to players table...")
            cursor.execute('ALTER TABLE players ADD COLUMN is_on_my_team BOOLEAN DEFAULT 0')
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("Column is_on_my_team already exists. No migration needed.")

if __name__ == "__main__":
    migrate_database()
