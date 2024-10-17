import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        # Init the Raycasting class
        self.game = game # Reference to the main game object
        self.ray_casting_result = [] # Stores results of each raycast (depth, project_height, texture, offset)
        self.objects_to_render = [] # List of objects (walls) to be rendered
        self.textures = self.game.object_render.wall_textures # Reference to wall textures

    def get_objects_to_render(self):
        """
        Convert raycasting results into objects that will be rendered.
        Scales the wall texture according to the calculated projection height for each ray.
        """
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # If the walls is within the screen height
            if proj_height < HEIGHT:
                # Get the vertical slice of the wall texture
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )

                # Scale the wall column to match the projected height
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))

                # Determine the position to draw the wall (center vertically)
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                # For very close walls, the projected height exceeds screen height
                # Determine the texture height to fit the screen size
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )

                # Scale the wall to match the screen height
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))

                # Place the wall at the top of the screen
                wall_pos = (ray * SCALE, 0)

            # Append the wall to the render list along with depth info for sorting
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """
        Perform raycasting to determine what walls are visible to the player.
        For each ray, it calculates the intersection with vertical and horizontal grid lines
        to find the nearest wall. This method uses trigonometry to simulate the player's field
        of view by casting rays and determining wall distances.
        """

        # Clear the previous result
        self.ray_casting_result = []

        # Tecture Ids for vertical and horizontal walls
        texture_vert, texture_hor = 1, 1

        # Player's current position (x,y)
        ox, oy = self.game.player.pos

        # Player's current map grid position
        x_map, y_map = self.game.player.map_pos

        # Start casting rays across the player's field of view
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # Start angle for the first ray

        # Loop over the number of rays (to simulate the player's field of view)
        for ray in range(NUM_RAYS):
            # Calculate the direction of the ray using trigonometry
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Horizontal grid intersection (find where the ray crosses a horizontal grid line)
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1) # Check if ray is pointing up or down

            #  Calculate teh distance to the first horizontal intersection
            depth_hor = (y_hor - oy) / sin_a

            # Calculate the X Coordinate between horizontal intersections
            x_hor = ox + depth_hor * cos_a

            # How much distance between horizontal intersections
            delta_depth = dy / sin_a

            # How much the x-coordinate changes per intersection 
            dx = delta_depth * cos_a

            # Check for wall collisions
            for i in range(MAX_DEPTH):

                # Get the map tile at the intersection point
                tile_hor = int(x_hor), int(y_hor)

                # Check if this tile contains a wall
                if tile_hor in self.game.map.world_map:
                    # Get the wall's texture id
                    texture_hor = self.game.map.world_map[tile_hor]
                    break # Stop once we hit the wall

                # Move to the next horizontal grid line
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Vertical grid intersection (find where the ray crosses a vertical grid line)
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1) # Check if ray is pointing left or right

            # Calculate the distance to the first vertical intersection
            depth_vert = (x_vert - ox) / cos_a

            # Calculate the Y-Coordinate of the intersection
            y_vert = oy + depth_vert * sin_a

            # How much distance between vertical intersections
            delta_depth = dx / cos_a

            # How much the y-coordinate changes per intersection
            dy = delta_depth * sin_a

            # Check for vertical wall collisions
            for i in range(MAX_DEPTH):
                # Get current tile
                tile_vert = int(x_vert), int(y_vert)

                # Check if this tile contains a wall
                if tile_vert in self.game.map.world_map:
                    # Get the wall's texture id
                    texture_vert = self.game.map.world_map[tile_vert]
                    break # Stop once we've hit the wall

                # Move to the next vertical grid line
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Determine which collision is closer: horizontal or vertical
            if depth_vert < depth_hor:
                # Vertical wall is closer
                depth, texture = depth_vert, texture_vert
                # Calculate texture offset (fractional part of the intersection point)
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                # Horizontal wall is closer
                depth, texture = depth_hor, texture_hor
                # Calculate texture offset (fractional part of the intersection point)
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Remove fish-eye effect by adjustinmg depth based on player's view angle
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Calculate the projected wall height based on the distance to the wall
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Save the result for this ray: (depth, projected_height, texture id, texture offset)
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # Increment the ray angle for the next ray
            ray_angle += DELTA_ANGLE

    def update(self):
        # Update the raycasting results and objects to render in each frame
        self.ray_cast()
        self.get_objects_to_render()