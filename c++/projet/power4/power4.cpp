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

// pour le sleep
#include <chrono>
#include <thread>

// macro pour remonter une ligne et effacer
#define UP "\033[F"
#define CLEAR "\033[K"

using namespace std;

int grille[8][8] = { 0 };

char get_piont(int num) {
	if (num == 1) {
		return '@';
	}
	if (num == 2) {
		return 'X';
	}
	return ' ';
}

void print_grille() {
	cout << "   1   2   3   4   5   6   7   8\n\n";

	for (int l = 0; l < 8; l++) {
		for (int c = 0; c < 8; c++) {
			cout << " | " << get_piont(grille[c][l]);
		}
		cout << " |" << endl;
	}
	cout << endl;
}

void clear_all() {
	for (int x = 0; x < 14; x++) {
		cout << UP << CLEAR;
	}
}

int get_user_choix() {
	int inp;

	clear_all();
	print_grille();

	cout << "SAISIR LA COLONNE -> ";
	while (1) {
		cin >> inp;
		cin.ignore();

		inp--;

		clear_all();
		print_grille();

		if (inp < 8 && inp >= 0 && grille[inp][0] == 0) {
			cout << "DONE!";
			return inp;
		}
		else {
			cout << "CASE NON VALIDE! -> ";
		}
	}
}

void chute(int colonne) {

	for (int l = 0; l < 7; l++) {
		if (grille[colonne][l] > 0 && grille[colonne][l + 1] == 0) {
			grille[colonne][l + 1] = grille[colonne][l];
			grille[colonne][l] = 0;
			clear_all();
			print_grille();
			this_thread::sleep_for(chrono::milliseconds(100));
		}
	}
}

int check_eg(int v1, int v2, int v3, int v4) {
	if (v1 == v2 && v1 == v3 && v1 == v4) {
		return v1;
	}
	return 0;
}

int is_gagnant(int tab[8][8]) {

	// ligne & colonnes

	for (int c = 0; c < 8; c++) {
		for (int l = 0; l < 5; l++) {
			if (check_eg(tab[c][l], tab[c][l + 1], tab[c][l + 2], tab[c][l + 3]) > 0) {
				return 1;
			}
			if (check_eg(tab[l][c], tab[l + 1][c], tab[l + 2][c], tab[l + 3][c]) > 0) {
				return 2;
			}
		}
	}

	// diagonales

	for (int c = 0; c < 5; c++) {
		for (int l = 0; l < 5; l++) {
			if (check_eg(tab[c][l], tab[c + 1][l + 1], tab[c + 2][l + 2], tab[c + 3][l + 3]) > 0) {
				return 3;
			}
			if (check_eg(tab[l +3 ][c], tab[l + 2][c + 1], tab[l + 1][c + 2], tab[l][c + 3]) > 0) {
				return 4;
			}
		}
	}
	return 0;
}

class IA {
private:
	int grille_test[8][8] = { 0 };

	void vute(int colonne) {
		for (int l = 0; l < 7; l++) {
			if (grille_test[colonne][l] > 0 && grille_test[colonne][l + 1] == 0) {
				grille_test[colonne][l + 1] = grille_test[colonne][l];
				grille_test[colonne][l] = 0;
			}
		}
	}

	void push_grille(int g[8][8]) {
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				grille_test[i][j] = grille[i][j];
			}
		}
	}

	int cp_gagnant(int joueur) {
		for (int c = 0; c < 8; c++) {
			push_grille(grille);
			grille_test[c][0] = joueur;
			vute(c);
			if (is_gagnant(grille_test) > 0) {
				return c;
			}
		}
		return -1;
	}

public:
	int play() {
		int val;
		val = cp_gagnant(2);
		if (val >= 0) {
			return val;
		}
		val = cp_gagnant(1);
		if (val >= 0) {
			return val;
		}
		while (1) {
			val = rand() % 10 - 1;
			if (val < 8 && val >= 0 && grille[val][0] == 0) {
				return val;
			}
		}
	}
};

int main() {
	bool tour = 0;
	int colonne;
	IA joueur2;

	while (1) {
		print_grille();

		if (!tour) {
			colonne = get_user_choix();
		}
		else {
			colonne = joueur2.play();
		}

		grille[colonne][0] = tour + 1;

		chute(colonne);

		if (is_gagnant(grille) > 0) {
			break;
		}

		clear_all();

		tour = !tour;
	}
	cout << "Bravo joueur " << get_piont(tour + 1) << " vous avec gagner avec une ";
	if (is_gagnant(grille) == 1) {
		cout << "colonne!\n";
	}
	else if (is_gagnant(grille) == 2) {
		cout << "ligne!\n";
	}
	else {
		cout << "diagonale!\n";
	}
}