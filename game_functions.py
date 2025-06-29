#GAME_FUNCTIONS.PY
import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def create_explosion(screen, position, size=100):
    try:
        original_img = pygame.image.load('E:\Office\Alien_Invasion\game\images\explosion.bmp').convert_alpha()
        
        explosion_images = []
        for i in range(5):
            scale = 0.5 + (i * 0.15)  
            width = int(original_img.get_width() * scale)
            height = int(original_img.get_height() * scale)
            img = pygame.transform.scale(original_img, (width, height))
            explosion_images.append(img)
            
    except:
        explosion_images = []
        for i in range(5):
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            color = (255, 200 - i*30, 0, 200 - i*40)
            pygame.draw.circle(surf, color, (size//2, size//2), (i + 1) * (size // 10))
            explosion_images.append(surf)
    
    return {
        'images': explosion_images,
        'position': position,
        'frame': 0,
        'last_update': pygame.time.get_ticks()
    }
    
    
def check_events(ai_settings, screen, stats, play_button, ship, bullets, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            check_play_button(stats, play_button, mouse_x, mouse_y, 
                            ai_settings, screen, ship, aliens, bullets, sb)
            
            check_reset_button(stats, sb, mouse_x, mouse_y)
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, 
                               ship, bullets, aliens, sb)
                               
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_reset_button(stats, sb, mouse_x, mouse_y):
   
    if sb.reset_button.collidepoint(mouse_x, mouse_y):
        stats.reset_high_score()
        
        sb.prep_high_score()
        
        print("High score reset to 0")

def check_keydown_events(event, ai_settings, screen, stats, ship, bullets, aliens, sb):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_new_game(ai_settings, screen, stats, ship, aliens, bullets, sb)
    elif event.key == pygame.K_r and not stats.game_active:
        start_new_game(ai_settings, screen, stats, ship, aliens, bullets, sb)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_new_game(ai_settings, screen, stats, ship, aliens, bullets, sb)

def start_new_game(ai_settings, screen, stats, ship, aliens, bullets, sb):
    stats.reset_stats()
    stats.game_active = True

    sb.prep_score()
    sb.prep_level()
    sb.prep_high_score()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    pygame.mouse.set_visible(False)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb):

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
            sb.prep_score()
            check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        stats.save_high_score()
        sb.prep_high_score()

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        
       
        explosion = create_explosion(screen, ship.rect.center, 150)  
        
       
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 500:
            current_frame = min((pygame.time.get_ticks() - start_time) // 100, 4)
            img = explosion['images'][current_frame]
            img_rect = img.get_rect(center=explosion['position'])
            screen.blit(img, img_rect)
            pygame.display.flip()
        
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def create_fleet(ai_settings, screen, ship, aliens):

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()
        font = pygame.font.SysFont(None, 48)
        text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(text, (ai_settings.screen_width / 2 - text.get_width() / 2, 
                          ai_settings.screen_height / 2 + 100))

    pygame.display.flip()