from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):

        # Initialize the AnimatedSprite parent class with necessary arguments
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)

        # Scale all weapon iomages for proper display
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        
        #  Position the weapon at the bottom center of the screen
        self.weapon_pos = (HALF_WIDTH - self.image.get_width() // 2, HEIGHT - self.images[0].get_height())

        # Weapon-related attributes
        self.reloading = False # Indicates whether the weapon ius in the process of reloading (or shooting)
        self.num_images = len(self.images) # Total number of images used for the animation
        self.frame_counter = 0 # Counts animation frames to control playback
        self.damage = 100 # The amount of damage the weapon deals

    def animate_shot(self):
        """
        Animate the weapon's shot by cycling through images.
        This is triggered when the player shoots, and continues while 'reloading' is true.
        """

        # Animation only happens if the weapon is in the 'reloading' state
        if self.reloading:

            # Disable shooting while reloading
            self.game.player.shot = False

            # Check if it's time to animate (based on time)
            if self.animation_trigger:
                # Rotate through weapon images to creat the shot animation effect
                self.images.rotate(-1)
                self.image = self.images[0]

                # Increase frame counter to track the animation seqience
                self.frame_counter += 1

                # If all frames have been shown, reset the animation
                if self.frame_counter == self.num_images:
                    # End reloading once the animation finishes
                    self.reloading = False

                    # Reset frame counter for the next shot
                    self.frame_counter = 0

    def draw(self):
        """
        Draw the current weapon image on the screen at the calculated weapon position.
        """

        self.game.screen.blit(self.images[0], self.weapon_pos) # Draw the first image of the deque

    def update(self):
        """
        Update the weapon state, including animation timing and shot animation.
        This is called every frame.
        """

        # Check if enough time has passed to animate new frame
        self.check_animation_time()

        # Handle the shot animation logic
        self.animate_shot()