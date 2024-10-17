import math

# Game settings
RES = WIDTH, HEIGHT = 1600, 900  # Resolution of the game window (width x height)
# RES = WIDTH, HEIGHT = 1920, 1080  # Alternative resolution for the game window (optional)
HALF_WIDTH = WIDTH // 2  # Half of the screen width, used in various calculations
HALF_HEIGHT = HEIGHT // 2  # Half of the screen height, used in various calculations
FPS = 0  # Frames per second setting (0 might mean uncapped or unlimited FPS)

# Player settings
PLAYER_POS = 1.5, 5  # Initial player position on the mini-map (x, y)
PLAYER_ANGLE = 0  # Initial angle or direction the player is facing (in radians)
PLAYER_SPEED = 0.004  # Speed at which the player moves forward/backward
PLAYER_ROT_SPEED = 0.002  # Speed at which the player rotates or turns
PLAYER_SIZE_SCALE = 60  # Scaling factor to adjust the player's size for collision detection
PLAYER_MAX_HEALTH = 100  # Maximum health of the player

# Mouse settings
MOUSE_SENSITIVITY = 0.0003  # Sensitivity for mouse movement, controlling how fast the player turns
MOUSE_MAX_REL = 40  # Maximum amount of mouse movement that will be registered in one frame
MOUSE_BORDER_LEFT = 100  # Left border limit for the mouse movement (keeps mouse in the middle area)
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT  # Right border limit for mouse movement

# Floor settings
FLOOR_COLOR = (30, 30, 30)  # RGB color for the floor in the game (a dark gray color)

# Raycasting settings
FOV = math.pi / 3  # Field of view (FOV) of the player, set to 60 degrees (pi/3 radians)
HALF_FOV = FOV / 2  # Half of the field of view, used for calculations
NUM_RAYS = WIDTH // 2  # Number of rays cast for rendering (half the screen width)
HALF_NUM_RAYS = NUM_RAYS // 2  # Half of the number of rays, used for centering
DELTA_ANGLE = FOV / NUM_RAYS  # The angle difference between each ray
MAX_DEPTH = 20  # Maximum depth (distance) the ray will travel in the 3D world

# Screen distance settings
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)  # Distance from the player to the projection plane (used for 3D rendering)
SCALE = WIDTH // NUM_RAYS  # Scaling factor for the width of each ray on the screen

# Texture settings
TEXTURE_SIZE = 256  # Size of each texture (width and height), typically a square
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2  # Half of the texture size, often used in rendering calculations
