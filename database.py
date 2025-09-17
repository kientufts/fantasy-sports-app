"""
Database operations for the fantasy sports app
Uses SQLite for local storage of player data with multi-league support
"""

import sqlite3
import json
from models import Player, League


class Database:
    def __init__(self, db_path='fantasy_players.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with the players and leagues tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create leagues table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leagues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL,
                    sport_type TEXT NOT NULL,
                    description TEXT,
                    scoring_system TEXT DEFAULT 'weighted',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create players table with league_id
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    team TEXT NOT NULL,
                    position TEXT NOT NULL,
                    scores TEXT NOT NULL,
                    final_score REAL DEFAULT 0.0,
                    is_on_my_team BOOLEAN DEFAULT 0,
                    league_id INTEGER DEFAULT 1,
                    UNIQUE(name, league_id)
                )
            ''')
            
            # Initialize default leagues if empty
            cursor.execute('SELECT COUNT(*) FROM leagues')
            if cursor.fetchone()[0] == 0:
                leagues_data = [
                    ('f1', 'Formula 1', 'Motorsport', 'Formula 1 Championship racing', 'weighted'),
                    ('epl', 'English Premier League', 'Football', 'English Premier League football/soccer', 'weighted'),
                    ('ucl', 'UEFA Champions League', 'Football', 'UEFA Champions League European football', 'weighted'),
                    ('nfl', 'National Football League', 'American Football', 'NFL American Football league', 'weighted')
                ]
                cursor.executemany('''
                    INSERT INTO leagues (name, display_name, sport_type, description, scoring_system)
                    VALUES (?, ?, ?, ?, ?)
                ''', leagues_data)
            
            conn.commit()
    
    # League Operations
    def get_all_leagues(self):
        """Get all available leagues"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, display_name, sport_type, description, scoring_system FROM leagues ORDER BY id')
            rows = cursor.fetchall()
            
            leagues = []
            for row in rows:
                league = League(row[0], row[1], row[2], row[3], row[4], row[5])
                leagues.append(league)
            
            return leagues
    
    def get_league_by_id(self, league_id):
        """Get a specific league by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, display_name, sport_type, description, scoring_system FROM leagues WHERE id = ?', (league_id,))
            row = cursor.fetchone()
            
            if row:
                return League(row[0], row[1], row[2], row[3], row[4], row[5])
            return None
    
    def get_league_by_name(self, name):
        """Get a specific league by name"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, display_name, sport_type, description, scoring_system FROM leagues WHERE name = ?', (name,))
            row = cursor.fetchone()
            
            if row:
                return League(row[0], row[1], row[2], row[3], row[4], row[5])
            return None
    
    def add_player(self, player):
        """Add a new player to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            scores_json = json.dumps(player.scores)
            
            try:
                cursor.execute('''
                    INSERT INTO players (name, team, position, scores, final_score, is_on_my_team, league_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (player.name, player.team, player.position, scores_json, player.final_score, player.is_on_my_team, player.league_id))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print(f"Player {player.name} already exists in this league!")
                return False
    
    def get_all_players(self, league_id=None):
        """Retrieve all players from the database, optionally filtered by league"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if league_id:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE league_id = ?', (league_id,))
            else:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players')
                
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json, is_on_my_team, player_league_id = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores, bool(is_on_my_team), player_league_id)
                
                # Populate league information
                player.league = self.get_league_by_id(player_league_id)
                players.append(player)
            
            return players
    
    def get_players_by_league(self, league_id):
        """Get all players in a specific league"""
        return self.get_all_players(league_id)
    
    def get_player_by_name(self, name, league_id=None):
        """Get a specific player by name, optionally within a specific league"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if league_id:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE name = ? AND league_id = ?', (name, league_id))
            else:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE name = ?', (name,))
                
            row = cursor.fetchone()
            
            if row:
                name, team, position, scores_json, is_on_my_team, player_league_id = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores, bool(is_on_my_team), player_league_id)
                
                # Populate league information
                player.league = self.get_league_by_id(player_league_id)
                return player
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
    
    def toggle_my_team_status(self, name):
        """Toggle whether a player is on my team or not"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get current status
            cursor.execute('SELECT is_on_my_team FROM players WHERE name = ?', (name,))
            row = cursor.fetchone()
            if not row:
                return False
            
            current_status = bool(row[0])
            new_status = not current_status
            
            # Update status
            cursor.execute('''
                UPDATE players 
                SET is_on_my_team = ?
                WHERE name = ?
            ''', (new_status, name))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_my_team_players(self, league_id=None):
        """Get all players currently on my team, optionally filtered by league"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if league_id:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE is_on_my_team = 1 AND league_id = ?', (league_id,))
            else:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE is_on_my_team = 1')
            
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json, is_on_my_team, player_league_id = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores, bool(is_on_my_team), player_league_id)
                player.league = self.get_league_by_id(player_league_id)
                players.append(player)
            
            return players
    
    def get_available_players(self, league_id=None):
        """Get all players not currently on my team, optionally filtered by league"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if league_id:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE is_on_my_team = 0 AND league_id = ?', (league_id,))
            else:
                cursor.execute('SELECT name, team, position, scores, is_on_my_team, league_id FROM players WHERE is_on_my_team = 0')
            
            rows = cursor.fetchall()
            
            players = []
            for row in rows:
                name, team, position, scores_json, is_on_my_team, player_league_id = row
                scores = json.loads(scores_json)
                player = Player(name, team, position, scores, bool(is_on_my_team), player_league_id)
                player.league = self.get_league_by_id(player_league_id)
                players.append(player)
            
            return players
    
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
