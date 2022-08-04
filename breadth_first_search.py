# Breadth First Search

import curses
import queue
import time
from curses import wrapper

"""
# - Obstacles
" " - Paths
O - Starting Point
X - Exit
"""

maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                # "X" will represent current path
                stdscr.addstr(i, j*2, "X", RED)
            else:
                # j*2 - to spread columns a bit wider
                stdscr.addstr(i, j*2, value, BLUE)


def find_start(maze, start_symbol):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start_symbol:
                # Return row and the column with founded symbol
                return i, j
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    # Where are start positions?
    start_position = find_start(maze, start)

    # Create Queue (FIFO)
    q = queue.Queue()
    # [PATH] will continue to grow
    q.put((start_position, [start_position]))

    # Keep track of all elements algorithm visited
    visited = set()

    # While Queue is not empty
    while not q.empty():
        # Get most recent element
        current_position, path = q.get()
        row, col = current_position

        # Drawing current path
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        # If we are at the ened
        if maze[row][col] == end:
            return path
        
        # Continue looking for an end node
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            # Check if it is visited
            if neighbor in visited:
                # Skip visited
                continue
            
            # Check if it is obstacle
            r, c = neighbor
            if maze[r][c] == '#':
                # Skip obstacle
                continue
                
            # Add to path and queue
            new_path = path + [neighbor]
            q.put((neighbor, new_path))

            # Add to visited
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    # Not a obstacle and a valid position
    neighbors = []

    if row > 0: # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): # DOWN
        neighbors.append((row + 1, col))  
    if col > 0: # LEFT
        neighbors.append((row, col - 1))  
    if col + 1 < len(maze[0]): # RIGHT
        neighbors.append((row, col + 1))  
    
    return neighbors

# Standard Output Screen
def main(stdscr):
    # Add background and foreground colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)

    # Wait for character or move and close up
    stdscr.getch()  

wrapper(main)