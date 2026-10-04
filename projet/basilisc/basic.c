#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define VAR_STRING 1
#define VAR_NUMBER 2

#define WORD_NONE 0
#define WORD_VAR  1
#define WORD_STR  2
#define WORD_NUM  3

#define WORD_FIRST_INST 4

#define WORD_INST_INPUT 4
#define WORD_INST_PRINT 5
#define WORD_INST_GOTO  6
#define WORD_INST_IF    7
#define WORD_INST_STOP  8
#define WORD_INST_LET   9
#define WORD_INST_LEN   10
#define WORD_INST_THEN  11
#define WORD_INST_LT    12
#define WORD_INST_PLUS  13

#define VAARG_FUNC 10

#define EXEC_END      0xFFFF
#define EXEC_ERROR    0xFFFE
#define EXEC_CONTINUE 0xFFFD

typedef struct variable {
    char *name;
    int type;
    union {
        char *str;
        int num;
    } value;
    struct variable *prev;
} variable_t;

typedef struct word {
    int type;
    union {
        struct word *inst_args;
        variable_t *var_ptr;
        char *str;
        int num;
    };
} word_t;

typedef struct {
    variable_t *variables;
    word_t *lines;
} program_t;

typedef struct {
    int type;
    char *name;
    int argc;
} instruction_t;

variable_t *g_var_tail = NULL;
int goto_table[100] = {0xFFFF};

instruction_t instructions[] = {
    {WORD_INST_INPUT, "INPUT", 1},
    {WORD_INST_PRINT, "PRINT", VAARG_FUNC},
    {WORD_INST_GOTO,  "GOTO",  1},
    {WORD_INST_IF,    "IF",    2},
    {WORD_INST_STOP,  "STOP",  0},
    {WORD_INST_LET,   "LET",   2},
    {WORD_INST_LEN,   "LEN",   1},
    {WORD_INST_THEN,  "THEN",  VAARG_FUNC},
    {WORD_INST_LT,    "<",     2},
    {WORD_INST_PLUS,  "+",     2},
};

int tok_end(char *str, int length) {
    int i = 0;
    int in_quotes = 0;
    while (i < length && str[i] && (str[i] != ' ' || in_quotes) && str[i] != '\n') {
        if (str[i] == '"') {
            in_quotes = !in_quotes;
        }
        i++;
    }
    return i;
}

int line_end(char *str, int length) {
    int i = 0;
    while (i < length && str[i] && str[i] != '\n') {
        i++;
    }
    return i;
}

int isnumber(char *str, int length) {
    if (length == 0) {
        return 0;
    }
    for (int i = 0; i < length; i++) {
        if (str[i] < '0' || str[i] > '9') {
            return 0;
        }
    }
    return 1;
}

void free_word(word_t *word, int is_parent) {
    if (word->type >= WORD_FIRST_INST) {
        for (int i = 0; word->inst_args[i].type != WORD_NONE; i++) {
            free_word(word->inst_args + i, 0);
        }
    } else if (word->type == WORD_STR) {
        free(word->str);
    }
    if (is_parent) {
        free(word);
    } else if (word->type >= WORD_FIRST_INST) {
        free(word->inst_args);
    }
}

int is_valid_var_name(char *str, int length) {
    if (length == 0) {
        return 0;
    }
    if (!((str[0] >= 'a' && str[0] <= 'z') || (str[0] >= 'A' && str[0] <= 'Z'))) {
        return 0;
    }
    for (int i = 1; i < length; i++) {
        if (!((str[i] >= 'a' && str[i] <= 'z') || (str[i] >= 'A' && str[i] <= 'Z') || (str[i] >= '0' && str[i] <= '9') || str[i] == '_')) {
            return 0;
        }
    }
    return 1;
}

variable_t *get_variable(char *str, int length) {
    variable_t *var = g_var_tail;
    while (var) {
        if (strncmp(var->name, str, length) == 0 && var->name[length] == '\0') {
            return var;
        }
        var = var->prev;
    }
    return NULL;
}

variable_t *get_variable_or_create(char *str, int length) {
    variable_t *var = get_variable(str, length);
    if (var) {
        return var;
    }

    // variable not found, create a new one
    var = malloc(sizeof(variable_t));
    var->name = strndup(str, length);
    var->type = VAR_NUMBER;
    var->value.num = 0;
    var->prev = g_var_tail;
    g_var_tail = var;

    return var;
}

int check_goto_label(char *str, int *length, int pos) {
    if (*length == 0 || str[0] != '[') {
        return 0;
    }

    int i = 1;
    while (i < *length && str[i] != ']') {
        i++;
    }

    // found a label
    if (!isnumber(str + 1, i - 1)) {
        printf("Error: invalid label number: '%.*s'\n", i - 1, str + 1);
        return 0;
    }
    int label_num = atoi(str + 1);
    if (label_num < 0 || label_num >= 100) {
        printf("Error: label number out of range: %d\n", label_num);
        return 0;
    }
    goto_table[label_num] = pos; // mark label as used
    *length -= i + 1;
    return i + 1; // return the number of characters to skip
}

int find_matching_parenthesis(char *str, int length) {
    int open_parens = 1;
    int end = 0;

    while (end < length && open_parens > 0) {
        if (str[end] == '(') {
            open_parens++;
        } else if (str[end] == ')') {
            open_parens--;
        }
        end++;
    }
    if (open_parens != 0) {
        return 0;
    }
    return end;
}

word_t *parse_str(char *str, int length, word_t *word) {
    while (length > 0 && (*str == ' ')) {
        str++;
        length--;
    }

    printf("Parsing: %.*s\n", length, str);

    int end = tok_end(str, length);

    if (end == 0) {
        printf("Error: empty instruction\n");
        return NULL;
    }

    int expected_args = 0;
    int type = 0;
    
    if (end > 1 && str[0] == '"' && str[end - 1] == '"') {
        if (word == NULL)
            word = malloc(sizeof(word_t));
        word->type = WORD_STR;
        word->str = strndup(str + 1, end - 2);
        return word;
    } else if (isnumber(str, end)) {
        if (word == NULL)
            word = malloc(sizeof(word_t));
        word->type = WORD_NUM;
        word->num = atoi(str);
        return word;
    }

    word_t preloaded_word;
    preloaded_word.type = WORD_NONE;
    
    for (unsigned i = 0; i < sizeof(instructions) / sizeof(instruction_t); i++) {
        if (strncmp(str, instructions[i].name, end) == 0) {
            type = instructions[i].type;
            expected_args = instructions[i].argc;
            break;
        }
    }

    if (type == 0) {
        int debut = end;
        while (debut < length && str[debut] == ' ') {
            debut++;
        }
        if (debut < length && str[debut] == '=') {
            if (!is_valid_var_name(str, end)) {
                printf("Error: invalid variable name: '%.*s'\n", end, str);
                return NULL;
            }
            type = WORD_INST_LET;
            expected_args = 2;
            preloaded_word.type = WORD_VAR;
            preloaded_word.var_ptr = get_variable_or_create(str, end);
            end = debut + 1; // skip '='
        } else if (get_variable(str, end) != NULL) {
            if (word == NULL)
                word = malloc(sizeof(word_t));
            word->type = WORD_VAR;
            word->var_ptr = get_variable(str, end);
            return word;
        } else {
            printf("Error: unknown instruction: '%.*s'\n", end, str);
            return NULL;
        }
    }

    str += end;
    length -= end;

    void *to_free = NULL;
    if (word == NULL) {
        to_free = word = malloc((expected_args + 2) * sizeof(word_t));
        word->inst_args = (word_t *)(word + 1);
    } else {
        to_free = word->inst_args = malloc((expected_args + 1) * sizeof(word_t));
    }

    word->type = type;
    word->inst_args[expected_args].type = WORD_NONE;

    int argc = 0;
    if (preloaded_word.type != WORD_NONE) {
        word->inst_args[argc++] = preloaded_word;
    }

    for (; argc < expected_args; argc++) {
        while (length > 0 && (*str == ' ')) {
            str++;
            length--;
        }

        if (length == 0) {
            if (expected_args >= VAARG_FUNC) {
                // variable number of arguments
                word->inst_args[argc].type = WORD_NONE;
                return word;
            }
            printf("Error: not enough arguments\n");
            free(to_free);
            return NULL;
        }

        int have_parentheses = 0;
        if (str[0] == '(') {
            have_parentheses = 1;
            str++;
            length--;
            end = find_matching_parenthesis(str, length);
            if (end == 0) {
                printf("Error: unclosed parentheses\n");
                free(to_free);
                return NULL;
            }
            if (end == 1) {
                printf("Error: empty parentheses\n");
                free(to_free);
                return NULL;
            }
        } else {
            end = tok_end(str, length);
        }

        word_t *arg;
        if (have_parentheses) {
            arg = parse_str(str, end - 1, word->inst_args + argc);
        } else {
            arg = parse_str(str, length, word->inst_args + argc);
            if (arg && arg->type >= WORD_FIRST_INST) {
                if (expected_args != argc + 1 && expected_args < VAARG_FUNC) {
                    printf("Error: wrong number of arguments %d, expected %d\n", argc + 1, expected_args);
                    free(to_free);
                    return NULL;
                }
                end = length;
            }
        }

        if (!arg) {
            free(to_free);
            return NULL;
        }

        str += end;
        length -= end;
    }

    while (length > 0 && (*str == ' ')) {
        str++;
        length--;
    }

    if (length == 0) {
        return word;
    }

    printf("Error: too many arguments\n");
    // too many arguments
    free(to_free);
    return NULL;
}

void print_word(word_t *word) {
    if (word->type >= WORD_FIRST_INST)
        printf("( ");

    switch (word->type) {
        case WORD_NONE:
            printf("None ");
            break;
        case WORD_VAR:
            printf("%s ", word->var_ptr->name);
            break;
        case WORD_STR:
            printf("\"%s\" ", word->str);
            break;
        case WORD_NUM:
            printf("%d ", word->num);
            break;
        default:
            for (unsigned i = 0; i < sizeof(instructions) / sizeof(instruction_t); i++) {
                if (instructions[i].type == word->type) {
                    printf("%s ", instructions[i].name);
                    break;
                }
            } 
            printf("[type: %d] ", word->type);
            break;
    }

    if (word->type < WORD_FIRST_INST)
        return;

    for (int i = 0; word->inst_args[i].type != WORD_NONE; i++) {
        print_word(word->inst_args + i);
    }
    printf(") ");
}

int execute_word(word_t *word, word_t *return_value) {
    if (return_value) {
        return_value->type = WORD_NONE;
    }
    word_t args[10];
    int argc = 0;
    for (; word->inst_args[argc].type != WORD_NONE; argc++) {
        if (argc >= 10) {
            printf("Error: too many arguments\n");
            return EXEC_ERROR;
        }
        if (word->inst_args[argc].type == WORD_VAR) {
            if (word->type == WORD_INST_LET) {
                args[argc] = word->inst_args[argc];
            } else {
                if (word->inst_args[argc].var_ptr->type == VAR_STRING) {
                    args[argc].type = WORD_STR;
                    args[argc].str = word->inst_args[argc].var_ptr->value.str;
                } else {
                    args[argc].type = WORD_NUM;
                    args[argc].num = word->inst_args[argc].var_ptr->value.num;
                }
            }
        } else if (word->inst_args[argc].type < WORD_FIRST_INST) {
            args[argc] = word->inst_args[argc];
        } else if (word->type != WORD_INST_IF || argc != 1) {
            int a = execute_word(word->inst_args + argc, args + argc);
            if (a != EXEC_CONTINUE) {
                return a;
            }
        }
    }

    switch (word->type) {
        case WORD_INST_PRINT:
            for (int i = 0; i < argc; i++) {
                switch (args[i].type) {
                    case WORD_STR:
                        printf("%s", args[i].str);
                        break;
                    case WORD_NUM:
                        printf("%d", args[i].num);
                        break;
                    case WORD_NONE:
                        printf("None");
                        break;
                    default:
                        printf("[type: %d]", args[i].type);
                        break;
                }
                if (i < argc - 1) {
                    printf(" ");
                }
            }
            printf("\n");
            break;
        case WORD_INST_LEN:
            if (args[0].type == WORD_STR) {
                if (return_value) {
                    return_value->type = WORD_NUM;
                    return_value->num = strlen(args[0].str);
                }
            } else {
                printf("Error: LEN expects a string argument\n");
                return EXEC_ERROR;
            }
            break;
        case WORD_INST_STOP:
            return EXEC_END;
        case WORD_INST_LET:
            if (args[0].type != WORD_VAR) {
                printf("Error: LET expects a variable as first argument\n");
                return EXEC_ERROR;
            }
            if (args[1].type == WORD_STR) {
                args[0].var_ptr->type = VAR_STRING;
                args[0].var_ptr->value.str = strdup(args[1].str);
            } else if (args[1].type == WORD_NUM) {
                args[0].var_ptr->type = VAR_NUMBER;
                args[0].var_ptr->value.num = args[1].num;
            } else {
                printf("Error: LET expects a string or number as second argument\n");
                return EXEC_ERROR;
            }
            break;
        case WORD_INST_THEN:
            // arguments are already executed, nothing to do here
            break;
        case WORD_INST_IF:
            if ((args[0].type == WORD_NUM && args[0].num) || (args[0].type == WORD_STR && args[0].str[0])) {
                int a = execute_word(word->inst_args + 1, NULL);
                if (a != EXEC_CONTINUE) {
                    return a;
                }
            }
            break;
        case WORD_INST_GOTO:
            if (args[0].type != WORD_NUM) {
                printf("Error: GOTO expects a number argument\n");
                return EXEC_ERROR;
            }
            if (args[0].num < 0 || args[0].num >= 100 || goto_table[args[0].num] == 0xFFFF) {
                printf("Error: GOTO label %d does not exist\n", args[0].num);
                return EXEC_ERROR;
            }
            return goto_table[args[0].num];
        case WORD_INST_LT:
            if (args[0].type != WORD_NUM || args[1].type != WORD_NUM) {
                printf("Error: < expects two number arguments\n");
                return EXEC_ERROR;
            }
            if (return_value) {
                return_value->type = WORD_NUM;
                return_value->num = args[0].num < args[1].num;
            }
            break;
        case WORD_INST_PLUS:
            if (args[0].type != WORD_NUM || args[1].type != WORD_NUM) {
                printf("Error: + expects two number arguments\n");
                return EXEC_ERROR;
            }
            if (return_value) {
                return_value->type = WORD_NUM;
                return_value->num = args[0].num + args[1].num;
            }
            break;
        default:
            printf("Error: unknown instruction type: %d\n", word->type);
            return EXEC_ERROR;
    }
    return EXEC_CONTINUE;
}

void free_variable_list(variable_t *var) {
    while (var) {
        variable_t *prev = var->prev;
        if (var->type == VAR_STRING) {
            free(var->value.str);
        }
        free(var->name);
        free(var);
        var = prev;
    }
}

int main(void) {
    /*char *program =
            "age = 100\n"
            "IF (< age 18) GOTO 1\n"
            "PRINT \"You are an adult.\"\n"
            "STOP\n"
            "[1] PRINT \"You are a minor.\"\n";*/

    char *program =
            "i = 0\n"
            "[1] i = + i 1\n"
            "PRINT i\n"
            "IF (< i 10) GOTO 1\n";

    /*char *program =
            "coucou = \"hi!\"\n"
            "PRINT \"Hello\" (LEN \"oui\") coucou\n"
            "PRINT 1 LEN \"hi\"\n"
            "IF 1 THEN (PRINT \"if is true\") (PRINT 123)\n";*/

    // split program into lines
    word_t *lines[10];
    int line_count = 0;

    while (*program) {
        int end = line_end(program, strlen(program));
        if (end == 0) {
            break;
        }
        printf("Line: %.*s\n", end, program);

        program += check_goto_label(program, &end, line_count);
        lines[line_count] = parse_str(program, end, NULL);
        if (lines[line_count] == NULL) {
            printf("Error parsing instruction: %.*s\n", end, program);
            return 1;
        }

        line_count++;
        program += end + 1;
    }

    for (int i = 0; i < line_count; i++) {
        print_word(lines[i]);
        printf("\n");
    }

    printf("Executing program...\n");

    for (int i = 0; i < line_count;) {
        int a = execute_word(lines[i], NULL);
        if (a == EXEC_ERROR) {
            return 1;
        } else if (a == EXEC_END) {
            break;
        } else if (a != EXEC_CONTINUE) {
            i = a;
        } else {
            i++;
        }
    }

    for (int i = 0; i < line_count; i++) {
        free_word(lines[i], 1);
    }

    free_variable_list(g_var_tail);
}
