import json


class GameStats:
    """Track statistics for Alien Invasion"""

    HIGH_SCORE_FILE = 'high_score.json'

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never reset — load it from disk instead
        self.high_score = self._load_high_score()


    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.hearts_left = self.settings.heart_limit
        self.score = 0
        self.level = 1


    def _load_high_score(self):
        """Read the saved high score from disk, or default to 0 if none exists."""
        try:
            with open(self.HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0


    def save_high_score(self):
        """Write the current high score to disk."""
        with open(self.HIGH_SCORE_FILE, 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def reset_high_score(self):
        """Reset the high score back to zero and save that."""
        self.high_score = 0
        self.save_high_score()