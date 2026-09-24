import sys
from time import sleep

import pygame
import random

from starfield import Starfield
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from sound_manager import SoundManger
from space_decor import SpaceDecoreManager
from space_decor_images import SpaceDecorImages
from depth_blur import DepthBlur
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_widht = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sounds = SoundManger()
        

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = False

        pygame.mouse.set_visible(True)

        # Make the play button
        self.play_button = Button(self, "Play")


        # Pause or unpause the game
        self.game_paused = False
        self.pause_button = Button(self, "Pause")

        # For the class starfield
        self.starfield = Starfield(self)
        self.stars_far = Starfield(self, num_stars=60, speed=1)
        self.stars_near = Starfield(self, num_stars=30, speed=3)


        # For the class space_decor and space_decor images

        self.decor_images = SpaceDecorImages()


        # One manager per catagory
        decor_configs = [
            {
                # Planets
                "images":self.decor_images.space_decor_objects[0],
                "min_count": 0, "max_count": 2, "min_speed": 0.2,
                "max_speed": 0.8, "min_scale": 30, "max_scale": 300,
                "spawn_interval": 600, "max_rotation_speed":0
            },

            {
                # Asteroids
                "images":self.decor_images.space_decor_objects[1],
                "min_count": 0, "max_count": 3, "min_speed": 0.2,
                "max_speed": 0.8, "min_scale": 10, "max_scale": 350,
                "spawn_interval": 60, "max_rotation_speed":1
            }
        ]

        self.space_decors = [
            SpaceDecoreManager(
                    self, config["images"], min_count=config["min_count"], max_count=config["max_count"],
                    min_speed=config["min_speed"], max_speed=config["max_speed"], min_scale=config["min_scale"],
                    max_scale=config["max_scale"], spawn_interval=config["spawn_interval"],
                    max_rotation_speed=config["max_rotation_speed"]
                    )
                    for config in decor_configs
            ] 

        # For Depth Blur
        self.depth_blur = DepthBlur(max_blur=7, min_blur=0, overlap_margin=1)

        

    def run_game(self):
        """Start the game"""
        while True:

            for decor in self.space_decors:
                decor.update()

            self.stars_far.update()
            self.stars_near.update()

            self._check_events()

            if self.game_active and not self.game_paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()


            """Check if the fleet is at an edge, then update position"""
            self._check_fleet_edges()
        
            self._update_screen()
            self.clock.tick(62)


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()

        # Look for aliens-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            self.sounds.play_ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        self.sounds.play_ship_hit()
         # Decrement ship_left.
        self.stats.hearts_left -= 1
        self.sb.prep_ships()

        if self.stats.hearts_left > 0:

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create the new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treate this the same as if the ship get hit.
                self._ship_hit()
                break


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width


            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height



    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet position
        self.bullets.update()

        # Get rid of the bullet that disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                    self.bullets, self.aliens, True, True
                )

        if collisions:
            self.sounds.play_alien_hit()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
                    # Destroy existing bullets and create new fleet
                    self.bullets.empty()
                    self._create_fleet()
                    self.settings.increase_speed()

                    # Increase level.
                    self.stats.level += 1
                    self.sb.prep_level()


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            self._start_game()


    def _start_game(self):
        """This function will start the game/new game"""
        self.sounds.play_play()
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        
        # Reset the game statistics
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.game_active = True
        self.game_paused = False
        
        # Get rid of any remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()
        
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)


        self.sounds.start_music()



    def _toggle_pause(self):
        """Pause or unpause the game"""
        self.game_paused = not self.game_paused
        pygame.mouse.set_visible(self.game_paused)

        if self.game_paused:
            self.sounds.pause_music()
            self.sounds.play_pause()

        else:
            self.sounds.unpause_music()
            self.sounds.play_play()



    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_active and self.game_paused:
                    if self.play_button.rect.collidepoint(mouse_pos):
                        self._toggle_pause()

                else:
                    self._check_play_button(mouse_pos)


            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Respond to keypress"""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            if not self.game_active:
                self._start_game()

            else:
                self._toggle_pause()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.sounds.play_fire()

        elif event.key == pygame.K_KP_ENTER:
            self._check_play_button(event.key)

        elif event.key == pygame.K_m:
            self.sounds.toggle_music()

        elif event.key == pygame.K_BACKSPACE:
            self.stats.reset_high_score()


    def _check_keyup_events(self, event):
        """Responds to key release"""
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        
        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)


        all_decor_objects = []
        for decor in self.space_decors:
            all_decor_objects.extend(decor.objects.sprites())

        self.depth_blur.apply(self.screen, all_decor_objects)
        self.stars_near.draw()
        self.stars_far.draw()

        # self.starfield.draw()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        elif self.game_paused:
            self.pause_button.draw_button()
            
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()