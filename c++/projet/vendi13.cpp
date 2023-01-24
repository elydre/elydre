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

int corect_jour(int jour_nom) {
    if (jour_nom == 7) {
        return 1;
    }
    else {
        return jour_nom + 1;
    }
}

string get_jour_str(int id) {
    string jours[7] = { "lundi", "mardi", "credi", "jeudi", "vendi", "samdi", "diche" };
    return jours[id - 1];
}

string get_mois_str(int id) {
    string mois[12] = { "janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre" };
    return mois[id];
}

int annee(int jm, bool bis, int nom_tofinf, int num_tofind, int print) {
    // print = 0: pas de print
    // print = 1: print des bon jours
    // print = 2: tt les print

    int jour_nom = jm;
    int compter = 0;
    int nb_jours[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
    if (bis) {
        nb_jours[1] = 29;
    }

    for (int mois = 0; mois < 12; mois++) {
        for (int jour_num = 1; jour_num <= nb_jours[mois]; jour_num++) {
            jour_nom = corect_jour(jour_nom);
            if (jour_nom == nom_tofinf && jour_num == num_tofind) {
                if (print == 1) {
                    cout << get_jour_str(jour_nom) << " " << jour_num << " " << get_mois_str(mois) << " (" << nb_jours[mois] << ") " << endl;
                }
                compter++;
            }
            if (print == 2) {
                cout << get_jour_str(jour_nom) << " " << jour_num << " " << get_mois_str(mois) << " (" << nb_jours[mois] << ") " << endl;
            }
        }
    }
    return compter;
}

int tester(int nom_tofind, int num_tofind, int debug) {
    int compter = 0;

    for (int sd = 0; sd < 7; sd++) {
        if (debug > 0) {
            cout << endl << "  [" << get_jour_str(sd + 1) << " non bissextile]" << endl;
        }
        compter += annee(sd, false, nom_tofind, num_tofind, debug);
        if (debug > 0) {
            cout << endl << "  [" << get_jour_str(sd + 1) << " bissextile]" << endl;
        }
        compter += annee(sd, true, nom_tofind, num_tofind, debug);
    }
    return compter;
}

int main()
{

    cout << tester(5, 13, 1) << endl;

}