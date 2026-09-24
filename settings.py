class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's satistics settings"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 20)

        # Ship's Settings
        self.ship_speed = 3.0
        self.heart_limit = 3

        # Bullet's Settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 17
        self.bullet_color = (250, 0, 0)
        self.bullets_allowed = 5

        # Alien's Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values inceases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 3.0
        self.bullet_speed = 5.0
        self.alien_speed = 2.0
        self.bullet_width = 3
        self.bullets_allowed = 5

        # Fleet_direction of 1 represent right; -1 represent left.
        self.fleet_direction = 1

        # Scoring Setting
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings an alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullets_allowed += 2

        if self.bullet_width <= 300:
            self.bullet_width *= 1.2

        if self.alien_speed >= 19.1943425:
            self.alien_speed += 0.00002

        if self.ship_speed >= 47.589279:
            self.ship_speed += 0.00002

        self.alien_points = int(self.alien_points * self.score_scale)