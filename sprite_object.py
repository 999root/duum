import pygame as pg
from settings import *
import os
from collections import deque


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        # Reference to the game and player
        self.game = game
        self.player = game.player
        
        # Sprite position in the game world (x, y)
        self.x, self.y = pos
        
        # Load the sprite image and set dimensions
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        
        # Variables for sprite's relation to the player (distance, angle)
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        
        # Sprite properties
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        """
        Projects the sprite onto the player's view (screen space).
        Uses the normalized distance for depth-based scaling.
        """
        # Calculate projection size based on distance and sprite scale
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        
        # Resize the sprite image to match its projection size
        image = pg.transform.scale(self.image, (proj_width, proj_height))
        
        # Determine horizontal and vertical position for the sprite
        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift
        
        # Append sprite to the list of objects to render
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        """
        Determines the sprite's position relative to the player (distance, angle),
        and whether it should be visible on the screen.
        """
        # Calculate the distance and angle from the player to the sprite
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)  # Angle between sprite and player
        
        # Calculate the angle difference between the sprite and player's viewing angle
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau  # Adjust angle based on player's quadrant
        
        # Convert the angle difference into a screen position (ray number)
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE
        
        # Calculate the distance to the sprite and normalize it to remove fish-eye effect
        self.dist = math.hypot(dx, dy)  # Euclidean distance
        self.norm_dist = self.dist * math.cos(delta)
        
        # Check if the sprite is in the player's view and close enough to be rendered
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        """
        Called every frame to update the sprite's state.
        Checks if the sprite should be visible to the player.
        """
        self.get_sprite()



class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        # Inherit from SpriteObject
        super().__init__(game, path, pos, scale, shift)
        
        # Animation timing and path
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]  # Directory path for animation frames
        
        # Load animation images
        self.images = self.get_images(self.path)
        
        # Variables to control animation timing
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        """
        Updates the animated sprite each frame.
        It checks the animation timing and updates the sprite projection.
        """
        super().update()  # Call parent update method to handle sprite projection
        self.check_animation_time()  # Check if it's time to advance the animation frame
        self.animate(self.images)  # Animate the sprite

    def animate(self, images):
        """
        Rotate through the sprite's images to create an animation.
        """
        if self.animation_trigger:  # Only animate if the timing condition is met
            images.rotate(-1)  # Rotate the deque to get the next image
            self.image = images[0]  # Set the current image for rendering

    def check_animation_time(self):
        """
        Ensures the animation only updates after a certain time interval (animation_time).
        """
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        
        # If the time elapsed is greater than the defined animation time, trigger animation
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        """
        Loads all images from the specified directory and stores them in a deque.
        """
        images = deque()
        
        # Iterate over all files in the directory and load images
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        
        return images