import pygame as pg


class Sound:
    def __init__(self, game):
        # Initialize the Sound class
        self.game = game  # Reference to the main game object

        # Initialize the pygame mixer for sound and music
        pg.mixer.init()

        # Path to the folder where all sound files are stored
        self.path = 'resources/sound/'

        # Load individual sound effects
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')  # Shotgun sound
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')  # NPC pain sound
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')  # NPC death sound
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')  # NPC attack shot sound

        # Set volume for specific sounds
        self.npc_shot.set_volume(0.2)  # Lower the NPC shot volume to 20%

        # Load player-specific sound effects
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')  # Player pain sound

        # Load background music (theme music)
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')

        # Set volume for the music
        pg.mixer.music.set_volume(0.3)  # Lower the background music to 30%
