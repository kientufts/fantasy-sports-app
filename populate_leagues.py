"""
Sample data generator for multi-league fantasy sports app
Creates realistic sample players for F1, EPL, UCL, and NFL leagues
"""

from database import Database
from models import Player
import random

def generate_sample_scores(num_weeks=5, base_range=(70, 95)):
    """Generate realistic sample scores with some variance"""
    scores = []
    for _ in range(num_weeks):
        score = random.randint(base_range[0], base_range[1])
        scores.append(score)
    return scores

def create_f1_players(db):
    """Create Formula 1 sample players"""
    print("🏎️  Creating Formula 1 players...")
    
    f1_drivers = [
        ("Max Verstappen", "Red Bull Racing", "Driver"),
        ("Sergio Pérez", "Red Bull Racing", "Driver"), 
        ("Lewis Hamilton", "Mercedes", "Driver"),
        ("George Russell", "Mercedes", "Driver"),
        ("Charles Leclerc", "Ferrari", "Driver"),
        ("Carlos Sainz", "Ferrari", "Driver"),
        ("Lando Norris", "McLaren", "Driver"),
        ("Oscar Piastri", "McLaren", "Driver"),
        ("Fernando Alonso", "Aston Martin", "Driver"),
        ("Lance Stroll", "Aston Martin", "Driver"),
        ("Pierre Gasly", "Alpine", "Driver"),
        ("Esteban Ocon", "Alpine", "Driver")
    ]
    
    # Add some constructors as well
    f1_constructors = [
        ("Red Bull Racing", "Red Bull Racing", "Constructor"),
        ("Mercedes AMG F1", "Mercedes", "Constructor"),
        ("Scuderia Ferrari", "Ferrari", "Constructor"),
        ("McLaren F1", "McLaren", "Constructor")
    ]
    
    f1_league = db.get_league_by_name('f1')
    
    for name, team, position in f1_drivers:
        scores = generate_sample_scores(5, (75, 100))  # Higher range for top drivers
        if name in ["Max Verstappen", "Lewis Hamilton", "Charles Leclerc"]:
            scores = generate_sample_scores(5, (85, 100))  # Elite drivers
        
        player = Player(name, team, position, scores, False, f1_league.id)
        db.add_player(player)
    
    for name, team, position in f1_constructors:
        scores = generate_sample_scores(5, (80, 95))
        player = Player(name, team, position, scores, False, f1_league.id)
        db.add_player(player)

def create_epl_players(db):
    """Create English Premier League sample players"""
    print("⚽ Creating English Premier League players...")
    
    epl_players = [
        ("Erling Haaland", "Manchester City", "Forward"),
        ("Kevin De Bruyne", "Manchester City", "Midfielder"),
        ("Phil Foden", "Manchester City", "Midfielder"),
        ("Bukayo Saka", "Arsenal", "Forward"),
        ("Martin Ødegaard", "Arsenal", "Midfielder"),
        ("Gabriel Jesus", "Arsenal", "Forward"),
        ("Mohamed Salah", "Liverpool", "Forward"),
        ("Virgil van Dijk", "Liverpool", "Defender"),
        ("Sadio Mané", "Liverpool", "Forward"),
        ("Bruno Fernandes", "Manchester United", "Midfielder"),
        ("Marcus Rashford", "Manchester United", "Forward"),
        ("Harry Kane", "Tottenham", "Forward"),
        ("Son Heung-min", "Tottenham", "Forward"),
        ("Reece James", "Chelsea", "Defender"),
        ("Mason Mount", "Chelsea", "Midfielder"),
        ("Alisson Becker", "Liverpool", "Goalkeeper"),
        ("Ederson", "Manchester City", "Goalkeeper"),
        ("Aaron Ramsdale", "Arsenal", "Goalkeeper")
    ]
    
    epl_league = db.get_league_by_name('epl')
    
    for name, team, position in epl_players:
        # Adjust scoring based on position and player quality
        if position == "Forward" and name in ["Erling Haaland", "Mohamed Salah", "Harry Kane"]:
            scores = generate_sample_scores(5, (85, 98))  # Elite forwards
        elif position == "Midfielder" and name in ["Kevin De Bruyne", "Bruno Fernandes"]:
            scores = generate_sample_scores(5, (82, 95))  # Elite midfielders
        elif position == "Defender":
            scores = generate_sample_scores(5, (70, 88))  # Defenders generally score lower
        elif position == "Goalkeeper":
            scores = generate_sample_scores(5, (75, 92))  # Goalkeepers
        else:
            scores = generate_sample_scores(5, (75, 90))  # Regular players
        
        player = Player(name, team, position, scores, False, epl_league.id)
        db.add_player(player)

def create_ucl_players(db):
    """Create UEFA Champions League sample players"""
    print("🏆 Creating UEFA Champions League players...")
    
    ucl_players = [
        ("Kylian Mbappé", "PSG", "Forward"),
        ("Lionel Messi", "PSG", "Forward"),
        ("Neymar Jr", "PSG", "Forward"),
        ("Karim Benzema", "Real Madrid", "Forward"),
        ("Vinícius Jr.", "Real Madrid", "Forward"),
        ("Luka Modrić", "Real Madrid", "Midfielder"),
        ("Robert Lewandowski", "Barcelona", "Forward"),
        ("Pedri", "Barcelona", "Midfielder"),
        ("Gavi", "Barcelona", "Midfielder"),
        ("Jamal Musiala", "Bayern Munich", "Midfielder"),
        ("Sadio Mané", "Bayern Munich", "Forward"),
        ("Thomas Müller", "Bayern Munich", "Midfielder"),
        ("Erling Haaland", "Manchester City", "Forward"),
        ("Jack Grealish", "Manchester City", "Midfielder"),
        ("Rafael Leão", "AC Milan", "Forward"),
        ("Theo Hernández", "AC Milan", "Defender")
    ]
    
    ucl_league = db.get_league_by_name('ucl')
    
    for name, team, position in ucl_players:
        # UCL players tend to have higher scores due to elite competition
        if name in ["Kylian Mbappé", "Lionel Messi", "Karim Benzema", "Robert Lewandowski"]:
            scores = generate_sample_scores(5, (88, 100))  # Superstar players
        elif position == "Forward":
            scores = generate_sample_scores(5, (80, 95))
        elif position == "Midfielder":
            scores = generate_sample_scores(5, (75, 92))
        else:
            scores = generate_sample_scores(5, (72, 88))
        
        player = Player(name, team, position, scores, False, ucl_league.id)
        db.add_player(player)

def create_nfl_players(db):
    """Create National Football League sample players"""
    print("🏈 Creating NFL players...")
    
    nfl_players = [
        ("Josh Allen", "Buffalo Bills", "Quarterback"),
        ("Patrick Mahomes", "Kansas City Chiefs", "Quarterback"),
        ("Joe Burrow", "Cincinnati Bengals", "Quarterback"),
        ("Lamar Jackson", "Baltimore Ravens", "Quarterback"),
        ("Jonathan Taylor", "Indianapolis Colts", "Running Back"),
        ("Derrick Henry", "Tennessee Titans", "Running Back"),
        ("Austin Ekeler", "Los Angeles Chargers", "Running Back"),
        ("Cooper Kupp", "Los Angeles Rams", "Wide Receiver"),
        ("Davante Adams", "Las Vegas Raiders", "Wide Receiver"),
        ("Tyreek Hill", "Miami Dolphins", "Wide Receiver"),
        ("Stefon Diggs", "Buffalo Bills", "Wide Receiver"),
        ("Travis Kelce", "Kansas City Chiefs", "Tight End"),
        ("Mark Andrews", "Baltimore Ravens", "Tight End"),
        ("George Kittle", "San Francisco 49ers", "Tight End"),
        ("Pittsburgh Steelers", "Pittsburgh Steelers", "Defense"),
        ("New England Patriots", "New England Patriots", "Defense"),
        ("Justin Tucker", "Baltimore Ravens", "Kicker"),
        ("Harrison Butker", "Kansas City Chiefs", "Kicker")
    ]
    
    nfl_league = db.get_league_by_name('nfl')
    
    for name, team, position in nfl_players:
        # NFL scoring varies significantly by position
        if position == "Quarterback" and name in ["Josh Allen", "Patrick Mahomes"]:
            scores = generate_sample_scores(5, (85, 100))  # Elite QBs
        elif position == "Quarterback":
            scores = generate_sample_scores(5, (78, 95))
        elif position == "Running Back":
            scores = generate_sample_scores(5, (70, 92))
        elif position == "Wide Receiver" and name in ["Cooper Kupp", "Davante Adams"]:
            scores = generate_sample_scores(5, (82, 98))  # Elite WRs
        elif position == "Wide Receiver":
            scores = generate_sample_scores(5, (75, 90))
        elif position == "Tight End":
            scores = generate_sample_scores(5, (65, 85))
        elif position == "Defense":
            scores = generate_sample_scores(5, (60, 85))
        elif position == "Kicker":
            scores = generate_sample_scores(5, (70, 88))
        else:
            scores = generate_sample_scores(5, (70, 85))
        
        player = Player(name, team, position, scores, False, nfl_league.id)
        db.add_player(player)

def populate_all_leagues():
    """Populate all leagues with sample players"""
    db = Database()
    
    print("🏆 Populating Multi-League Fantasy Database")
    print("=" * 50)
    
    # Check if any league already has players
    f1_players = db.get_players_by_league(1)  # F1
    epl_players = db.get_players_by_league(2)  # EPL  
    ucl_players = db.get_players_by_league(3)  # UCL
    nfl_players = db.get_players_by_league(4)  # NFL
    
    if len(f1_players) == 0:
        create_f1_players(db)
    else:
        print("🏎️  Formula 1 players already exist, skipping...")
    
    if len(epl_players) == 0:
        create_epl_players(db)
    else:
        print("⚽ EPL players already exist, skipping...")
    
    if len(ucl_players) == 0:
        create_ucl_players(db)
    else:
        print("🏆 UCL players already exist, skipping...")
    
    if len(nfl_players) == 0:
        create_nfl_players(db)
    else:
        print("🏈 NFL players already exist, skipping...")
    
    print("=" * 50)
    print("✅ Multi-League Sample Data Creation Complete!")
    
    # Show final statistics
    print("\n📊 Final League Statistics:")
    leagues = db.get_all_leagues()
    for league in leagues:
        players = db.get_players_by_league(league.id)
        print(f"{league.display_name:<25} | {len(players):>3} players")

if __name__ == "__main__":
    try:
        populate_all_leagues()
    except Exception as e:
        print(f"❌ Error populating leagues: {e}")
