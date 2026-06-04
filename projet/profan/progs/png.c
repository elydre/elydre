// @LINK: libpng16, libpf

#include <stdio.h>
#include <stdlib.h>
#include <png.h>
#include <unistd.h>

#include <profan/syscall.h>
#include <profan/math.h>
#include <profan.h>

#define PIXEL_AT(x, y) (rows[y][x * 4 + 0] << 16 | rows[y][x * 4 + 1] << 8 | rows[y][x * 4 + 2] << 0 | rows[y][x * 4 + 3] << 24)

#define BLEND_COLOR(src_color, strength) \
    ((uint32_t)(((((src_color) >> 16) & 0xFF) * (strength))) << 16 | \
     (uint32_t)((((src_color) >> 8) & 0xFF) * (strength)) << 8 | \
     (uint32_t)((((src_color) >> 0) & 0xFF) * (strength)) << 0 | \
     (uint32_t)((((src_color) >> 24) & 0xFF) * (strength)) << 24)

void display_zoom(png_bytep *rows, png_uint_32 width, png_uint_32 height, double zoom)
{
    uint32_t *framebuffer = syscall_vesa_fb();
    uint32_t fb_width = syscall_vesa_width();
    uint32_t fb_height = syscall_vesa_height();
    uint32_t fb_pitch = syscall_vesa_pitch();

    // full black background
    for (uint32_t y = 0; y < fb_height; y++)
        for (uint32_t x = 0; x < fb_width; x++)
            framebuffer[y * fb_pitch + x] = 0x000000;

    uint32_t zoomed_width = (uint32_t)(width * zoom);
    uint32_t zoomed_height = (uint32_t)(height * zoom);

    for (uint32_t y = 0; y < zoomed_height && y < fb_height; y++) {
        for (uint32_t x = 0; x < zoomed_width && x < fb_width; x++) {
            double src_x = x / zoom;
            double src_y = y / zoom;

            int x_color1 = floor(src_x);
            int x_color2 = floor(src_x + 1);

            if (x_color1 < 0)
                x_color1 = 0;
            if (x_color2 >= (int) width)
                x_color2 = width - 1;

            double x_color2_strength = src_x - floor(src_x);
            double x_color1_strength = 1.0 - x_color2_strength;

            int y_color1 = floor(src_y);
            int y_color2 = floor(src_y + 1);

            if (y_color1 < 0)
                y_color1 = 0;
            if (y_color2 >= (int) height)
                y_color2 = height - 1;

            double y_color2_strength = src_y - floor(src_y);
            double y_color1_strength = 1.0 - y_color2_strength;

            uint32_t colors[4] = {0};

            colors[0] = BLEND_COLOR(PIXEL_AT(x_color1, y_color1), x_color1_strength * y_color1_strength);
            colors[1] = BLEND_COLOR(PIXEL_AT(x_color2, y_color1), x_color2_strength * y_color1_strength);
            colors[2] = BLEND_COLOR(PIXEL_AT(x_color1, y_color2), x_color1_strength * y_color2_strength);
            colors[3] = BLEND_COLOR(PIXEL_AT(x_color2, y_color2), x_color2_strength * y_color2_strength);

            uint32_t r = ((colors[0] >> 16) & 0xFF) + ((colors[1] >> 16) & 0xFF) + ((colors[2] >> 16) & 0xFF) + ((colors[3] >> 16) & 0xFF);
            uint32_t g = ((colors[0] >> 8) & 0xFF) + ((colors[1] >> 8) & 0xFF) + ((colors[2] >> 8) & 0xFF) + ((colors[3] >> 8) & 0xFF);
            uint32_t b = ((colors[0] >> 0) & 0xFF) + ((colors[1] >> 0) & 0xFF) + ((colors[2] >> 0) & 0xFF) + ((colors[3] >> 0) & 0xFF);

            framebuffer[y * fb_pitch + x] = (r << 16) | (g << 8) | b;
        }
    }
}

void interactrive(png_bytep *rows, png_uint_32 width, png_uint_32 height)
{
    double zoom = 1.0;
    display_zoom(rows, width, height, zoom);

    while (1)
    {
        int kb = syscall_sc_get();

        if (kb == KB_TOP)
            zoom += 0.1;
        else if (kb == KB_BOT)
            zoom -= 0.1;
        else if (kb == KB_ESC)
            break;
        else {
            usleep(10000);
            continue;
        }

        if (zoom < 0.1)
            zoom = 0.1;

        display_zoom(rows, width, height, zoom);
    }
}

int afficherPNG(const char *filename)
{
    FILE *fp = fopen(filename, "rb");
    if (!fp)
    {
        perror("fopen");
        return -1;
    }

    png_structp png = png_create_read_struct(
        PNG_LIBPNG_VER_STRING,
        NULL, NULL, NULL);

    if (!png)
    {
        fclose(fp);
        return -1;
    }

    png_infop info = png_create_info_struct(png);

    if (!info)
    {
        png_destroy_read_struct(&png, NULL, NULL);
        fclose(fp);
        return -1;
    }

    if (setjmp(png_jmpbuf(png)))
    {
        png_destroy_read_struct(&png, &info, NULL);
        fclose(fp);
        return -1;
    }

    png_init_io(png, fp);
    png_read_info(png, info);

    png_uint_32 width  = png_get_image_width(png, info);
    png_uint_32 height = png_get_image_height(png, info);

    int color_type = png_get_color_type(png, info);
    int bit_depth  = png_get_bit_depth(png, info);

    /* Conversions vers RGBA 8 bits */

    if (bit_depth == 16)
        png_set_strip_16(png);

    if (color_type == PNG_COLOR_TYPE_PALETTE)
        png_set_palette_to_rgb(png);

    if (color_type == PNG_COLOR_TYPE_GRAY &&
        bit_depth < 8)
        png_set_expand_gray_1_2_4_to_8(png);

    if (png_get_valid(png, info, PNG_INFO_tRNS))
        png_set_tRNS_to_alpha(png);

    if (color_type == PNG_COLOR_TYPE_GRAY ||
        color_type == PNG_COLOR_TYPE_GRAY_ALPHA)
        png_set_gray_to_rgb(png);

    if (!(color_type & PNG_COLOR_MASK_ALPHA))
        png_set_add_alpha(
            png, 0xFF,
            PNG_FILLER_AFTER);

    png_read_update_info(png, info);

    png_bytep *rows =
        malloc(sizeof(png_bytep) * height);

    if (!rows)
    {
        png_destroy_read_struct(&png, &info, NULL);
        fclose(fp);
        return -1;
    }

    int rowbytes =
        png_get_rowbytes(png, info);

    for (png_uint_32 y = 0; y < height; y++)
    {
        rows[y] = malloc(rowbytes);

        if (!rows[y])
        {
            while (y--)
                free(rows[y]);

            free(rows);

            png_destroy_read_struct(
                &png, &info, NULL);

            fclose(fp);
            return -1;
        }
    }

    png_read_image(png, rows);

    interactrive(rows, width, height);

    for (png_uint_32 y = 0; y < height; y++)
        free(rows[y]);

    free(rows);

    png_destroy_read_struct(
        &png, &info, NULL);

    fclose(fp);

    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <file.png>\n", argv[0]);
        return EXIT_FAILURE;
    }

    if (afficherPNG(argv[1]) != 0)
    {
        fprintf(stderr, "Failed to display PNG image.\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
