"""
Player model for the fantasy sports app
"""


class Player:
    def __init__(self, name, team, position, scores):
        self.name = name
        self.team = team
        self.position = position
        self.scores = scores  # List of scores for each game week
        self.final_score = 0.0  # Will be calculated using weighted average
    
    def __repr__(self):
        return f"Player(name='{self.name}', team='{self.team}', position='{self.position}', final_score={self.final_score:.2f})"
    
    def to_dict(self):
        """Convert player to dictionary for easy serialization"""
        return {
            'name': self.name,
            'team': self.team,
            'position': self.position,
            'scores': self.scores,
            'final_score': self.final_score
        }
