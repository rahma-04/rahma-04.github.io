import pygame
from pygame.sprite import Sprite

class Frog(Sprite):
    """A class to manage the frog."""

    def __init__(self, ai_game):
        """Initialize the frog and set its starting positions."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the frog image and get its rect.
        self.image = pygame.image.load('images/frog.bmp')
        self.rect = self.image.get_rect()

        #Start each new frog at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the frog's horizontal position
        self.x = float(self.rect.x)

        #Movement flag
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Update the frog's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.frog_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.frog_speed
        
        self.rect.x = self.x

    def blitme(self):
        """Draw the frog at its current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_frog(self):
        """Center the frog on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)