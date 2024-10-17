
from settings import *
import pygame as pg
import math

class Player():
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

        self.diag_move_corr = 1 / math.sqrt(2)

    #  If the player has met the requirements for the health recovery delay and is below maximum
    #  health then +1 to their health
    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self) -> bool:
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        
    def check_game_over(self):
        if self.health < 1: # If player is the below
            self.game.object_render.game_over() # render the game over screen
            pg.display.flip()
            pg.time.delay(1500) # ms
            self.game.new_game() # load a new game

    def get_damage(self, damage):
        self.health -= damage # Take away from health the amount of damage done
        self.game.object_render.player_damage() # inform player they've been hurt
        self.game.sound.player_pain.play() # MP3 of the character in pain
        self.check_game_over() # Check whether they're out of health

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            #  Check the player is not in the process of shooting already or reloading their weapon
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play() # Play shotgun sfx
                self.shot = True # shoot
                self.game.weapon.reloading = True # then reload the gun

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]: # Forwards
            num_key_pressed += 1 
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]: # Backwards
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]: # Left
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]: # Right
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # Diagonal Moving Correction
        if num_key_pressed:
            dx *= self.diag_move_corr
            dy *= self.diag_move_corr

        self.check_wall_collision(dx, dy) # Make sure the player can't walk through walls

        self.angle %= math.tau # tau = 2*pi

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self) -> tuple:
        return self.x, self.y
    
    @property
    def map_pos(self) -> tuple:
        return int(self.x), int(self.y)