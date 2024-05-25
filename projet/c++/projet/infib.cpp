#include <iostream>
#include <vector>
using namespace std;

class Infi {
private:
    vector<int> liste{ 0 };

    bool check_retenu() {
        for (int i = 0; i < liste.size(); i++) {
            if (liste[i] > 9) {
                return 0;
            }
        }
        return 1;
    }


public:
    int get_int(int id) {
        return liste[id];
    }

    void retenu() {
        while (!check_retenu()) {
            for (int i = 0; i < liste.size(); i++) {
                if (liste[i] < 10) {
                    continue;
                }
                if (i + 1 >= liste.size()) {
                    liste.push_back(0);
                }
                liste[i + 1] += liste[i] / 10;
                liste[i] = liste[i] % 10;
            }
        }
    }

    int get_size() {
        return liste.size();
    }

    void add(Infi nb2) {
        for (int i = 0; i < nb2.get_size(); i++) {
            if (i >= liste.size()) {
                liste.push_back(0);
            }
            liste[i] += nb2.get_int(i);
        }
        retenu();
    }

    void egal(Infi nb2) {
        for (int i = 0; i < liste.size(); i++) {
            liste.clear();
        }
        liste.push_back(0);
        add(nb2);
    }

    void push_int(int num, int id) {
        liste[id] = num;
        retenu();
    }

    void print() {
        for (int i = liste.size(); i > 0; i--) {
            cout << liste[i - 1];
        }
        cout << endl;
    }
};

int main() {
    Infi n1;
    n1.push_int(1, 0);
    n1.print();

    Infi n2;
    n2.push_int(2, 0);
    n2.print();

    Infi temp;
    temp.push_int(0, 0);

    while (true) {
        temp.egal(n2);
        n2.add(n1);
        n1.egal(temp);
        n2.print();
    }
}