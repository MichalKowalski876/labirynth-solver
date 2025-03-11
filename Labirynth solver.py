import random
import json
import pygame
import time


def get_maze():
    fh = open("maze_base.json")
    maze = json.load(fh)

    for row in range(len(maze)):
        for item in range(len(maze[row])):
            if type(item) == int:
                maze[row][item] = str(maze[row][item])

    return maze


def cur_position(point_of_interest):
    x = 0
    pos = []
    for row in maze_1:
        if point_of_interest in row:
            pos.append(x)
            pos.append(maze_1[x].index(point_of_interest))
            break
        x += 1

    return pos


def show_res():
    maze = get_maze()

    for coordinates in path:
        for num in coordinates:
            maze[coordinates[0]][coordinates[1]] = "*"

    maze[path[0][0]][path[0][1]] = "X"
    gui(maze, False, "Solution found", "green")


def gui(maze, fin, res, color):
    maze_tbd = []
    white = (232, 232, 232)

    if color == "green":
        rez_col = (32, 230, 62)
    elif color == "red":
        rez_col = (214, 36, 24)
    else:
        rez_col = (232, 232, 232)

    for row in maze:
        draw = ""
        for item in row:
            item = item.replace("1", "█")
            item = item.replace("0", " ")
            draw += item
        maze_tbd.append(draw)

    pygame.init()
    pygame.font.init()
    background = pygame.color.Color("#292828")
    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption("LABYRINTH SOLVER")
    text_font = pygame.font.SysFont("monospace", 25)

    screen.fill(background)

    x_axis = 75
    res_txt = text_font.render(res, True, rez_col)
    screen.blit(res_txt, res_txt.get_rect(center=(1000 // 2, x_axis - 35)))

    for item in maze_tbd:
        text_tbd = text_font.render(item, True, white)
        item_rect = text_tbd.get_rect(center=(1000 // 2, x_axis))
        screen.blit(text_tbd, item_rect)
        x_axis += 25

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.flip()

        if fin:
            break


def data_change(pos, new_pos):
    time.sleep(.1)
    maze_1[pos[0]][pos[1]] = "*"
    maze_1[new_pos[0]][new_pos[1]] = "X"
    gui(maze_1, True, "Searching for path", "")


def move(pos):
    possibilities = []
    try:
        possibilities = [(pos[0], pos[1] + 1),  # right
                         (pos[0], pos[1] - 1),  # left
                         (pos[0] + 1, pos[1]),  # down
                         (pos[0] - 1, pos[1])]  # up
    except ImportError:
        gui(maze_1, False, "No start found", "red")

    random.shuffle(possibilities)

    for item in possibilities:
        if maze_1[item[0]][item[1]] == "G":
            path.append(pos)
            show_res()
        elif maze_1[item[0]][item[1]] == "0":
            path.append(pos)
            data_change(pos, item)
            break
    else:
        if len(path) == 0:
            gui(maze_1, False, "labyrinth invalid, no solution found", "red")
        else:
            data_change(pos, path[-1])
            path.remove(path[-1])


def main():
    if not cur_position("G"):
        gui(maze_1, False, "No goal found", "red")

    while True:
        move(cur_position("X"))


path = []
maze_1 = get_maze()
main()
