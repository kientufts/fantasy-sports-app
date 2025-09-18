"""
Weighted scoring calculator for fantasy sports players

Implements the weighted average formula:
(score_week1 * 1 + score_week2 * 2 + ... + score_weekN * N) / (1 + 2 + ... + N)

This prioritizes more recent game weeks in the final score calculation.
"""


class WeightedScoreCalculator:
    def __init__(self):
        pass
    
    def calculate_weighted_score(self, scores):
        """
        Calculate weighted average score for a player
        
        Args:
            scores (list): List of scores for each game week
            
        Returns:
            float: Weighted average score
        """
        if not scores:
            return 0.0
        
        n = len(scores)
        
        # Calculate weighted sum: score1*1 + score2*2 + ... + scoreN*N
        weighted_sum = sum(score * (i + 1) for i, score in enumerate(scores))
        
        # Calculate sum of weights: 1 + 2 + ... + N
        weight_sum = sum(range(1, n + 1))
        
        # Return weighted average
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def calculate_weighted_score_detailed(self, scores):
        """
        Calculate weighted average score with detailed breakdown
        
        Args:
            scores (list): List of scores for each game week
            
        Returns:
            dict: Dictionary containing detailed calculation breakdown
        """
        if not scores:
            return {
                'final_score': 0.0,
                'breakdown': [],
                'weighted_sum': 0.0,
                'weight_sum': 0
            }
        
        n = len(scores)
        breakdown = []
        weighted_sum = 0
        
        for i, score in enumerate(scores):
            weight = i + 1
            weighted_value = score * weight
            weighted_sum += weighted_value
            
            breakdown.append({
                'week': i + 1,
                'score': score,
                'weight': weight,
                'weighted_value': weighted_value
            })
        
        weight_sum = sum(range(1, n + 1))
        final_score = weighted_sum / weight_sum if weight_sum > 0 else 0.0
        
        return {
            'final_score': final_score,
            'breakdown': breakdown,
            'weighted_sum': weighted_sum,
            'weight_sum': weight_sum
        }
