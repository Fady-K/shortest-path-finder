import queue
import time
import curses
from curses import wrapper

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


def print_maze(maze, stdscr, path):
    blue = curses.color_pair(1)
    red = curses.color_pair(2)

    # enumerate take iterabel and make it a counter 
    for i, row in enumerate(maze):      # iterate over indexes of rows and rows of the maze
        for j, value in enumerate(row): # iterate over indexes of columns inside each row
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "S", red)
            else:
                stdscr.addstr(i, j * 2, value, blue)



# algorithm 
# find the start node position
def find_start(maze, start):        # iterate over each value of the maze if any equalls the start node returns it's position
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j       #

    else:
        return None


def find_all_neighbors(maze, row, col):
    neighbors = []

    # get the upper neighbor =>>>> only if the index of the current row is bigger than the 0
    if row > 0:
        neighbors.append((row - 1, col))        # UP
    
    # get the beneth neighbor (downward one) =>>>>> only if the current row is smaller than the last row index
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))        # DOWN
    
    # get the left neighbor =>>>>>>> only if the current column is bigger than 0
    if col > 0:
        neighbors.append((row, col - 1))        # LEFT
    
    # get the right neighbore =>>>>>> only if the col + 1 smaller than len(maze[0]) >> currenct row
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))        # RIGHT

    return neighbors


def find_shortest_path(maze, stdscr):
    # declare and define the start node position
    start = "O"
    end = "X"

    # breadth first searsh
    start_pos = find_start(maze, start)

    # declare the queue and add the first node pos and start a path starting with start pos as the first
    q = queue.Queue()

    q.put(((start_pos), [start_pos]))

    # declare visited set to collect all visited node so as not to be checked again
    visited = set()         # set is a data structure that removes dublicate numbers


    # init the (BFS)     Algorithm
    while not q.empty():        # while queue not empty
        
        # get latest pair in the queue >>>>>> pair (currenct_pos, [path])
        current_pos, path = q.get()

        # print the maze with unique path
        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.refresh()
        time.sleep(0.2)
        # break currect_pos pair into row and column (cartasian coordinates)
        row, col = current_pos

        # if the coordination belongs to the end, return the path
        if maze[row][col] == end:
            return path
        
        

        # check all neighbors

        neighbors = find_all_neighbors(maze, row, col)

        for neighbor in neighbors:
            r, c = neighbor


            # continue if neigbor is already checked (in visited)
            if neighbor in visited:
                continue

            # coninue if neighbor is an obstacle
            if maze[r][c] == "#":
                continue

        
            # put this neighbor into the queue and add new path comprisd of old path + new node (neighbor)
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            
            # add this neighboring node to visited node so as it be checked
            visited.add(neighbor)
            
def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    find_shortest_path(maze, stdscr)
    stdscr.getch()


wrapper(main)