from collections import deque
from functools import lru_cache


class PathFinding:
    def __init__(self, game):
        self.game = game # Reference to the main game object
        self.map = game.map.mini_map # Reference our mini map for pathfinding

        # Directions left, up, right, down, diagonals
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]

        self.graph = {} # Dicitionary to store the graph representation of the map
        self.get_graph() # Create teh graph based on the mini map

    # Cached method to get the next step in the path from start to goal
    @lru_cache
    def get_path(self, start, goal):
        # Run BFS to get the visited nodes from start to goal
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal] # Start building the path from the goal
        step = self.visited.get(goal, start) # Get the previous step from the goal

        # Traverse the visited nodes back to the start to build the full path
        while step and step != start:
            path.append(step) # Add the current step to the path
            step = self.visited[step] # Move to the previous step in the path
        return path[-1] # Return the next step in the path (not the full path, just the next move)

    # Breadth-first search (BFS) Algorithm to explore nodes and find the shortest path
    def bfs(self, start, goal, graph):
        queue = deque([start]) # Initialize the BFS queue with the start node
        visited = {start: None} # Dictionary to track visited nodes and their previous node

        # Continue the BFS as long as there are no nodes in the queue
        while queue:
            cur_node = queue.popleft() # Get current node from the front of the queue

            # Have we reached the goal
            if cur_node == goal:
                break # If we've reached the goal then stop the search

            # Get all connected nodes (neigbours) of the current node
            next_nodes = graph[cur_node]

            # Explore each neigbour of the current node
            for next_node in next_nodes:
                # Only visit the neigbouring node if it hasnt been visited and isnt blocked by an npc
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node) # Add the neigbour to the queue for further exploration
                    visited[next_node] = cur_node # Mark the current node as the previous node for the neighbour
        return visited # Return the visited dictionary with the path information

    # Get all valid neighbouring nodes (next possible positions) for a given node (x, y)
    def get_next_nodes(self, x, y):
        # Check all possible moves (up, left, right, down, diagonals) and return valid neighbours
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    # Create a graph from the mini-map where each free cell is to it's valid neighbours
    def get_graph(self):
        # loop through each cell in the mini map
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col: # If the cell is walkable/false (not a wall)
                    # Add the cell to the graph and connect it to it's neighbouring nodes 
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)