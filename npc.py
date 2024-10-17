from sprite_object import *  # Import necessary classes and functions from sprite_object
from random import randint, random  # Import random utilities

# Base NPC class inheriting from AnimatedSprite for animated NPCs
class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        # Initialize the base AnimatedSprite class with NPC-specific settings
        super().__init__(game, path, pos, scale, shift, animation_time)
        
        # Load images for different animations (attack, death, idle, pain, walk)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        # NPC attributes for attack, movement, size, and health
        self.attack_dist = randint(3, 6)  # Randomize attack distance within range
        self.speed = 0.03  # Movement speed
        self.size = 20  # Hitbox size for collision detection
        self.health = 100  # Initial health of the NPC
        self.attack_damage = 10  # Damage dealt when attacking the player
        self.accuracy = 0.15  # Probability of hitting the player when attacking
        
        # State management flags
        self.alive = True  # Indicates if the NPC is alive
        self.pain = False  # Whether NPC is in a pain animation
        self.ray_cast_value = False  # Whether the NPC sees the player
        self.frame_counter = 0  # Frame counter for death animation
        self.player_search_trigger = False  # Whether NPC is actively searching for the player

    def update(self):
        # Called every frame: update NPC logic, animations, and sprite projection
        self.check_animation_time()  # Check if it's time to change animation frame
        self.get_sprite()  # Get the current sprite projection
        self.run_logic()  # Run the core AI logic for this NPC

    def check_wall(self, x, y):
        # Check if a given (x, y) position is not a wall
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        # Prevent NPC from moving through walls, adjust movement based on wall collisions
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx  # Move horizontally if no collision
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy  # Move vertically if no collision

    def movement(self):
        # NPC pathfinding movement logic
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)  # Get path to player
        next_x, next_y = next_pos  # Extract next position

        if next_pos not in self.game.object_handler.npc_positions:  # Ensure the position is not occupied
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)  # Calculate angle to next position
            dx = math.cos(angle) * self.speed  # Calculate x displacement based on angle and speed
            dy = math.sin(angle) * self.speed  # Calculate y displacement
            self.check_wall_collision(dx, dy)  # Move while checking for wall collisions

    def attack(self):
        # Attack logic: NPC attacks the player if within range and animation triggers
        if self.animation_trigger:
            self.game.sound.npc_shot.play()  # Play attack sound
            if random() < self.accuracy:  # Determine hit based on accuracy
                self.game.player.get_damage(self.attack_damage)  # Deal damage to player

    def animate_death(self):
        # Animate death sequence if NPC is dead
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)  # Rotate through death animation frames
                self.image = self.death_images[0]  # Set current image to the first frame
                self.frame_counter += 1  # Increment frame counter

    def animate_pain(self):
        # Animate pain sequence if NPC is hit
        self.animate(self.pain_images)  # Use pain images for animation
        if self.animation_trigger:
            self.pain = False  # Exit pain state after animation finishes

    def check_hit_in_npc(self):
        # Check if player shot hits the NPC
        if self.ray_cast_value and self.game.player.shot:  # If the player shoots and NPC is in line of sight
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()  # Play pain sound
                self.game.player.shot = False  # Reset player's shot flag
                self.pain = True  # Set NPC to pain state
                self.health -= self.game.weapon.damage  # Reduce health by weapon damage
                self.check_health()  # Check if NPC has died

    def check_health(self):
        # Check if the NPC is dead
        if self.health < 1:
            self.alive = False  # Set NPC to dead
            self.game.sound.npc_death.play()  # Play death sound

    def run_logic(self):
        # Core NPC AI logic controlling movement, attacking, and animations
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()  # Check if NPC has line of sight to player
            self.check_hit_in_npc()  # Check if the NPC has been hit by the player

            if self.pain:
                self.animate_pain()  # Animate pain if NPC is hit

            elif self.ray_cast_value:
                self.animate(self.attack_images)  # Animate attack sequence
                self.attack()  # Execute attack logic

                if self.dist < self.attack_dist:  # If close enough to the player
                    self.animate(self.attack_images)  # Continue attack animation
                    self.attack()  # Attack the player again

                else:
                    self.animate(self.walk_images)  # Otherwise, animate walking
                    self.movement()  # Move towards the player

            elif self.player_search_trigger:  # If searching for the player
                self.animate(self.walk_images)  # Animate walking
                self.movement()  # Move to the next position

            else:
                self.animate(self.idle_images)  # Animate idle state if no player is in sight
        else:
            self.animate_death()  # Animate death if NPC is dead

    @property
    def map_pos(self):
        # Return the NPC's position on the map grid
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self) -> bool:
        # Perform raycasting to check if the NPC can see the player
        if self.game.player.map_pos == self.map_pos:
            return True  # If NPC and player are at the same position, return True
        
        # Initialize distances for raycasting
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        # Get player position and map position
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta  # Angle between NPC and player

        # Calculate vertical and horizontal ray intersections for raycasting
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Horizontal calculations
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor  # Calculate player distance on horizontal axis
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor  # Calculate wall distance on horizontal axis
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Vertical calculations
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert  # Calculate player distance on vertical axis
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert  # Calculate wall distance on vertical axis
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # Get maximum player and wall distances
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        # Return True if player is closer than the nearest wall, or if no wall is found
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        # Draw raycasting line from NPC to player for debugging
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)

# Soldier NPC class inheriting from the base NPC class
class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

# CacoDemon NPC class inheriting from NPC, with specific attributes for the demon
class CacoDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0  # Shorter attack distance
        self.health = 150  # Higher health
        self.attack_damage = 25  # Stronger attack
        self.speed = 0.05  # Faster movement
        self.accuracy = 0.35  # More accurate attacks

# CyberDemon NPC class inheriting from NPC, with specific attributes for a boss-like enemy
class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6  # Longer attack distance
        self.health = 350  # Very high health
        self.attack_damage = 15  # Moderate attack damage
        self.speed = 0.055  # Slightly faster movement
        self.accuracy = 0.25  # Moderate accuracy