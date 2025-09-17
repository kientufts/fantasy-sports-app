"""
Multi-League Fantasy Sports Player Scoring App

A Python application that manages player data across multiple leagues with weighted scoring.
Features:
- Multi-league support (F1, EPL, UCL, NFL)
- Player database with team, position, and game scores per league
- Weighted average calculation prioritizing recent performance
- Sorted leaderboard based on final scores per league
"""

from database import Database
from models import Player, League
from scoring import WeightedScoreCalculator


class MultiLeagueFantasyApp:
    def __init__(self, db_path='fantasy_players.db'):
        self.db = Database(db_path)
        self.calculator = WeightedScoreCalculator()
        self.current_league_id = 2  # Default to EPL
    
    def switch_league(self, league_id):
        """Switch to a different league"""
        league = self.db.get_league_by_id(league_id)
        if league:
            self.current_league_id = league_id
            print(f"Switched to {league.display_name} ({league.sport_type})")
            return True
        else:
            print("League not found!")
            return False
    
    def show_leagues(self):
        """Show all available leagues"""
        leagues = self.db.get_all_leagues()
        print("\n" + "="*60)
        print("AVAILABLE LEAGUES")
        print("="*60)
        
        for league in leagues:
            players = self.db.get_players_by_league(league.id)
            my_team_count = len([p for p in players if p.is_on_my_team])
            current = " (CURRENT)" if league.id == self.current_league_id else ""
            print(f"{league.id}. {league.display_name} - {league.sport_type}{current}")
            print(f"   Players: {len(players)}, My Team: {my_team_count}")
        print()
    
    def get_leaderboard(self, league_id=None):
        """Get all players sorted by their weighted scores for a specific league"""
        if league_id is None:
            league_id = self.current_league_id
            
        players = self.db.get_players_by_league(league_id)
        
        # Calculate weighted scores for all players
        for player in players:
            player.final_score = self.calculator.calculate_weighted_score(player.scores)
        
        # Sort by final score in descending order
        sorted_players = sorted(players, key=lambda p: p.final_score, reverse=True)
        return sorted_players
    
    def display_leaderboard(self, league_id=None):
        """Display the leaderboard in a formatted table"""
        if league_id is None:
            league_id = self.current_league_id
            
        league = self.db.get_league_by_id(league_id)
        leaderboard = self.get_leaderboard(league_id)
        
        print("\n" + "="*90)
        print(f"{league.display_name.upper()} ({league.sport_type.upper()}) LEADERBOARD")
        print("="*90)
        print(f"{'Rank':<4} {'Player':<20} {'Team':<15} {'Position':<12} {'Score':<8} {'Status':<10}")
        print("-"*90)
        
        for i, player in enumerate(leaderboard, 1):
            status = "⭐ MY TEAM" if player.is_on_my_team else "Available"
            print(f"{i:<4} {player.name:<20} {player.team:<15} {player.position:<12} {player.final_score:<8.2f} {status:<10}")
    
    def add_player(self, name, team, position, scores, is_on_my_team=False, league_id=None):
        """Add a new player to the database in the current league"""
        if league_id is None:
            league_id = self.current_league_id
            
        player = Player(name, team, position, scores, is_on_my_team, league_id)
        self.db.add_player(player)
        
        league = self.db.get_league_by_id(league_id)
        team_status = "and added to your team" if is_on_my_team else ""
        print(f"Player {name} added to {league.display_name} successfully! {team_status}")
    
    def update_player_scores(self, player_name, new_scores):
        """Update a player's scores in the current league"""
        if self.db.update_player_scores(player_name, new_scores):
            print(f"Scores updated for {player_name}")
        else:
            print(f"Player {player_name} not found in current league")
    
    def show_my_team(self, league_id=None):
        """Show players on my team for a specific league"""
        if league_id is None:
            league_id = self.current_league_id
            
        league = self.db.get_league_by_id(league_id)
        players = self.db.get_players_by_league(league_id)
        my_team = [p for p in players if p.is_on_my_team]
        
        if not my_team:
            print(f"\nYou don't have any players in {league.display_name} yet!")
            return
        
        # Calculate scores
        for player in my_team:
            player.final_score = self.calculator.calculate_weighted_score(player.scores)
        
        my_team.sort(key=lambda p: p.final_score, reverse=True)
        
        print(f"\n⭐ MY {league.display_name.upper()} TEAM")
        print("="*60)
        total_score = sum(p.final_score for p in my_team)
        
        for player in my_team:
            print(f"{player.name:<20} {player.team:<15} {player.position:<12} {player.final_score:.2f}")
        
        print("-"*60)
        print(f"TEAM AVERAGE: {total_score/len(my_team):.2f}")
        print(f"TOTAL PLAYERS: {len(my_team)}")


def interactive_menu():
    """Interactive command-line interface"""
    app = MultiLeagueFantasyApp()
    
    while True:
        print("\n" + "="*50)
        print("MULTI-LEAGUE FANTASY SPORTS MANAGER")
        print("="*50)
        print("1. Show Available Leagues")
        print("2. Switch League")
        print("3. Show Current League Leaderboard")
        print("4. Show My Team (Current League)")
        print("5. Show My Team (All Leagues)")
        print("6. Add Player to Current League")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            app.show_leagues()
            
        elif choice == '2':
            app.show_leagues()
            try:
                league_id = int(input("Enter league ID: "))
                app.switch_league(league_id)
            except ValueError:
                print("Invalid league ID!")
                
        elif choice == '3':
            app.display_leaderboard()
            
        elif choice == '4':
            app.show_my_team()
            
        elif choice == '5':
            leagues = app.db.get_all_leagues()
            for league in leagues:
                app.show_my_team(league.id)
                
        elif choice == '6':
            league = app.db.get_league_by_id(app.current_league_id)
            print(f"\nAdding player to {league.display_name}")
            
            name = input("Player name: ").strip()
            if not name:
                print("Player name is required!")
                continue
                
            print(f"\nAvailable teams in {league.display_name}:")
            teams = league.get_typical_teams()
            for i, team in enumerate(teams, 1):
                print(f"{i}. {team}")
            
            try:
                team_idx = int(input("Select team number: ")) - 1
                team = teams[team_idx]
            except (ValueError, IndexError):
                print("Invalid team selection!")
                continue
            
            print(f"\nAvailable positions in {league.display_name}:")
            positions = league.get_position_types()
            for i, pos in enumerate(positions, 1):
                print(f"{i}. {pos}")
            
            try:
                pos_idx = int(input("Select position number: ")) - 1
                position = positions[pos_idx]
            except (ValueError, IndexError):
                print("Invalid position selection!")
                continue
            
            scores_input = input("Enter scores (comma-separated, e.g., 85,92,78,88,95): ").strip()
            try:
                scores = [int(x.strip()) for x in scores_input.split(',')]
                if len(scores) < 1:
                    raise ValueError("At least one score is required")
            except ValueError:
                print("Invalid scores format!")
                continue
            
            add_to_team = input("Add to your team? (y/n): ").strip().lower() == 'y'
            
            app.add_player(name, team, position, scores, add_to_team)
            
        elif choice == '7':
            print("Thanks for using Multi-League Fantasy Sports Manager!")
            break
            
        else:
            print("Invalid choice! Please enter 1-7.")


def main():
    """Main function - can be used for basic testing or interactive mode"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_menu()
    else:
        # Basic demo
        app = MultiLeagueFantasyApp()
        
        # Show all leagues
        app.show_leagues()
        
        # Show EPL leaderboard (default)
        app.display_leaderboard()
        
        # Switch to F1 and show leaderboard
        app.switch_league(1)
        app.display_leaderboard()


if __name__ == "__main__":
    main()
