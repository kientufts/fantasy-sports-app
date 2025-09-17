"""
Multi-League Database Migration Script

This script migrates the existing database to support multiple fantasy leagues:
- F1 (Formula 1)
- EPL (English Premier League)
- UCL (UEFA Champions League)
- NFL (National Football League)

Creates leagues table and adds league_id to players table.
"""

import sqlite3
import json
import os
from datetime import datetime

def migrate_to_multi_league():
    """Migrate database to support multiple leagues"""
    db_path = 'fantasy_players.db'
    
    if not os.path.exists(db_path):
        print("Database does not exist yet. No migration needed.")
        return
    
    print("🏆 Starting Multi-League Migration...")
    print("=" * 50)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if leagues table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leagues'")
        if cursor.fetchone():
            print("✅ Leagues table already exists. Checking for updates...")
        else:
            print("📅 Creating leagues table...")
            
            # Create leagues table
            cursor.execute('''
                CREATE TABLE leagues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL,
                    sport_type TEXT NOT NULL,
                    description TEXT,
                    scoring_system TEXT DEFAULT 'weighted',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert default leagues
            leagues_data = [
                ('f1', 'Formula 1', 'Motorsport', 'Formula 1 Championship racing with drivers and constructors', 'weighted'),
                ('epl', 'English Premier League', 'Football', 'English Premier League football/soccer', 'weighted'),
                ('ucl', 'UEFA Champions League', 'Football', 'UEFA Champions League European football', 'weighted'),
                ('nfl', 'National Football League', 'American Football', 'NFL American Football league', 'weighted')
            ]
            
            cursor.executemany('''
                INSERT INTO leagues (name, display_name, sport_type, description, scoring_system)
                VALUES (?, ?, ?, ?, ?)
            ''', leagues_data)
            
            print("✅ Created leagues table with 4 leagues")
        
        # Check if league_id column exists in players table
        cursor.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'league_id' not in columns:
            print("📅 Adding league_id column to players table...")
            
            # Add league_id column
            cursor.execute('ALTER TABLE players ADD COLUMN league_id INTEGER DEFAULT 1')
            
            # Set foreign key relationship (note: SQLite doesn't enforce FK by default)
            print("✅ Added league_id column (defaults to EPL for existing players)")
        else:
            print("✅ league_id column already exists")
        
        # Update any players without league_id (set to EPL as default)
        cursor.execute('UPDATE players SET league_id = 2 WHERE league_id IS NULL OR league_id = 0')
        updated_players = cursor.rowcount
        if updated_players > 0:
            print(f"✅ Updated {updated_players} existing players to EPL league")
        
        conn.commit()
    
    print("=" * 50)
    print("🎉 Multi-League Migration Completed Successfully!")
    print("\nAvailable Leagues:")
    print("1. Formula 1 (F1)")
    print("2. English Premier League (EPL)")
    print("3. UEFA Champions League (UCL)") 
    print("4. National Football League (NFL)")
    print("\nExisting players have been assigned to EPL by default.")
    print("You can now add players from different leagues!")

def show_league_stats():
    """Show statistics for each league"""
    db_path = 'fantasy_players.db'
    
    if not os.path.exists(db_path):
        print("Database does not exist yet.")
        return
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        print("\n📊 League Statistics:")
        print("=" * 50)
        
        cursor.execute('''
            SELECT l.display_name, l.sport_type, COUNT(p.id) as player_count
            FROM leagues l
            LEFT JOIN players p ON l.id = p.league_id
            GROUP BY l.id, l.display_name, l.sport_type
            ORDER BY l.id
        ''')
        
        results = cursor.fetchall()
        for display_name, sport_type, count in results:
            print(f"{display_name:<25} | {sport_type:<20} | {count:>3} players")

if __name__ == "__main__":
    try:
        migrate_to_multi_league()
        show_league_stats()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("Please check the database file and try again.")
