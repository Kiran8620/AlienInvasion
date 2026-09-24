import pygame
import random

class Starfield:
    """Making a background like Chrome Dino game but, space themed"""

    def __init__(self, ai_game, num_stars = 100, speed = 2):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.speed = speed


        # Each star: [x, y, size, brightness]
        self.stars = []

        for _ in range(num_stars):
            x = random.randint(0, self.screen_rect.width)
            y = random.randint(0, self.screen_rect.height)
            size = random.choice([1, 1, 1, 2])
            brightness = random.choices(
                [random.randint(40, 100), random.randint(100, 180), random.randint(180, 255)],
                    weights=[70, 25, 5]   # mostly dim, few bright
                        )[0]
            self.stars.append([x, y, size, brightness])


    def update(self):
        """Move the stars downward and sideways and wrap them around"""
        for star in self.stars:
            star[1] += self.speed # Move downwards

             # Twinkle: randomly nudge a small percentage of stars' brightness
            if random.random() < 0.05:
                star[3] = max(80, min(255, star[3] + random.randint(-15, 15)))

            # Wrap around them off screen
            if star[1] > self.screen_rect.height:
                star[1] = 0
                star[0] = random.randint(0, self.screen_rect.width)


    def draw(self):
        """Draw all the stars"""
        for x, y, size, brightness in self.stars:
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)