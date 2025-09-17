"""
Fantasy Sports Player Scoring App

A Python application that manages player data with weighted scoring based on game weeks.
Features:
- Player database with team, position, and game scores
- Weighted average calculation prioritizing recent performance
- Sorted leaderboard based on final scores
"""

from database import Database
from models import Player
from scoring import WeightedScoreCalculator


class FantasyApp:
    def __init__(self, db_path='fantasy_players.db'):
        self.db = Database(db_path)
        self.calculator = WeightedScoreCalculator()
    
    def initialize_sample_data(self):
        """Initialize the database with sample player data"""
        sample_players = [
            # Sample data - replace with actual player data
            ("John Smith", "Team A", "Forward", [85, 92, 78, 88, 95]),
            ("Sarah Johnson", "Team B", "Midfielder", [75, 83, 90, 87, 82]),
            ("Mike Davis", "Team A", "Defender", [65, 70, 75, 80, 85]),
            ("Emily Wilson", "Team C", "Forward", [95, 88, 92, 85, 90]),
            ("Chris Brown", "Team B", "Goalkeeper", [70, 75, 80, 78, 82]),
        ]
        
        for name, team, position, scores in sample_players:
            player = Player(name, team, position, scores)
            self.db.add_player(player)
    
    def get_leaderboard(self):
        """Get all players sorted by their weighted scores"""
        players = self.db.get_all_players()
        
        # Calculate weighted scores for all players
        for player in players:
            player.final_score = self.calculator.calculate_weighted_score(player.scores)
        
        # Sort by final score in descending order
        sorted_players = sorted(players, key=lambda p: p.final_score, reverse=True)
        return sorted_players
    
    def display_leaderboard(self):
        """Display the leaderboard in a formatted table"""
        leaderboard = self.get_leaderboard()
        
        print("\n" + "="*80)
        print("FANTASY SPORTS LEADERBOARD")
        print("="*80)
        print(f"{'Rank':<4} {'Player':<20} {'Team':<10} {'Position':<12} {'Final Score':<12}")
        print("-"*80)
        
        for i, player in enumerate(leaderboard, 1):
            print(f"{i:<4} {player.name:<20} {player.team:<10} {player.position:<12} {player.final_score:.2f}")
    
    def add_player(self, name, team, position, scores):
        """Add a new player to the database"""
        player = Player(name, team, position, scores)
        self.db.add_player(player)
        print(f"Player {name} added successfully!")
    
    def update_player_scores(self, player_name, new_scores):
        """Update a player's scores"""
        if self.db.update_player_scores(player_name, new_scores):
            print(f"Scores updated for {player_name}")
        else:
            print(f"Player {player_name} not found")


def main():
    app = FantasyApp()
    
    # Initialize with sample data (remove this in production)
    app.initialize_sample_data()
    
    # Display the current leaderboard
    app.display_leaderboard()
    
    # Example of adding a new player
    app.add_player("Alex Thompson", "Team C", "Midfielder", [88, 85, 90, 92, 87])
    
    # Display updated leaderboard
    app.display_leaderboard()


if __name__ == "__main__":
    main()
