"""
Player model for the fantasy sports app
"""


class Player:
    def __init__(self, name, team, position, scores, is_on_my_team=False):
        self.name = name
        self.team = team
        self.position = position
        self.scores = scores  # List of scores for each game week
        self.final_score = 0.0  # Will be calculated using weighted average
        self.is_on_my_team = is_on_my_team
    
    def __repr__(self):
        team_status = "⭐ MY TEAM" if self.is_on_my_team else "Available"
        return f"Player(name='{self.name}', team='{self.team}', position='{self.position}', final_score={self.final_score:.2f}, status={team_status})"
    
    def to_dict(self):
        """Convert player to dictionary for easy serialization"""
        return {
            'name': self.name,
            'team': self.team,
            'position': self.position,
            'scores': self.scores,
            'final_score': self.final_score,
            'is_on_my_team': self.is_on_my_team
        }
