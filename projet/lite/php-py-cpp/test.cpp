// interpreted and compiled by GLADE
#include <iostream>
using namespace std;
int main()
{
    long long int a;  // auto var
    a = 0;
    while (true)
    {
        a++;
        if (a % 100000 == 0)
        {
            cout << a << endl;
        }
    }
}