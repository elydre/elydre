#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <fcntl.h>

void test_ungetc(void) {
    const char *fname = "t_ungetc_mix.tmp";

    {
        FILE *fw = fopen(fname, "wb");
        assert(fw);
        const char *data = "ABCDE";
        assert(fwrite(data, 1, strlen(data), fw) == strlen(data));
        fclose(fw);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(f);
        int c1 = fgetc(f);
        assert(c1 == 'A');
        int r = ungetc('Z', f);
        assert(r == 'Z');
        int c2 = fgetc(f);
        assert(c2 == 'Z');
        int c3 = fgetc(f);
        assert(c3 == 'B');
        fclose(f);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(f);
        assert(fgetc(f) == 'A');
        assert(ungetc('Y', f) == 'Y');
        char buf[8] = {0};
        size_t n = fread(buf, 1, 3, f);
        assert(n == 3);
        assert(memcmp(buf, "YBC", 3) == 0);
        fclose(f);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(f);
        fseek(f, 2, SEEK_SET);
        assert(fgetc(f) == 'C');
        assert(ungetc('X', f) == 'X');
        char buf[8];
        char *s = fgets(buf, sizeof(buf), f);
        assert(s == buf);

        assert(strncmp(buf, "XDE", 4) == 0);
        fclose(f);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(f);
        fseek(f, 4, SEEK_SET);
        int c1 = fgetc(f);
        assert(c1 == 'E');
        assert(feof(f) == 0);
        assert(ungetc('Q', f) == 'Q');
        assert(feof(f) == 0);

        fseek(f, -1, SEEK_CUR);
        int c2 = fgetc(f);
        assert(c2 == 'D');
        fclose(f);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(f);
        fgetc(f);

        assert(ungetc('1', f) == '1');
        int ret2 = ungetc('2', f);
        int ret3 = ungetc('3', f);

        int c;
        int count = 0;
        char out[8] = {0};

        while ((c = fgetc(f)) != EOF && count < 8) {
            out[count++] = (char)c;
        }

        out[count] = '\0';

        if (ret3 == EOF || ret2 == EOF) {
            printf("Note: standard posix ungetc\n");
            assert(out[0] == '1');
        } else {
            printf("Note: multiple ungetc supported (GNU style)\n");
            assert(strncmp(out, "321", 3) == 0);
        }

        fclose(f);
    }

    {
        FILE *f = fopen(fname, "rb");
        assert(fgetc(f) == 'A');
        assert(ungetc('Z', f) == 'Z');
        char buf[8] = {0};
        size_t n = fread(buf, 2, 2, f); // lire 2 elements de 2 octets
        assert(n == 2);
        assert(memcmp(buf, "ZBCD", 4) == 0);
        fclose(f);
    }

    remove(fname);
    printf("[ -- OK -- ] test_ungetc passed\n");
}

void test_unistd_interact(void) {
    const char *fname = "t_stdio_posix.tmp";
    const char *msg1 = "ABC";
    const char *msg2 = "DEF";
    
    int fd = open(fname, O_CREAT | O_TRUNC | O_RDWR, 0644);
    assert(fd >= 0);

    FILE *f = fdopen(fd, "r+");
    assert(f);
    
    size_t w = fwrite(msg1, 1, 3, f);
    assert(w == 3);
    
    assert(fflush(f) == 0);
    
    off_t o = lseek(fd, 0, SEEK_SET);
    assert(o == 0);

    char buf[16] = {0};
    ssize_t n = read(fd, buf, 3);
    assert(n == 3);
    assert(memcmp(buf, "ABC", 3) == 0);
    
    assert(lseek(fd, 3, SEEK_SET) == 3);
    ssize_t wn = write(fd, msg2, 3);
    assert(wn == 3);
    
    assert(fseek(f, 0, SEEK_SET) == 0);

    char buf2[8] = {0};
    size_t rd = fread(buf2, 1, 6, f); 
    assert(rd == 6);
    assert(memcmp(buf2, "ABCDEF", 6) == 0);

    fclose(f);
    
    unlink(fname);
    printf("[ -- OK -- ] test_unistd_interact passed\n");
}


int main(void) {
    test_ungetc();
    test_unistd_interact();
    return 0;
}
