import mod.colorprint as colorprint
from time import time
import itertools
import random

TIME_OUT = 2

def print_sudoku(grille, error):
    for y in range(9):
        print(end = "   ")
        for x in range(9):
            if x % 3 == 0 and x != 0:
                print(end = "| ")
            colorprint.colorprint(f"{grille[y][x] if grille[y][x] > 0 else '.'} ", "red" if error else "blue","k")
        print()
        if y % 3 == 2 and y != 8:
            print("   ------+-------+------")
    print()

def one_line_print(grille):
    for i, j in itertools.product(range(9), range(9)):
        print(end = str(grille[i][j]))
    print()


def chek_grille(grille, full):
    if full:
        for x, y in itertools.product(range(9), range(9)):
            if grille[y][x] == 0:
                return False

    for x, y in itertools.product(range(9), range(9)):
        if grille[y][x] != 0:
            for a in range(9):
                # horizontal
                if a != x and grille[y][a] == grille[y][x]:
                    return False
                # vertical
                if a != y and grille[a][x] == grille[y][x]:
                    return False

    # 3x3
    for x, y in itertools.product(range(0, 9, 3), range(0, 9, 3)):
        for a, b in itertools.product(range(3), range(3)):
            if grille[y + a][x + b] == 0:
                continue
            for c, d in itertools.product(range(3), range(3)):
                if a == c and b == d:
                    continue
                if grille[y + a][x + b] == grille[y + c][x + d]:
                    return False
    return True

def test_grille(grille, x, y):
    next_x = x + 1
    next_y = y

    if time() - debut > TIME_OUT: # time out
        return False

    if chek_grille(grille, 1):
        print_sudoku(grille, False)
        return True

    if next_y == 9 and next_x == 1:
        print("IMPOSSIBLEEEEEEEEEEEEE")
        return True

    if next_x == 9:
        next_x = 0
        next_y += 1

    # deep copy
    g = [i.copy() for i in grille]

    # one_line_print(g)

    if grille[x][y] == 0:
        for i in range(1, 10):
            g[x][y] = i
            if chek_grille(g, 0) and test_grille(g, next_x, next_y):
                return 1
    elif test_grille(g, next_x, next_y):
        return 1
    return 0

def file_empty(grid):
    # get the x and y of the first free cell
    for i, j in itertools.product(range(9), range(9)):
        if grid[i][j] == 0:
            x, y = i, j
            break

    # si la grille est full
    if chek_grille(grid, 1):
        return grid

    # list of possible values for the cell in a random order
    values = list(range(1, 10))
    random.shuffle(values)

    for i in values:
        grid[x][y] = i
        if chek_grille(grid, 0) and file_empty(grid):
            return grid

    grid[x][y] = 0
    return False

def gen_empty_grid():
    return [[0 for __ in range(9)] for _ in range(9)]

def make_holes(grid, nb):
    for _ in range(nb):
        x, y = random.randint(0, 8), random.randint(0, 8)
        if x == 0 and y in range(3):
            continue
        grid[x][y] = 0
    return grid

def set_time_out(time_out):
    global TIME_OUT
    TIME_OUT = time_out

def solve_sudoku(grille_empty):
    global debut
    debut = time()

    print_sudoku(grille_empty, False)
    if test_grille(grille_empty, 0, 0) == False:
        print_sudoku(grille_empty, True)
    print(f"Temps : {time() - debut}")
