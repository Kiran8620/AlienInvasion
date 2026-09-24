import pygame

class SoundManger:
    """A class to manage the sound of the game"""

    def __init__(self):
        """Initialize the sound of the game"""
        pygame.mixer.init()

        # Sound effects
        self.fire_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.alien_hit_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.ship_hit_sound = pygame.mixer.Sound('sounds/ship_explosion.wav')

        self.fire_sound.set_volume(0.5)
        self.alien_hit_sound.set_volume(0.5)
        self.ship_hit_sound.set_volume(0.9)
        

        # Background Music
        pygame.mixer.music.load('sounds/space.ogg')

        self.music_on = True


        # Play and Pause sound
        self.play_sound = pygame.mixer.Sound('sounds/play.wav')
        self.pause_sound = pygame.mixer.Sound('sounds/pause.wav')

        self.play_sound.set_volume(0.5)
        self.pause_sound.set_volume(0.3)


    def play_fire(self):
        self.fire_sound.play()


    def play_alien_hit(self):
        self.alien_hit_sound.play()


    def play_ship_hit(self):
        self.ship_hit_sound.play()


    def play_play(self):
        self.play_sound.play()


    def play_pause(self):
        self.pause_sound.play()


    def start_music(self):
        """Looping the background music, if the music is enabled"""
        if self.music_on:
            pygame.mixer.music.play(loops=-1)



    def pause_music(self):
        pygame.mixer.music.pause()


    def unpause_music(self):
        if self.music_on:
            pygame.mixer.music.unpause()


    def toggle_music(self):
        """Mute/unmute background music entirely (using M/m)"""
        self.music_on = not self.music_on
        if self.music_on:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()