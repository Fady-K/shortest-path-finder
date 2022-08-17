import curses
from curses import wrapper
import queue
import time

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
    blue = curses.color_pair(1)
    red = curses.color_pair(2)
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", red)
            else:
                stdscr.addstr(i, j*2, value, blue)



def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
                break


# This function returns the end point position
def find_end(maze):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == "X":
                return i, j
                break
 


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)
    
    # initialize the queue
    q = queue.Queue()
    q.put(((start_pos), [start_pos]))

    # don't check nodes in visisted set
    visited = set()


    # breadth first search alogrithm
    while not q.empty():
        currenct_pos, path = q.get()
        row, col = currenct_pos


        # print the maze every new iteration with red path
        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()
        time.sleep(0.2)

        # check if node whose pair == (row, col) is end
        if maze[row][col] == end:
            return path

        # get all neighbors to check them 
        neighbors = find_neighbors(maze, row, col)


        # check the fetched neighbor
        for neighbor in neighbors:

            # check if neighbore is already visited
            if neighbor in visited:
                continue

            # if neighbor is obstacle ignore it (continue)
            r, c = neighbor
            if maze[r][c] == "#":
                continue

            # form the new path
            new_path = path + [neighbor]

            # add This neighbor to the queue with anew path starting with it's position
            q.put((neighbor, new_path))
            
            # asighn this node as visited 
            visited.add(neighbor)    # which is a pair




# The functions returns Neighbors of currenct node
def find_neighbors(maze, row, col):
    neighbors = []

    # get the upper neighbor
    if row > 0:
        neighbors.append((row - 1, col))    # Up
    
    # get the down neighbor
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))    # down

    # get left node
    if col > 0:
        neighbors.append((row, col - 1))      # left

    # get right node (neibore)
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))  # right
    
    
    return neighbors


def main(stdscr):
    # colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_path(maze, stdscr)
    stdscr.getch()
wrapper(main)
