#include "../includes/so_long.h"
#include <syscall.h>

typedef struct {
    void *mlx;

    void *func_loop;
    void *loop_param;

    void *func_key;
    void *key_param;

    uint32_t *win;
    uint32_t x;
    uint32_t y;
} mlx_t;

typedef struct {
    uint32_t *img;
    uint32_t x;
    uint32_t y;
} img_t;

int	mlx_destroy_display(void *mlx_ptr) {
    // free(mlx_ptr);
    return 0;
}

void i_manage_kb(mlx_t *mlx) {
    int sc = c_kb_get_scfh();
    if (!sc) return;
    if (sc > 127) return;
    switch (sc) {
        case KB_LEFT:
            sc = KEY_LEFT;
            break;
        case KB_RIGHT:
            sc = KEY_RIGHT;
            break;
        case KB_OLDER:
            sc = KEY_UP;
            break;
        case KB_NEWER:
            sc = KEY_DOWN;
            break;
        case KB_ESC:
            sc = KEY_ESC;
            break;
        case 30:
            sc = KEY_A;
            break;
        case 32:
            sc = KEY_D;
            break;
        case 31:
            sc = KEY_S;
            break;
        case 17:
            sc = KEY_W;
            break;
        case KB_CTRL:
            sc = ATTACK;
            break;
        default:
            sc = 0;
            break;
    }
    if (sc)
        ((int (*)(int, void *)) mlx->func_key)(sc, mlx->key_param);
}

void editmlx_sleep(void *mlx_ptr, int us) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;

    us = us / 1000;
    int start = c_timer_get_ms();
    while (c_timer_get_ms() - start < us) {
        i_manage_kb(mlx);
        usleep(1000);
    }
}

int	mlx_destroy_window(void *mlx_ptr, void *win_ptr) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    free(mlx->win);
    return 0;
}

int	mlx_destroy_image(void *mlx_ptr, void *img_ptr) {
    img_t *img = (img_t *) img_ptr;
    free(img->img);
    free(img);
    return 0;
}

int	mlx_string_put(void *mlx_ptr, void *win_ptr, int x, int y, int color, char *string) {
    return 0;
}

int	mlx_hook(void *win_ptr, int x_event, int x_mask, int (*funct)(), void *param) {
    return 0;
}

int	mlx_key_hook(void *win_ptr, int (*funct_ptr)(), void *param) {
    mlx_t *mlx = (mlx_t *) win_ptr;
    mlx->func_key = funct_ptr;
    mlx->key_param = param;
    return 0;
}

/*
# define KEY_W 119
# define KEY_A 97
# define KEY_S 115
# define KEY_D 100
# define KEY_ESC 65307

# define KEY_UP 65362
# define KEY_DOWN 65364
# define KEY_LEFT 65361
# define KEY_RIGHT 65363
*/


int	mlx_loop(void *mlx_ptr) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    int sc;

    while (mlx->func_loop) {
        ((int (*)(void *)) mlx->func_loop)(mlx->loop_param);
        i_manage_kb(mlx);
    }
    return 0;
}

void *mlx_new_window(void *mlx_ptr, int size_x, int size_y, char *title) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    mlx->x = size_x;
    mlx->y = size_y;

    mlx->win = calloc(size_x * size_y, 4);

    return mlx;
}

int	mlx_loop_hook(void *mlx_ptr, int (*funct_ptr)(), void *param) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    mlx->func_loop = funct_ptr;
    mlx->loop_param = param;
    return 0;
}

/******************/

void *mlx_bmp_file_to_image(void *mlx_ptr, char *path, int *w_ptr, int *h_ptr) {
    // check if file exists
    FILE *file = fopen(path, "rb");
    if (!file) {
        printf("File %s not found\n", path);
        return NULL;
    }
    
    // open file
    fseek(file, 0, SEEK_END);
    int file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    uint8_t *file_content = malloc(file_size);
    fread(file_content, 1, file_size, file);
    fclose(file);

    // check if file is a bmp
    if (file_content[0] != 'B' || file_content[1] != 'M') {
        free(file_content);
        printf("File %s is not a bmp\n", path);
        return NULL;
    }

    // get image data
    int width = *(int *)(file_content + 18);
    int height = *(int *)(file_content + 22);
    int offset = *(int *)(file_content + 10);
    int size = *(int *)(file_content + 34);
    uint8_t *data = file_content + offset;

    if (width <= 0 || height <= 0) {
        free(file_content);
        printf("File %s has invalid dimensions\n", path);
        return NULL;
    }

    int factor = size / (width * height);

    // copy image data to buffer
    if (factor != 3 && factor != 4) {
        free(file_content);
        printf("File %s has invalid pixel format\n", path);
        return NULL;        
    }

    uint32_t *output = malloc(width * height * sizeof(uint32_t));

    int k;
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) { 
            k = width - i - 1;
            uint32_t color = data[(j * width + i) * factor] |
                            (data[(j * width + i) * factor + 1] << 8) |
                            (data[(j * width + i) * factor + 2] << 16);

            if (factor == 4 && data[(j * width + i) * factor + 3] == 0) continue;
            output[width * height - (k + j * width + 1)] = color;
        }
    }

    free(file_content);
    
    // create image
    img_t *img = malloc(sizeof(img_t));
    img->img = output;
    img->x = width;
    img->y = height;

    *w_ptr = width;
    *h_ptr = height;

    return img;
}

int	mlx_put_image_to_window(void *mlx_ptr, void *win_ptr, void *img_ptr, int x, int y) {
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    img_t *img = (img_t *) img_ptr;
    uint32_t *fb = c_vesa_get_fb();
    uint32_t pitch = c_vesa_get_pitch();

    for (int i = 0; i < img->y; i++) {
        for (int j = 0; j < img->x; j++) {
            fb[(y + i) * pitch + x + j] = img->img[i * img->x + j];
        }
    }
    return 0;
}

char *mlx_get_data_addr(void *img_ptr, int *bits_per_pixel, int *size_line, int *endian) {
    img_t *img = (img_t *) img_ptr;
    *bits_per_pixel = 32;
    *size_line = img->x * 4;
    *endian = 0;
    return (char *) img->img;
}

int	mlx_do_sync(void *mlx_ptr) {
    return 0;
    mlx_t *mlx = (mlx_t *) mlx_ptr;
    uint32_t *fb = c_vesa_get_fb();
    uint32_t pitch = c_vesa_get_pitch();

    int pos = -1;
    for (int i = 0; i < mlx->y; i++) {
        for (int j = 0; j < mlx->x; j++) {
            pos++;
            fb[i * pitch + j] = mlx->win[pos];
        }
    }
            
    return 0;
}

void *mlx_init(void) {
    mlx_t *mlx = malloc(sizeof(mlx_t));
    mlx->mlx = mlx;

    mlx->func_loop = 0;
    mlx->loop_param = 0;

    mlx->func_key = 0;
    mlx->key_param = 0;

    mlx->win = 0;
    mlx->x = 0;
    mlx->y = 0;

    return mlx;
}

/*******************/
