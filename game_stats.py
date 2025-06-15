#GAME_STATS.PY
import os

class GameStats:
    
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        
        self.game_active = False
        
        self.high_score_file = 'highscore.txt'
        self.high_score = self.load_high_score()
        
        print(f"Initialized GameStats. High score: {self.high_score}")

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:
            if os.path.exists(self.high_score_file) and os.access(self.high_score_file, os.R_OK):
                with open(self.high_score_file, 'r') as f:
                    content = f.read().strip()
                    if content.isdigit():
                        high_score = int(content)
                        print(f"Successfully loaded high score: {high_score}")
                        return high_score
                    
            print("No valid high score found, defaulting to 0")
            return 0
            
        except Exception as e:
            print(f"Error loading high score: {e}")
            return 0

    def save_high_score(self):
        try:
            with open(self.high_score_file, 'w') as f:
                f.write(str(self.high_score))
            print(f"Saved high score: {self.high_score}")
            
        except Exception as e:
            print(f"Failed to save high score: {e}")

    def reset_high_score(self):
        self.high_score = 0
        self.save_high_score()
        print("High score reset to 0")
        return True