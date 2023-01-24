import mod.sudok as sdk

sdk.set_time_out(2)

while True:
    grille_full = sdk.gen_empty_grid()
    sdk.file_empty(grille_full)

    grille_empty = sdk.make_holes(grille_full, 50)

    sdk.solve_sudoku(grille_empty)
