import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):
    """A class to represent a single zombie in the fleet."""

    def __init__(self, ai_game):
        """Initialize the zombie and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load the zombie image and set its recct attribute
        self.image = pygame.image.load('images/zombie.bmp')
        self.rect = self.image.get_rect()

        #Start each new zombie near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the zombie's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if zombie is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        """Move the zombie right of left"""
        self.x += (self.settings.zombie_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        