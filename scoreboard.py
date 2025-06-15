#SCOREBOARD.PY
import pygame.font
from pygame.sprite import Group

class Scoreboard:
    
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        self.text_color = (255, 255, 255)  
        self.font = pygame.font.SysFont(None, 36)
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        
        self.reset_button = pygame.Rect(0, 0, 90, 30)  
        self.reset_button.midright = (self.high_score_rect.left - 30, self.high_score_rect.centery)
        self.reset_button.top = 5
        self.reset_button_color = (0, 0, 139)  

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_str = "Level: {}".format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def draw_reset_button(self):
        mouse_pos = pygame.mouse.get_pos()
        button_color = (0, 0, 0) if self.reset_button.collidepoint(mouse_pos) else self.reset_button_color
        pygame.draw.rect(self.screen, button_color, self.reset_button)
        
        reset_text = self.font.render("RESET", True, self.text_color)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.draw_reset_button()