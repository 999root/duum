import pygame as pg

_ = False # This is a shortcut to represent empty spaces in the mini-map
mini_map = [ # Define the layout of the mini-map using a 2D list
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1], # 1 Represents walls (Edges of Map)
    [1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1], #  _ = False (Represents Open Space)
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1], # Different numbers represent different objects
    [1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1], # like = 2 another type of wall, 3, 4, 5 = other objects
    [1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1], # These numbers can represent enemy spawn points etc.
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, 4, _, _, _, 4, _, _, _, _, _, _, 1], # The structure creates a maze like enviornment
    [1, 1, 1, 3, 1, 3, 1, 1, 1, 3, _, _, 3, 1, 1, 1], # With walls and pathways
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 1, 3, 1, 1, 1, 1, 1, 1, 3, _, _, 3, 1, 1, 1],
    [1, 4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, 3, 4, _, 4, 3, _, 1],
    [1, _, _, 5, _, _, _, _, _, _, 3, _, 3, _, _, 1],
    [1, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 4, _, _, _, _, _, _, 4, _, _, 4, _, _, _, 1],
    [1, 1, 3, 3, _, _, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1],
    [1, 1, 1, 3, _, _, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 3, 4, _, _, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, 5, _, _, _, 5, _, _, _, 5, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]


class Map:
    def __init__(self, game):
        self.game = game # Link map class to the game's instance
        self.mini_map = mini_map # Assign the mini map layout above to this instance
        self.world_map = {} # Dictionary to store the world map (Converted from Mini Map)
        self.rows = len(self.mini_map) # number of rows in the mini map
        self.cols = len(self.mini_map[0]) # number of columns in the mini map
        self.get_map() # Call the method to process and store the map information

    def get_map(self):
        for j, row in enumerate(self.mini_map): # Loop through the rows
            for i, value in enumerate(row): # Loop through each value in the row
                if value: # if the value is not false or not an open space
                    self.world_map[(i, j)] = value # Add it to the world map with it's coordinates as key

    # Method to draw the map using pygame
    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map] # draw a rectangle for each block in the world map