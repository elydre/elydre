import mod.sudok as sdk

TIMEOUT = 10 # in seconds
sdk.set_time_out(TIMEOUT)

grille_empty = [
    [0, 0, 2, 0, 3, 0, 0, 0, 5],
    [0, 8, 0, 0, 0, 0, 0, 4, 7],
    [7, 4, 0, 1, 8, 0, 6, 0, 2],
    [3, 0, 0, 7, 0, 6, 0, 5, 1],
    [8, 0, 0, 9, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 8, 0, 3, 4],
    [0, 9, 6, 0, 0, 4, 7, 0, 0],
    [5, 1, 0, 2, 0, 9, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 0, 0],
]

sdk.solve_sudoku(grille_empty)
