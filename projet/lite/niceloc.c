#include <stdlib.h>
#include <stdio.h>

typedef struct {
    void **ptrs;
    int size;
} reg_t;

#define NEW_REG {NULL, 0}

void *registererd_malloc(reg_t *reg, int size) {
    void *ptr = malloc(size);
    if (ptr == NULL)
        return NULL;
    reg->ptrs = realloc(reg->ptrs, (reg->size + 1) * sizeof(void *));
    if (reg->ptrs == NULL) {
        free(ptr);
        return NULL;
    }
    reg->ptrs[reg->size++] = ptr;
    return ptr;
}


void free_all(reg_t *reg) {
    for (int i = 0; i < reg->size; i++) {
        printf("freeing %p\n", reg->ptrs[i]);
        free(reg->ptrs[i]);
    }
    free(reg->ptrs);
}

#define rmalloc(size) registererd_malloc(&reg, size)

int main() {
    reg_t reg = NEW_REG;
    
    int **p = rmalloc(sizeof(int **) * 10);
    for (int i = 0; i < 10; i++) {
        p[i] = rmalloc(sizeof(int *) * 10);
        for (int j = 0; j < 10; j++)
            p[i][j] = i * j;
    }

    rmalloc(sizeof(int) * 10);
    
    printf("%d\n", p[5][6]);    

    free_all(&reg);
    return 0;
}