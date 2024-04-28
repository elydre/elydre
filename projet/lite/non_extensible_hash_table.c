#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

typedef struct {
    const char *key;
    const char *data;
    uint32_t hash;
    void *next;
} hash_t;

typedef struct {
    hash_t *table;
    int size;
} hash_table_t;

uint32_t hash(const char *str) {
    uint32_t hash = 0;
    for (int i = 0; str[i]; i++) {
        hash = (hash << 5) + str[i];
    }
    return hash;
}

hash_table_t hash_it(char **key, char **data, int size) {
    hash_t *table = calloc(size, sizeof(hash_t));
    hash_t *later = calloc(size, sizeof(hash_t));
    int later_index = 0;

    for (int i = 0; i < size; i++) {
        uint32_t h = hash(key[i]) % size;
        if (!table[h].data) {
            table[h].data = data[i];
            table[h].key = key[i];
            table[h].hash = h;
        } else {
            later[later_index].data = data[i];
            later[later_index].key = key[i];
            later[later_index].hash = h;
            later_index++;
        }
    }

    int table_index = 0;
    for (int i = 0; i < later_index; i++) {
        uint32_t h = later[i].hash;
        hash_t *entry = &table[h];

        while (table[table_index].data) {
            table_index++;
            if (table_index == size) {
                printf("Table is full\n");
                exit(1);
            }
        }
    
        table[table_index] = later[i];

        while (entry->next)
            entry = (void *) entry->next;
        entry->next = (void *) &table[table_index];

        table_index++;
    }
    free(later);

    return (hash_table_t) {table, size};
}

void hash_print(hash_table_t table) {
    for (int i = 0; i < table.size; i++) {
        hash_t *entry = table.table + i;
        printf("Index: %d\n", i);
        while (entry) {
            printf(" [%d] %s = %s\n", entry->hash, entry->key, entry->data);
            entry = entry->next;
        }
    }
}

const char *hash_get(hash_table_t table, const char *key) {
    uint32_t h = hash(key) % table.size;
    hash_t *entry = table.table + h;


    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return entry->data;
        }
        entry = entry->next;
    }

    return NULL;
}

int main(void) {
    char *data[] = {"my", "name", "is", "hash", "table"};
    char *key[] = {"mon", "nom", "est", "table", "de hash"};

    hash_table_t table = hash_it(key, data, 5);
    hash_print(table);

    for (int i = 0; i < 5; i++) {
        printf("key: %s, data: %s\n", key[i], hash_get(table, key[i]));
    }

    free(table.table);

    return 0;
}
