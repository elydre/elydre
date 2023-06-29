#include "syscall.h"

typedef struct Vertex2D_t {
    float x;
    float y;
} Vertex2D_t;

typedef struct Vertex3D_t {
    float x;
    float y;
    float z;
} Vertex3D_t;

typedef struct Color_t {
    int r;
    int g;
    int b;
} Color_t;

typedef struct Cube_t {
    Vertex3D_t center;
    float d;
    Vertex3D_t vertices[8];
    Color_t couleurs[36];
    int indices[36];
} Cube_t;

typedef struct depthBuffer_t {
    uint16_t *data;
    int width;
    int height;
} depthBuffer_t;

void fillTriangle(depthBuffer_t depthBuffer, Vertex2D_t v0, Vertex2D_t v1, Vertex2D_t v2, Color_t c0, Color_t c1, Color_t c2, float z0, float z1, float z2);
int depthBuffer_t_test(depthBuffer_t depthBuffer, int x, int y, uint16_t v);
void depthBuffer_t_set(depthBuffer_t depthBuffer, int x, int y, uint16_t v);
float depthBuffer_t_get(depthBuffer_t depthBuffer, int x, int y);
float crossProduct(Vertex2D_t v0, Vertex2D_t v1, Vertex2D_t v2);
depthBuffer_t depthBuffer_t_init(int height, int width);
void rotate(Cube_t item, Vertex3D_t axis, int angle);
void depthBuffer_t_clear(depthBuffer_t depthBuffer);
Cube_t Cube_t_init(Vertex3D_t position, float size);
Vertex2D_t Vertex2D_t_project(Vertex3D_t vector);
void translate(Cube_t item, Vertex3D_t v);
int rgb_to_6bits(int r, int g, int b);
float max(float a, float b, float c);
float min(float a, float b, float c);
int floor(float value);
int ceil(float num);
float sin(int deg);
float cos(int deg);

int main(int arg) {

    c_fskprint("Lancement du moteur 3d !\n");

    Cube_t cube = Cube_t_init((Vertex3D_t) {0, 0, 0}, 100);

    rotate(cube, (Vertex3D_t) {0, 0, 1}, 135);
    rotate(cube, (Vertex3D_t) {1, 0, 0}, 45);

    depthBuffer_t depthBuffer = depthBuffer_t_init(c_vga_get_height(), c_vga_get_width());
    int Far = 100000;
    int Near = -100000;

    c_vga_320_mode();

    // on itère sur tout les triangles du cube
    for (int i = 0; i < 36; i+=3) {

        // on projette les points
        Vertex2D_t v0 = Vertex2D_t_project(cube.vertices[cube.indices[i]]);
        Vertex2D_t v1 = Vertex2D_t_project(cube.vertices[cube.indices[i+1]]);
        Vertex2D_t v2 = Vertex2D_t_project(cube.vertices[cube.indices[i+2]]);

        // on décale tout pour centrer au milieu du canvas
        v0.x+=c_vga_get_width()/2; v0.y+=c_vga_get_height()/2;
        v1.x+=c_vga_get_width()/2; v1.y+=c_vga_get_height()/2;
        v2.x+=c_vga_get_width()/2; v2.y+=c_vga_get_height()/2;

        // et enfin, on dessine notre triangle

        float z0 = (cube.vertices[cube.indices[i]].y - Near) / (Far - Near);
        float z1 = (cube.vertices[cube.indices[i+1]].y - Near) / (Far - Near);
        float z2 = (cube.vertices[cube.indices[i+2]].y - Near) / (Far - Near);

        fillTriangle(depthBuffer ,v0, v1, v2, cube.couleurs[i], cube.couleurs[i+1], cube.couleurs[i+2], z0, z1, z2);
    }

    while (1);

    c_vga_text_mode();

    return arg;
}

void rotate(Cube_t item, Vertex3D_t axis, int angle) {
    Vertex3D_t a = axis;
    float s = sin(angle);
    float c = cos(angle);
    float t = 1-c;
    float x = a.x;
    float y = a.y;
    float z = a.z;

    float r[3][3] = {
        { t*x*x + c,   t*x*y - s*z, t*x*z + s*y },
        { t*x*y + s*z, t*y*y + c,   t*y*z - s*x },
        { t*x*z - s*y, t*y*z + s*x, t*z*z + c   }
    };

    for (int i=0; i<8; i++) {
        Vertex3D_t p = item.vertices[i];
        float px = p.x - item.center.x;
        float py = p.y - item.center.y;
        float pz = p.z - item.center.z;

        float rp[3] = {
            r[0][0]*px + r[0][1]*py + r[0][2]*pz,
            r[1][0]*px + r[1][1]*py + r[1][2]*pz,
            r[2][0]*px + r[2][1]*py + r[2][2]*pz
        };

        item.vertices[i].x = rp[0] + item.center.x;
        item.vertices[i].y = rp[1] + item.center.y;
        item.vertices[i].z = rp[2] + item.center.z;
    }
}

void translate(Cube_t item, Vertex3D_t v) {
    item.center.x += v.x;
    item.center.y += v.y;
    item.center.z += v.z;

    for (int i=0; i<8; i++) {
        item.vertices[i].x += v.x;
        item.vertices[i].y += v.y;
        item.vertices[i].z += v.z;
    }
}

float power(float base, int exp) {
    if(exp < 0) {
        if(base == 0)
            return -0; // Error!!
        return 1 / (base * power(base, (-exp) - 1));
    }
    if(exp == 0)
        return 1;
    if(exp == 1)
        return base;
    return base * power(base, exp - 1);
}

int fact(int n) {
    return n <= 0 ? 1 : n * fact(n-1);
}

#define TERMS 7
#define PI 3.1415926535

float sin(int deg) {
    deg %= 360; // make it less than 360
    float rad = deg * PI / 180;
    float sin = 0;

    for(int i = 0; i < TERMS; i++) { // That's Taylor series!!
        sin += power(-1, i) * power(rad, 2 * i + 1) / fact(2 * i + 1);
    }
    return sin;
}

float cos(int deg) {
    deg %= 360; // make it less than 360
    float rad = deg * PI / 180;
    float cos = 0;

    for(int i = 0; i < TERMS; i++) { // That's also Taylor series!!
        cos += power(-1, i) * power(rad, 2 * i) / fact(2 * i);
    }
    return cos;
}

depthBuffer_t depthBuffer_t_init(int height, int width) {
    depthBuffer_t depthBuffer = {c_calloc(height*width*sizeof(uint16_t)), height, width};
    for (int i=0; i<height*width; i++) {
        depthBuffer.data[i] = 65535;
    }
    return depthBuffer;
}

void depthBuffer_t_clear(depthBuffer_t depthBuffer) {
    for (int i=0; i<depthBuffer.height*depthBuffer.width; i++) {
        depthBuffer.data[i] = (uint16_t) 65535;
    }
}

float depthBuffer_t_get(depthBuffer_t depthBuffer, int x, int y) {
    return ((uint16_t) depthBuffer.data[y * depthBuffer.width + x]) / 65535;
}

void depthBuffer_t_set(depthBuffer_t depthBuffer, int x, int y, uint16_t v) {
    depthBuffer.data[y * depthBuffer.width + x] = v * 65535;
}

int depthBuffer_t_test(depthBuffer_t depthBuffer, int x, int y, uint16_t v) {
    uint16_t value =  v * 65535;
    int index = depthBuffer.width * y + x;
    if (value < depthBuffer.data[index]) {
        depthBuffer.data[index] = value;
        return 1;
    }
    return 0;
}

Vertex2D_t Vertex2D_t_project(Vertex3D_t vector) {
    return (Vertex2D_t) {vector.x, vector.y};
}

Cube_t Cube_t_init(Vertex3D_t position, float size) {
    float d = size/2;
    return (Cube_t) {
        position,
        d, 
        {
            (Vertex3D_t) {position.x - d, position.y - d, position.z + d},
            (Vertex3D_t) {position.x - d, position.y - d, position.z - d},
            (Vertex3D_t) {position.x + d, position.y - d, position.z - d},
            (Vertex3D_t) {position.x + d, position.y - d, position.z + d},
            (Vertex3D_t) {position.x + d, position.y + d, position.z + d},
            (Vertex3D_t) {position.x + d, position.y + d, position.z - d},
            (Vertex3D_t) {position.x - d, position.y + d, position.z - d},
            (Vertex3D_t) {position.x - d, position.y + d, position.z + d}
        },
        {
            (Color_t) {255,0,0}, (Color_t) {255,0,0}, (Color_t) {255,0,0},
            (Color_t) {255,0,0}, (Color_t) {255,0,0}, (Color_t) {255,0,0},

            (Color_t) {255,255,0}, (Color_t) {0,255,255}, (Color_t) {255,0,255},
            (Color_t) {255,255,0}, (Color_t) {255,0,255}, (Color_t) {0,255,0},

            (Color_t) {0,0,255}, (Color_t) {0,0,255}, (Color_t) {0,0,255},
            (Color_t) {0,0,255}, (Color_t) {0,0,255}, (Color_t) {0,0,255},

            (Color_t) {255,255,0}, (Color_t) {255,255,0}, (Color_t) {255,255,0},
            (Color_t) {255,255,0}, (Color_t) {255,255,0}, (Color_t) {255,255,0},

            (Color_t) {255,0,255}, (Color_t) {255,0,255}, (Color_t) {255,0,255},
            (Color_t) {255,0,255}, (Color_t) {255,0,255}, (Color_t) {255,0,255},

            (Color_t) {0,255,255}, (Color_t) {0,255,255}, (Color_t) {0,255,255},
            (Color_t) {0,255,255}, (Color_t) {0,255,255}, (Color_t) {0,255,255}
        },
        {
            0,1,2,
            0,2,3,
            4,5,6,
            4,6,7,
            0,7,6,
            0,6,1,
            3,5,4,
            3,2,5,
            0,4,7,
            0,3,4,
            1,6,5,
            1,5,2
        }
    };
}

/*
crossProduct(v0,v1,v2) {
  return (v1.x - v0.x) * -(v2.y - v0.y) - -(v1.y - v0.y) * (v2.x - v0.x);
}*/

float crossProduct(Vertex2D_t v0, Vertex2D_t v1, Vertex2D_t v2) {
    return (float)((v1.x - v0.x) * -(v2.y - v0.y) - -((v1.y - v0.y) * (v2.x - v0.x)));
}

void fillTriangle(depthBuffer_t depthBuffer, Vertex2D_t v0, Vertex2D_t v1, Vertex2D_t v2, Color_t c0, Color_t c1, Color_t c2, float z0, float z1, float z2) {
    int minX = floor(min(v0.x, v1.x, v2.x));
    int maxX = ceil(max(v0.x, v1.x, v2.x));
    int minY = floor(min(v0.y, v1.y, v2.y));
    int maxY = ceil(max(v0.y, v1.y, v2.y));

    float area = crossProduct(v0, v1, v2);

    Vertex2D_t p = (Vertex2D_t) {0, 0};

    Color_t fragment = (Color_t) {0, 0, 0};

    for (int y = minY; y < maxY; y++) {
        for (int x = minX; x < maxX; x++) {
            p.x = x + 0.5; p.y = y + 0.5;

            float w0 = crossProduct(v1, v2, p);
            float w1 = crossProduct(v2, v0, p);
            float w2 = crossProduct(v0, v1, p);

            if (w0 < 0 || w1 < 0 || w2 < 0) {
                continue;
            }

            uint16_t depth = (w0 * z0 + w1 * z1 + w2 * z2) / area; 

            if (depthBuffer_t_test(depthBuffer, x, y, depth))
            fragment.r = (w0 * c0.r + w1 * c1.r + w2 * c2.r) / area;
            fragment.g = (w0 * c0.g + w1 * c1.g + w2 * c2.g) / area;
            fragment.b = (w0 * c0.b + w1 * c1.b + w2 * c2.b) / area;
            c_vga_put_pixel(x, y, rgb_to_6bits(fragment.r, fragment.g, fragment.b));
        }
    }

}

int floor(float value) {
    return (int)value;
}

int ceil(float num) {
    int inum = (int)num;
    if (num < 0 || num == (float)inum) {
        return inum;
    }
    return inum + 1;
}

float min(float a, float b, float c) {
    float liste[3] = {a, b, c};
    float mini = a;
    for (int i=0; i<3; i++) {
        if (liste[i] < mini) {
            mini = liste[i];
        }
    }
    return mini;
}

float max(float a, float b, float c) {
    float liste[3] = {a, b, c};
    float maxi = a;
    for (int i=0; i<3; i++) {
        if (liste[i] > maxi) {
            maxi = liste[i];
        }
    }
    return maxi;
}

int rgb_to_6bits(int r, int g, int b) {
    return (int) (g/64 << 4) + (r/64 << 2) + b/64;
}