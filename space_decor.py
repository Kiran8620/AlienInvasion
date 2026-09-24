import pygame
import random

from motion_blur import MotionBlur

class SpaceObject(pygame.sprite.Sprite):
    """A single class to handle decorative background (e.g. Planets, astroids..)"""

    def __init__(self, image, x, y, speed, rotation_speed=0, enable_blur=False):
        super().__init__()

        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
        self.y_pos = float(y)
        self.x_center = x

        self.rotation_speed = rotation_speed
        self.angle = 0

        self.motion_blur = MotionBlur(trail_length=6) if enable_blur else None

    def update(self):
        """Move the object downward and remove all the objects once out of the screen"""
        self.y_pos += self.speed

        if self.rotation_speed != 0:
            self.angle = (self.angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)


        self.rect = self.image.get_rect()
        self.rect.center = (self.x_center, self.y_pos)


        if self.motion_blur:
            self.motion_blur.record(self.image, self.rect)


    def draw_trail(self, screen):
        """Draw the motion blur trail, if it had one"""
        if self.motion_blur:
            self.motion_blur.draw(screen)



class SpaceDecoreManager:
    """Spawnm and manage space objects - with paralax effect"""

    def __init__(self, ai_game, image_paths, min_count=1, max_count=3,
                 min_speed=0.3, max_speed=1.5, min_scale=30, max_scale=80,
                 spawn_interval=180, max_rotation_speed=0):
        
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()


        # Load all the provided image
        self.images = [pygame.image.load(path).convert_alpha()
                       for path in image_paths]

        self.min_count = min_count
        self.max_count = max_count
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.spawn_interval = spawn_interval
        self.max_rotation_speed = max_rotation_speed

        self.objects = pygame.sprite.Group()
        self._frame_count = 0

        # Seed some object at start so the screen don't look empty
        for _ in range(random.randint(min_count, max_count)):
            self._spawn_object(initial=True)


    def _spawn_object(self, initial=False):
        """Create one decorative object at a random position"""
        image = random.choice(self.images)
        scale = random.randint(self.min_scale, self.max_scale)

        # Preserver original ratio while scaling
        orig_w, orig_h = image.get_size()
        ratio = scale / max(orig_w, orig_h)
        new_size = (int(orig_w * ratio), int(orig_h * ratio))
        scaled_image = pygame.transform.smoothscale(image, new_size)

        max_x = max(0, self.screen_rect.width - new_size[0])
        x = random.randint(0, max_x)

        # If spawning at start, scatter vertically; otherwise start above the screen
        y = random.randint(0, self.screen_rect.height) if initial else - new_size[1]

        speed = random.uniform(self.min_speed, self.max_speed)

        if self.max_rotation_speed > 0:
        # Random rotation some fast, some slow, some the other way
            # min rotation speed
            min_rotation = 0.5
            rotation_speed = random.uniform(min_rotation, self.max_rotation_speed)
            if random.random() <= 0.5:
                rotation_speed *= -1

            # Faster the spin -> Faster the asteroid fall
            spin_ratio = abs(rotation_speed) / self.max_rotation_speed
            speed *= (1 + spin_ratio * 2)
            
        else:
            rotation_speed = 0

        obj = SpaceObject(scaled_image, x, y, speed, rotation_speed=rotation_speed,
                          enable_blur=(self.max_rotation_speed > 0 and abs(rotation_speed) > 0.5))
        self.objects.add(obj)


    def update(self):
        """Update existing objects, remove off-screen ones, spawn ones."""
        self.objects.update()

        # Remove anything that scroll past the screen
        for obj in self.objects.copy():
            if obj.rect.top > self.screen_rect.height:
                self.objects.remove(obj)

        # Periodically spawn the object to keep the screen fill.
        self._frame_count += 1
        if self._frame_count >= self.spawn_interval:
            self._frame_count = 0
            if len(self.objects) < self.max_count:
                self._spawn_object()


    def draw(self):
        for obj in self.objects:
            obj.draw_trail(self.screen)
        self.objects.draw(self.screen)