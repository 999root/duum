import pygame as pg
from settings import *


class ObjectRenderer:
    # Initialize the ObjectRenderer class
    def __init__(self, game):
    
        # Reference to the main game object
        self.game = game

        # Reference to the game screen where everything is draw
        self.screen = game.screen

        # Load wall textures for rendering walls during raycasting
        self.wall_textures = self.load_wall_textures()

        # Load the sky image, resize it to fit the screen width and half the screen height
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))

        # Sky offset to create the illusion of movement when the player turns
        self.sky_offset = 0

        # Load the blood screen overlay texture to be shown when the player takes damage
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)

        # Set the size of the digits used for player's health display
        self.digit_size = 90

        # Load digit textures (0-9 and 10 for the percentage sign)
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        
        # Create a dicitionary to map digit characters (0-10) to their respective images
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

        # Load the 'game over' screen image and the 'win' screen image
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        """
        Main draw function called every frame to render the game world and HUD elements.
        """

        # Draw sky and floor
        self.draw_background()

        # Render walls and game objects
        self.render_game_objects()

        # Display the player's health in the HUD
        self.draw_player_health()

    def win(self):
        """
        Display the win screen.
        """

        # Draw the win image covering the whole screen
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        """
        Display the 'game over' screen.
        """

        # Draw the game over image covering the whole screen
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        """
        Display the player's health as digits in the HUD.
        """

        # Get the player's health and convert it to a string
        health = str(self.game.player.health)

        # Loop through each digit in the player's health
        for i, char in enumerate(health):
            # Draw each digit texture in the appropriate position
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        
        # Draw the '%' symbol to indicate health (represented by index 10 in the digit list)
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        """
        Display the blood screen when the player takes damage.
        """

        # Overlay the blood screen texture
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """
        Draw the background (sky and floor)
        """

        # Adjust the sky offset based on player's movement relative to the screen width
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH

        # Draw 2 sky images side by side for smooth scrolling
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        
        # Draw the floor as a rectangle covering the bottom half of the screen
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """
        Render game objects such as walls using the raycasting results.
        The objects are drawn in order from farthest to closest.
        """

        # Sort objects by depth (from farthest to nearest)
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        
        # Draw each object on the screen
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """
        Load and scale a texture from the given path.
        The texture is scaled to the specified resolution.
        """
        
        # Load the image and preserve transparency
        texture = pg.image.load(path).convert_alpha()

        # Scale the texture to the desired resolution
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """
        Load textures for the walls in the game world and return a dictionary mapping texture IDs to images.
        """

        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }