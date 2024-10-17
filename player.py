
from settings import *
import pygame as pg
import math

class Player():
    def __init__(self, game):
        self.game = game  # Reference to the main game instance
        self.x, self.y = PLAYER_POS  # Set player's initial position
        self.angle = PLAYER_ANGLE  # Set player's initial angle (direction)
        self.shot = False  # Track if player has fired a shot
        self.health = PLAYER_MAX_HEALTH  # Initialize player's health
        self.rel = 0  # Mouse movement delta (relative motion)
        self.health_recovery_delay = 700  # Delay in milliseconds before health recovery
        self.time_prev = pg.time.get_ticks()  # Timestamp to track health recovery timing

        self.diag_move_corr = 1 / math.sqrt(2)  # Correction factor for diagonal movement

    #  If the player has met the requirements for the health recovery delay and is below maximum
    #  health then +1 to their health
    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1 # Recover 1 Health Unit if enough time has passed

    # Check if time for health recovery has passed
    def check_health_recovery_delay(self) -> bool:
        time_now = pg.time.get_ticks() # Get current time
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now # Update previous time
            return True # Return True if enough time has passed for recovery
    
    # Check if player's health has dropped below 1 (game over)
    def check_game_over(self):
        if self.health < 1: # If player is the below
            self.game.object_render.game_over() # render the game over screen
            pg.display.flip() # Update display
            pg.time.delay(1500) # Delay Before ...
            self.game.new_game() # Loading a new game

    # Handle damage delt to the player
    def get_damage(self, damage):
        self.health -= damage # Take away from health the amount of damage done
        self.game.object_render.player_damage() # inform player they've been hurt
        self.game.sound.player_pain.play() # MP3 of the character in pain
        self.check_game_over() # Check whether they're out of health

    # Handle mouse button events (Firing Weapon)
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN: # If left click
            #  Check the player is not in the process of shooting already or reloading their weapon
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play() # Play shotgun Sound Effect
                self.shot = True # Player has fired a shot
                self.game.weapon.reloading = True # Cock/Reload the gun

    # Manage the player's movement based on keyboard inputs
    def movement(self):
        sin_a = math.sin(self.angle) # Calculate the Sine of the player's angle
        cos_a = math.cos(self.angle) # Calculate the Cosine of the player's angle
        dx, dy = 0, 0 # Init movement in x and y directions
        speed = PLAYER_SPEED * self.game.delta_time # Player's movement speed adjusted by delta time
        speed_sin = speed * sin_a # Movement speed on the Y Axis
        speed_cos = speed * cos_a # Movement speed on the X Axis

        keys = pg.key.get_pressed() # Get currently pressed keys
        num_key_pressed = -1 # Track number of keys pressed for diagonal movement check
        if keys[pg.K_w]: # Move forward
            num_key_pressed += 1 
            dx += speed_cos # Adjust X Position
            dy += speed_sin # Adjust Y Position
        if keys[pg.K_s]: # Move Backwards
            num_key_pressed += 1
            dx += -speed_cos # adjust x position
            dy += -speed_sin # adjust y position
        if keys[pg.K_a]: # Move Left
            num_key_pressed += 1
            dx += speed_sin # Adjust X Position
            dy += -speed_cos# Adjust Y Position
        if keys[pg.K_d]: # Move Right
            num_key_pressed += 1
            dx += -speed_sin # Adjust X Position
            dy += speed_cos # Adjust Y Position

        # Apply Diagonal Moving Correction
        if num_key_pressed:
            dx *= self.diag_move_corr # Scale Down Diagonal Movement
            dy *= self.diag_move_corr # Scale Down Diagonal Movement

        self.check_wall_collision(dx, dy) # Check and prevent wall collisions

        self.angle %= math.tau # Normalize angle with 2 radians

    # Check if the player's future position would collid with a wall
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map # Return true if position is not where a wall is
    
    # Handle wall collisions with walls and adjust the player's position accordingly
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time # Scale movement based on the Player's Size and delta_time

        # Dont let the player move in the coordinal direction if there is a wall there
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx # Update X Position if there is no collision
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy # Update Y Position if there is no collision

    # Draw player's position and oriental on the mini map
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos() # Get mouse position
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT]) # Reset mouse position to the center of the screen if it goes beyond the borders of the window/screen
        self.rel = pg.mouse.get_rel()[0] # Get mouse movement relative
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel)) # Clamp mouse movement to avoid overly fast rotations
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time # Update player's angle based on mouse movement

    # Update player's state each frame
    def update(self):
        self.movement() # Handle player movement
        self.mouse_control() # Handle mouse input for rotation
        self.recover_health() # Handle health recovery

    # Return player's current position as a tuple
    @property
    def pos(self) -> tuple:
        return self.x, self.y

   # Return the player's current position on the map as coordinates in a tuple 
    @property
    def map_pos(self) -> tuple:
        return int(self.x), int(self.y)