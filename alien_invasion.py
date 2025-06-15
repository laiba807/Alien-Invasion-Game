#ALIEN_INVASION.PY
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
import game_functions as gf
from game_stats import GameStats  
from button import Button  
from scoreboard import Scoreboard  

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self.settings)
        
        self.ship = Ship(self)
        
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        gf.create_fleet(self.settings, self.screen, self.ship, self.aliens)

        self.play_button = Button(self.settings, self.screen, "Play")

        self.sb = Scoreboard(self.settings, self.screen, self.stats)

    def run_game(self):
        while True:
            gf.check_events(self.settings, self.screen, self.stats, self.play_button, self.ship, self.bullets, self.aliens, self.sb)

            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self.settings, self.screen, self.ship, self.aliens, self.bullets, self.stats, self.sb)
                gf.update_aliens(self.settings, self.stats, self.screen, self.ship, self.aliens, self.bullets, self.sb)
                self._check_game_over()

            self._update_screen()

    def _update_screen(self):
      
        self.screen.fill(self.settings.bg_color)
        
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.display_ships()

        self.sb.show_score()

        if not self.stats.game_active:
            if self.stats.ships_left <= 0:
                self._display_game_over()  
            else:
                self.play_button.draw_button()  

        pygame.display.flip()

    def display_ships(self):
        font = pygame.font.SysFont(None, 48)
        ships_left_image = font.render(f'Ships Left: {self.stats.ships_left}', True, (255, 255, 255))
        self.screen.blit(ships_left_image, (10, 10))

    def _display_game_over(self):
        
        font = pygame.font.SysFont("Arial", 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        restart_font = pygame.font.SysFont("Arial", 36)
        restart_text = restart_font.render("Press R to Restart", True, (0, 0, 255))
        restart_rect = restart_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 20))
        self.screen.blit(restart_text, restart_rect)

    def _check_game_over(self):
        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
                                 
                                 