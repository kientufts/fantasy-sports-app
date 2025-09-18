#!/usr/bin/env python3
"""
Simple database setup script for fantasy sports app
Run this from the main project directory to create and populate the database
"""
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import Database

def create_database():
    """Create database with proper path handling"""
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Database path
    db_path = os.path.join(data_dir, 'fantasy_players.db')
    print(f"Creating database at: {db_path}")
    
    # Create database instance (this will create the file and tables)
    db = Database(db_path)
    
    # Test database
    leagues = db.get_all_leagues()
    print(f"✅ Database created successfully with {len(leagues)} leagues")
    
    # Check if we need to populate
    total_players = 0
    for league in leagues:
        players = db.get_players_by_league(league.id)
        total_players += len(players)
        print(f"  {league.display_name}: {len(players)} players")
    
    if total_players == 0:
        print("\n🔄 Database is empty. Run the populate script to add sample data:")
        print("python scripts/setup/populate_leagues.py")
    else:
        print(f"\n✅ Database ready with {total_players} total players")
    
    return db_path

if __name__ == "__main__":
    try:
        db_path = create_database()
        print(f"\n🎉 Setup complete! Database ready at: {db_path}")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
