from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game  # Reference to the main game instance
        self.sprite_list = []  # List of static and animated sprites
        self.npc_list = []  # List of NPCs
        self.npc_sprite_path = 'resources/sprites/npc/'  # Path to NPC sprites
        self.static_sprite_path = 'resources/sprites/static_sprites/'  # Path to static sprites
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'  # Path to animated sprites
        
        # Methods for adding sprites and NPCs
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}  # Dictionary to track NPC positions

        # Configure NPC spawn
        self.enemies = 20  # Total number of enemies (NPCs)
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]  # List of NPC types
        self.weights = [70, 20, 10]  # Probabilities for spawning each type (70% Soldier, 20% CacoDemon, 10% CyberDemon)
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # Areas where NPCs cannot spawn
        
        self.spawn_npc()  # Spawn NPCs

        # Add static and animated sprites to the game world
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        # npc map
        # add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        # add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        # add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        # add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        # add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        # add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))

    def spawn_npc(self):
        for i in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]  # Randomly select an NPC type based on the weights
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)  # Generate random coordinates
            # Ensure the position is not in the world map or restricted area
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))  # Add the NPC to the game world


    def check_win(self):
        if not len(self.npc_positions):  # If there are no NPCs left
            self.game.object_renderer.win()  # Show the win screen
            pg.display.flip()  # Refresh the display
            pg.time.delay(1500)  # Wait 1.5 seconds before starting a new game
            self.game.new_game()  # Start a new game


    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}  # Update NPC positions
        [sprite.update() for sprite in self.sprite_list]  # Update all sprites
        [npc.update() for npc in self.npc_list]  # Update all NPCs
        self.check_win()  # Check if the player has won


    def add_npc(self, npc):
        self.npc_list.append(npc)  # Add an NPC to the list


    def add_sprite(self, sprite):
        self.sprite_list.append(sprite) # Add a sprite to the list