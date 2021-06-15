class Settings:
    """A Class to store all settings for Zominion."""
    
    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 720
        self.bg_color = (212, 191, 87)

        #frog settings
        self.frog_speed = 8.5
        self.frog_limit = 5

        #Bullet settings
        self.bullet_speed = 10
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        #Zombie settings
        self.zombie_speed = 2.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #How quickly the game speeds up
        self.speedup_scale = 4.0

        #How quickly the zombie point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.frog_speed = 8.5
        self.bullet_speed = 10
        self.zombie_speed = 2.0

        #fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

        #Scoring
        self.zombie_points = 10
    
    def increase_speed(self):
        """Increase speed settings and zombies point values."""
        self.frog_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.zombie_speed *= self.speedup_scale

        self.zombie_points = int(self.zombie_points*self.score_scale)