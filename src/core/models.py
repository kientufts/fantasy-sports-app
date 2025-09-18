"""
Models for the fantasy sports app with multi-league support
"""


class League:
    def __init__(self, id, name, display_name, sport_type, description='', scoring_system='weighted'):
        self.id = id
        self.name = name  # Short name like 'f1', 'epl', 'ucl', 'nfl'
        self.display_name = display_name  # Full display name
        self.sport_type = sport_type
        self.description = description
        self.scoring_system = scoring_system
    
    def get_position_types(self):
        """Return appropriate positions for this league"""
        position_map = {
            'f1': ['Driver', 'Constructor'],
            'epl': ['Forward', 'Midfielder', 'Defender', 'Goalkeeper'],
            'ucl': ['Forward', 'Midfielder', 'Defender', 'Goalkeeper'],
            'nfl': ['Quarterback', 'Running Back', 'Wide Receiver', 'Tight End', 'Defense', 'Kicker']
        }
        return position_map.get(self.name, ['Player'])
    
    def get_typical_teams(self):
        """Return example teams for this league"""
        teams_map = {
            'f1': ['Red Bull Racing', 'Mercedes', 'Ferrari', 'McLaren', 'Alpine', 'Aston Martin', 
                   'Williams', 'AlphaTauri', 'Alfa Romeo', 'Haas'],
            'epl': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Newcastle United', 
                    'Manchester United', 'Tottenham', 'Brighton', 'Aston Villa', 'West Ham'],
            'ucl': ['Real Madrid', 'Manchester City', 'Bayern Munich', 'PSG', 'Liverpool', 
                    'Barcelona', 'Chelsea', 'Inter Milan', 'AC Milan', 'Atletico Madrid'],
            'nfl': ['Kansas City Chiefs', 'Buffalo Bills', 'Cincinnati Bengals', 'Philadelphia Eagles',
                    'San Francisco 49ers', 'Dallas Cowboys', 'Miami Dolphins', 'Baltimore Ravens']
        }
        return teams_map.get(self.name, ['Team A', 'Team B', 'Team C'])
    
    def __repr__(self):
        return f"League(name='{self.name}', display='{self.display_name}', sport='{self.sport_type}')"
    
    def to_dict(self):
        """Convert league to dictionary for easy serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'sport_type': self.sport_type,
            'description': self.description,
            'scoring_system': self.scoring_system,
            'positions': self.get_position_types(),
            'typical_teams': self.get_typical_teams()
        }


class Player:
    def __init__(self, name, team, position, scores, is_on_my_team=False, league_id=1):
        self.name = name
        self.team = team
        self.position = position
        self.scores = scores  # List of scores for each game week
        self.final_score = 0.0  # Will be calculated using weighted average
        self.is_on_my_team = is_on_my_team
        self.league_id = league_id
        self.league = None  # Will be populated by database operations
    
    def __repr__(self):
        team_status = "⭐ MY TEAM" if self.is_on_my_team else "Available"
        league_name = self.league.name.upper() if self.league else f"League{self.league_id}"
        return f"Player(name='{self.name}', team='{self.team}', position='{self.position}', league='{league_name}', final_score={self.final_score:.2f}, status={team_status})"
    
    def to_dict(self):
        """Convert player to dictionary for easy serialization"""
        return {
            'name': self.name,
            'team': self.team,
            'position': self.position,
            'scores': self.scores,
            'final_score': self.final_score,
            'is_on_my_team': self.is_on_my_team,
            'league_id': self.league_id,
            'league': self.league.to_dict() if self.league else None
        }
