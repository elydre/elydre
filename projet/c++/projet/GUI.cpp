#include <windows.h>
#include <iostream>

using namespace std;

// COLORREF COLOR = RGB(255, 255, 255);
// SetPixel(Hdc, i, j, COLOR);

int main()
{
    HWND Hcon = GetConsoleWindow();
    HDC Hdc = GetDC(Hcon);
    
    
    int MAX_ITERATION = 50;
    
    long double XMIN = -2;
    long double XMAX = 0.5;
    long double YMIN = -1.25;
    long double YMAX = 1.25;

    long double cx, cy, xn, yn, tmp_x, tmp_y;
    int n;

    int LARGEUR = 500;
    int HAUTEUR = 500;

    for (int y = 0; y < HAUTEUR; y++) {
        for (int x = 0; x < LARGEUR; x++) {
            cx = (x * (XMAX - XMIN) / LARGEUR + XMIN);
            cy = (y * (YMIN - YMAX) / HAUTEUR + YMAX);
            xn = 0;
            yn = 0;
            n = 0;
            while ((xn * xn + yn * yn) < 4 && n < MAX_ITERATION) {
                tmp_x = xn;
                tmp_y = yn;
                xn = tmp_x * tmp_x - tmp_y * tmp_y + cx;
                yn = 2 * tmp_x * tmp_y + cy;
                n++;
            }
            COLORREF COLOR = RGB((3 * n) % 256, (1 * n) % 256, (10 * n) % 256);
            SetPixel(Hdc, x, y, COLOR);
        }
    }
    
    ReleaseDC(Hcon, Hdc);
    while (1) { ; }
    return 0;
}