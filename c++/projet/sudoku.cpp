/*     _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________

 - codé en : UTF-8
 - langage : c++
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
*/

#include <iostream>
using namespace std;

void print_sudoku(int grille[9][9]) {
	cout << "\n";
	for (int y = 0; y < 9; y++) {
		cout << "   ";
		for (int x = 0; x < 9; x++) {
			if (x % 3 == 0 && x != 0) {
				cout << "| ";
			}

			if (grille[x][y] > 0) {
				cout << grille[x][y] << " ";
			}
			else {
				cout << ". ";
			}
		}
		cout << "\n";
		if (y % 3 == 2 && y != 8) {
			cout << "   ------+-------+------\n";
		}
	}
}

void one_line_print(int grille[9][9]) {
	for (int y = 0; y < 9; y++) {
		for (int x = 0; x < 9; x++) {
			cout << grille[x][y];
		}
	}
	cout << endl;
}

bool chek_grille(int grille[9][9], bool full) {
	if (full) {
		for (int y = 0; y < 9; y++) {
			for (int x = 0; x < 9; x++) {
				if (grille[x][y] == 0) {
					return 0;
				}
			}
		}
	}

	for (int y = 0; y < 9; y++) {
		for (int x = 0; x < 9; x++) {
			if (grille[x][y] != 0) {
				for (int a = 0; a < 9; a++) {
					// orizontale
					if (a != x && grille[x][y] == grille[a][y]) {
						return 0;
					}
					// verticale
					if (a != y && grille[x][y] == grille[x][a]) {
						return 0;
					}
				}
			}
		}
	}

	// 3x3
	for (int ny = 0; ny < 9; ny += 3) {
		for (int nx = 0; nx < 9; nx += 3) {
			for (int y = ny; y < ny + 3; y++) {
				for (int x = nx; x < nx + 3; x++) {
					if (grille[x][y] != 0) {
						for (int a = nx; a < nx + 3; a++) {
							for (int b = ny; b < ny + 3; b++) {
								if (a != x && b != y && grille[x][y] == grille[a][b]) {
									return 0;
								}
							}
						}
					}
				}
			}
		}
	}

	return 1;
}

bool test_grille(int grille[9][9], int x, int y) {
	int g[9][9] = {0};
	int next_x = x + 1;
	int next_y = y;
	
	if (chek_grille(grille, 1)) {
		print_sudoku(grille);
		return 1;
	}


	if (next_x == 9) {
		next_x = 0;
		next_y++;
		if (next_y == 9 && next_x == 1) {
			cout << "IMPOSSIBLEEEEEEEEEEEEE" << endl;
			return 1;
		}
	}

	for (int b = 0; b < 9; b++) {
		for (int a = 0; a < 9; a++) {
			g[a][b] = grille[a][b];
		}
	}

	// one_line_print(g);

	if (grille[x][y] == 0) {
		for (int i = 1; i <= 9; i++) {
			g[x][y] = i;
			if (chek_grille(g, 0)) {
				if (test_grille(g, next_x, next_y)) {
					return 1;
				}
			}
		}
	}
	else {
		if (test_grille(g, next_x, next_y)) {
			return 1;
		}
	}
	return 0;
}

void start_sudoku(int grille[9][9]) {
	int s[9][9] = { 0 };
	for (int a = 0; a < 9; a++) {
		for (int b = 0; b < 9; b++) {
			s[a][b] = grille[b][a];
		}
	}
	cout << test_grille(s, 0, 0) << endl;
}

int main()
{
	int grille[9][9] = {
		{8,0,0, 0,0,0, 0,0,0},
		{0,0,3, 6,0,0, 0,0,0},
		{0,7,0, 0,9,0, 2,0,0},

		{0,5,0, 0,0,7, 0,0,0},
		{0,0,0, 0,4,5, 7,0,0},
		{0,0,0, 1,0,0, 0,3,0},

		{0,0,1, 0,0,0, 0,6,8},
		{0,0,8, 5,0,0, 0,1,0},
		{0,9,0, 0,0,0, 4,0,0},
	};

	start_sudoku(grille);
}