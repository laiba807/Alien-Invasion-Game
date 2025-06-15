import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.images = []
        
        # Load explosion images (you'll need to create these or find assets)
        for i in range(1, 6):  # Assuming you have 5 explosion frames
            filename = f'images/explosion{i}.bmp'
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (size, size))
            self.images.append(image)
            
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame_rate = 50  # milliseconds between frames
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = center