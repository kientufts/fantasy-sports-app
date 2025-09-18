#!/usr/bin/env python3
"""
Force recreate database for fantasy sports app
This will delete the existing database and create a fresh one
"""
import os
import sys
import sqlite3

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, project_root)

from src.core.database import Database

def force_recreate_database():
    """Delete existing database and create a fresh one"""
    # Database path
    db_path = os.path.join(project_root, 'data', 'fantasy_players.db')
    
    print(f"Project root: {project_root}")
    print(f"Database path: {db_path}")
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        try:
            os.remove(db_path)
            print("✅ Old database removed")
        except Exception as e:
            print(f"❌ Error removing old database: {e}")
            return False
    
    # Ensure data directory exists
    data_dir = os.path.dirname(db_path)
    os.makedirs(data_dir, exist_ok=True)
    print(f"✅ Data directory ready: {data_dir}")
    
    # Create fresh database with basic SQLite test
    try:
        print("Creating fresh database...")
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.execute("DROP TABLE test")
        conn.close()
        print("✅ SQLite connection test successful")
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
        return False
    
    # Now create with our Database class
    try:
        print("Initializing with Database class...")
        db = Database(db_path)
        
        # Test leagues
        leagues = db.get_all_leagues()
        print(f"✅ Database created with {len(leagues)} leagues:")
        for league in leagues:
            print(f"  - {league.display_name} (ID: {league.id})")
        
        return db_path
    except Exception as e:
        print(f"❌ Database class initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = force_recreate_database()
    if result:
        print(f"\n🎉 Database successfully created at: {result}")
        print("\nNext steps:")
        print("1. cd scripts/setup")
        print("2. python3 populate_leagues.py")
    else:
        print("\n❌ Database creation failed")
