"""
Database operations for the fantasy sports app
Uses SQLite for local storage of player data
"""

import sqlite3
import json
from models import Player


class Database:
    def __init__(self, db_path='fantasy_players.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the players table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    team TEXT NOT NULL,
                    position TEXT NOT NULL,
                    scores TEXT NOT NULL,
                    final_score REAL DEFAULT 0.0
                )
            ''')
            conn.commit()
    
    def add_player(self, player):
        """Add a new player to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            scores_json = json.dumps(player.scores)
            
            try:
                cursor.execute('''
                    INSERT INTO players (name, team, position, scores, final_score)
                    VALUES (?, ?, ?, ?, ?)
                ''', (player.name, player.team, player.position, scores_json, player.final_score))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print(f"Player {player.name} already exists!")
                return False
    
    def get_all_players(self):
        """Retrieve all players from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, team, position, scores FROM players')
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores)
                players.append(player)
            
            return players
    
    def get_player_by_name(self, name):
        """Get a specific player by name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, team, position, scores FROM players WHERE name = ?', (name,))
            row = cursor.fetchone()
            
            if row:
                name, team, position, scores_json = row
                scores = json.loads(scores_json)
                return Player(name, team, position, scores)
            return None
    
    def update_player_scores(self, name, new_scores):
        """Update a player's scores"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            scores_json = json.dumps(new_scores)
            
            cursor.execute('''
                UPDATE players 
                SET scores = ? 
                WHERE name = ?
            ''', (scores_json, name))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def update_player_info(self, original_name, new_name, new_team, new_position, new_scores):
        """Update all player information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            scores_json = json.dumps(new_scores)
            
            cursor.execute('''
                UPDATE players 
                SET name = ?, team = ?, position = ?, scores = ?
                WHERE name = ?
            ''', (new_name, new_team, new_position, scores_json, original_name))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_player(self, name):
        """Delete a player from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM players WHERE name = ?', (name,))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_all_players(self):
        """Delete all players from the database (use with caution!)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM players')
            conn.commit()
            return cursor.rowcount
    
    def get_players_by_team(self, team):
        """Get all players from a specific team"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, team, position, scores FROM players WHERE team = ?', (team,))
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores)
                players.append(player)
            
            return players
    
    def get_players_by_position(self, position):
        """Get all players from a specific position"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, team, position, scores FROM players WHERE position = ?', (position,))
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores)
                players.append(player)
            
            return players
