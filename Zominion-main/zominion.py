import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from frog import Frog
from bullet import Bullet
from zombie import Zombie

class Zominion:
    """Overall class to manage game assets and behaviour."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        #fullscreen mode
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        """a spesific screen size for the game"""
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Zominion by Rahma")

        #Create an instance to store game statistics.
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.frog = Frog(self)
        self.bullets = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "PLAY GAME")


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.frog.update()
                self.bullets.update()
                self._update_bullets()
                self._update_zombies()
            
            self._update_screen()
    
    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game statitics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_frogs()

            #Get rid of any remaining zombies and bullets.
            self.zombies.empty()
            self.bullets.empty()

            #Create a new fleet and center the frog.
            self._create_fleet()
            self.frog.center_frog()

            #Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.frog.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.frog.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.frog.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.frog.moving_left = False;
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
        self._check_bullet_zombie_collisions()
    
    def _check_bullet_zombie_collisions(self):
        """Respond to bullet-zombie collisions."""
        #Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.zombies, True, True)
        
        if collisions:
            for zombies in collisions.values():
                self.stats.score += self.settings.zombie_points * len(zombies)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.zombies:
            #Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()
    

    def _update_zombies(self):
        """
        Check if the fleet is at an edge,
            the update the positions of all zombies in the fleet.
        """
        self._check_fleet_edges()
        self.zombies.update()

        #Look for zombie-frog collisions.
        if pygame.sprite.spritecollideany(self.frog, self.zombies):
            self._frog_hit()
        #    print("Frog hit!!")

        #Look for zombies hitting the bottom of the screen.
        self._check_zombies_bottom()
        
    def _frog_hit(self):
        """Respond to the frog being hit by an zombie."""

        if self.stats.frogs_left > 0:
            #Decrement frog left and update scoreboard
            self.stats.frogs_left -= 1
            self.sb.prep_frogs()

            #Get rid of any remaining zombies and bullets.
            self.zombies.empty()
            self.bullets.empty()

            #Create a new fleet and center the frog.
            self._create_fleet()
            self.frog.center_frog()

            #Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of zombies."""
        #Create an zombie and find the number of zombies in a row.
        #Spacing between each zombie is equal to one zombie width
        zombie = Zombie(self)
        zombie_width, zombie_height = zombie.rect.size
        available_space_x = self.settings.screen_width - (2*zombie_width)
        number_zombies_x = available_space_x // (2*zombie_width)

        #Determine the number of rows of zombies that fit on the screen.
        frog_height = self.frog.rect.height
        available_space_y = (self.settings.screen_height - (2*zombie_height) - frog_height)
        number_rows = available_space_y // (2*zombie_height)
        #Create the full fleet of zombies
        for row_number in range(number_rows):
            for zombie_number in range(number_zombies_x):
                self._create_zombie(zombie_number, row_number)
    
    def _create_zombie(self, zombie_number, row_number):
        #Create an zombie and place it in the row.
        zombie = Zombie(self)
        zombie_width, zombie_height = zombie.rect.size
        zombie.x = zombie_width + 2*zombie_width*zombie_number
        zombie.rect.x = zombie.x
        zombie.rect.y = zombie.rect.height + 2 * zombie.rect.height * row_number
        self.zombies.add(zombie)
    
    def _check_fleet_edges(self):
        """Respond appropriately if any zombies have reached an edge."""
        for zombie in self.zombies.sprites():
            if  zombie.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for zombie in self.zombies.sprites():
            zombie.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # self.screen.fill(self.settings.bg_color)
        background_image = pygame.image.load("images/bg.jpg").convert()
        self.screen.blit(background_image, [0, 0])
        self.frog.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.zombies.draw(self.screen)

        #Draw the score information.
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()
    
    def _check_zombies_bottom(self):
        """Check if any zombies have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for zombie in self.zombies.sprites():
            if zombie.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the frog got hit.
                self._frog_hit()
                break

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = Zominion()
    ai.run_game()