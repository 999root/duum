import pygame as pg
import sys

from settings import *  # Import settings such as resolution, FPS, etc.
from map import *  # Import the map system
from player import *  # Import player-related code
from raycasting import *  # Import raycasting functionality
from object_renderer import *  # Import the object rendering system
from sprite_object import *  # Import sprite handling code
from object_handler import *  # Import object management logic
from weapon import *  # Import weapon system
from sound import *  # Import sound handling
from pathfinding import *  # Import pathfinding algorithms

# Game class to manage the game loop, events, and objects
class Game:
    def __init__(self):
        # Initialize pygame and set up the game environment
        pg.init()  # Initialize all pygame modules
        pg.mouse.set_visible(False)  # Hide the system mouse cursor
        self.screen = pg.display.set_mode(RES)  # Set the display/window resolution
        pg.event.set_grab(True)  # Lock the mouse to the game window
        self.clock = pg.time.Clock()  # Create a clock to manage frame rate
        self.delta_time = 1  # Delta time to keep track of frame-to-frame time
        self.global_trigger = False  # A global trigger for event handling
        self.global_event = pg.USEREVENT + 0  # Custom user event
        pg.time.set_timer(self.global_event, 40)  # Trigger global event every 40 ms
        self.new_game()  # Start a new game

    def new_game(self):
        # Initialize the main components of the game (map, player, etc.)
        self.map = Map(self)  # Initialize the game map
        self.player = Player(self)  # Initialize the player
        self.object_render = ObjectRenderer(self)  # Initialize the object renderer
        self.raycasting = RayCasting(self)  # Initialize the raycasting system
        self.object_handler = ObjectHandler(self)  # Handle in-game objects (e.g. enemies, items)
        self.weapon = Weapon(self)  # Initialize the weapon system
        self.sound = Sound(self)  # Initialize sound effects and background music
        self.pathfinding = PathFinding(self)  # Initialize the pathfinding system (e.g. AI navigation)
        pg.mixer.music.play(-1)  # Play background music indefinitely

    # Update all game objects (called every frame)
    def update(self):
        self.player.update()  # Update the player state (movement, shooting, etc.)
        self.raycasting.update()  # Perform raycasting to detect walls, objects, etc.
        self.object_handler.update()  # Update the state of all game objects
        self.weapon.update()  # Update the weapon (shooting, reloading, etc.)
        pg.display.flip()  # Update the display with new frame content
        self.delta_time = self.clock.tick(FPS)  # Control frame rate and calculate delta time
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # Display the current FPS in the window title

    # Draw game objects to the screen (called every frame)
    def draw(self):
        self.object_render.draw()  # Render all visible objects in the scene
        self.weapon.draw()  # Draw the player's weapon on screen

    # Handle all game events (input, quit, etc.)
    def check_events(self):
        self.global_trigger = False  # Reset global trigger before checking events
        
        # Loop through all events
        for event in pg.event.get():

            # Quit the game if the user closes the window or presses ESC
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)

            elif event.type == self.global_event:
                # Trigger custom global event (used for timed updates)
                self.global_trigger = True
            # Check for specific player-related events (e.g. firing weapon)
            self.player.single_fire_event(event)

    # Main game loop
    def run(self):
        while True:  # Game loop runs indefinitely until the game is quit
            self.check_events()  # Handle user input and events
            self.update()  # Update all game objects and logic
            self.draw()  # Draw the updated frame

# Run the game if this script is executed directly
if __name__ == "__main__":
    game = Game()  # Create a Game instance
    game.run()  # Start the main game loop