#include <windows.h>
#include <iostream>
#include <cmath>

using namespace std;

// COLORREF COLOR = RGB(255, 255, 255);
// SetPixel(Hdc, i, j, COLOR);

long double func(long double x) {
    return 5/x;
}

void axes(HDC Hdc) {
    for (int i = 0; i < 667; i++) {
        COLORREF COLOR = RGB(255, 0, 0);
        SetPixel(Hdc, i, 333, COLOR);
        SetPixel(Hdc, 333, i, COLOR);
    }
}

int main()
{
    HWND Hcon = GetConsoleWindow();
    HDC Hdc = GetDC(Hcon);

    axes(Hdc);

    int COx = 0;
    int COy;
    double long y;
    for (double long x = -10; x < 10; x += 0.03) {
        y = func(x);
        COy = (int)(333 - y / 0.03);
        if (COy < 666) {
            COLORREF COLOR = RGB(255, 255, 255);
            SetPixel(Hdc, COx, COy, COLOR);
        }
        COx++;
    }

    ReleaseDC(Hcon, Hdc);
    while (1) {
        Sleep(10);
    }
    return 0;
}