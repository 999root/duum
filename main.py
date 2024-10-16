
# Pygame Library
import pygame as pg

# System Library for quiting and exiting
import sys

# Game Instances Imports
from settings import *
from map import *
from player import *
from object_renderer import *
from raycasting import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init() # Initialise pygame
        pg.mouse.set_visible(False) # Disable your cursor
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game() # Create a new game upon the instance's initialisation

    def new_game(self):
        self.map = Map(self) # Initialise the Map
        self.player = Player(self) # Initialise our Player
        self.object_render = ObjectRenderer(self) # Render Objects
        self.raycasting = RayCasting(self) # Initialise our Raycasting
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :1.f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while 1:
            self.check_events() # Run Event Handler
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()