#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
    void *ptr;

    uint8_t type;
} ast_leaf_t;

typedef struct {
    ast_leaf_t left;
    ast_leaf_t center;
    ast_leaf_t right;
} ast_t;

#define AST_TYPE_AST   0
#define AST_TYPE_NIL   1
#define AST_TYPE_STR   3

char ops[] = "+-*/^&|~<>=()";


void printsplit(char **split) {
    for (int i = 0; split[i] != NULL; i++) {
        printf(i == 0 ?
                "[\"%s\", " :
                split[i + 1] ?
                    "\"%s\", " :
                    "\"%s\"]\n"
            , split[i]
        );
    }
}

ast_t *gen_ast(char **str, int len) {
    ast_t *ast = malloc(sizeof(ast_t));
    ast->left.type = AST_TYPE_NIL;
    ast->right.type = AST_TYPE_NIL;
    ast->center.type = AST_TYPE_NIL;

    // if start with parenthesis and end with parenthesis remove them
    if (len > 2 && str[0][0] == '(' && str[len - 1][0] == ')') {
        str++;
        len -= 2;
    }

    // check if only one element
    if (len == 1) {
        ast->center.type = AST_TYPE_STR;
        ast->center.ptr = str[0];
        return ast;
    }

    // check if only two elements
    if (len == 2) {
        ast->left.type = AST_TYPE_STR;
        ast->left.ptr = str[0];
        ast->right.type = AST_TYPE_STR;
        ast->right.ptr = str[1];
        return ast;
    }

    // check if only one operator
    if (len == 3) {
        ast->left.type = AST_TYPE_STR;
        ast->left.ptr = str[0];
        ast->center.type = AST_TYPE_STR;
        ast->center.ptr = str[1];
        ast->right.type = AST_TYPE_STR;
        ast->right.ptr = str[2];
        return ast;
    }

    // divide and rule

    // find operator with lowest priority
    int op_index = -1;
    int op_priority = 999;
    int op_parenthesis = 0;
    for (int i = 0; i < len; i++) {
        if (str[i][0] == '(') {
            op_parenthesis++;
        } else if (str[i][0] == ')') {
            op_parenthesis--;
        } else if (op_parenthesis == 0) {
            for (int j = 0; j < sizeof(ops); j++) {
                if (str[i][0] == ops[j] && j < op_priority) {
                    op_index = i;
                    op_priority = j;
                    break;
                }
            }
        }
    }

    // check if no operator
    if (op_index == -1) {
        printf("input: ");
        printsplit(str);
        printf("no operator found\n");
        exit(1);
    }

    // split array in three parts
    char **left = malloc(sizeof(char *) * (op_index + 1));
    char **center = malloc(sizeof(char *) * 2);
    char **right = malloc(sizeof(char *) * (len - op_index));

    for (int i = 0; i < op_index; i++)
        left[i] = str[i];
    left[op_index] = NULL;

    center[0] = str[op_index];
    center[1] = NULL;

    for (int i = op_index + 1; i < len; i++)
        right[i - op_index - 1] = str[i];
    right[len - op_index - 1] = NULL;

    // generate ast
    if (op_index == 0) {
        ast->left.type = AST_TYPE_STR;
        ast->left.ptr = str[0];
    } else {
        ast->left.type = AST_TYPE_AST;
        ast->left.ptr = gen_ast(left, op_index);
    }

    ast->center.type = AST_TYPE_STR;
    ast->center.ptr = str[op_index];

    if (len - op_index - 1 == 1) {
        ast->right.type = AST_TYPE_STR;
        ast->right.ptr = str[op_index + 1];
    } else {
        ast->right.type = AST_TYPE_AST;
        ast->right.ptr = gen_ast(right, len - op_index - 1);
    }

    return ast;
}

char *eval(ast_t *ast) {
    // if only one element return it
    if (ast->left.type == AST_TYPE_NIL && ast->right.type == AST_TYPE_NIL) {
        return (char *) ast->center.ptr;
    }

    if (ast->center.type == AST_TYPE_NIL) {
        printf("operator not supported\n");
        return NULL;
    }

    // convert to int
    char *op = (char *) ast->center.ptr;
    int left, right;
    char *res;

    if (ast->left.type == AST_TYPE_AST) {
        res = eval((ast_t *) ast->left.ptr);
        if (res == NULL) return NULL;
        left = atoi(res);
    } else {
        left = atoi((char *) ast->left.ptr);
    }

    if (ast->right.type == AST_TYPE_AST) {
        res = eval((ast_t *) ast->right.ptr);
        if (res == NULL) return NULL;
        right = atoi(res);
    } else {
        right = atoi((char *) ast->right.ptr);
    }

    // calculate
    int result;
    switch (op[0]) {
        case '+':
            result = left + right;
            break;
        case '-':
            result = left - right;
            break;
        case '*':
            result = left * right;
            break;
        case '/':
            result = left / right;
            break;
        default:
            printf("unknown operator: %s\n", op);
            return NULL;
    }

    printf("%d %s %d = %d\n", left, op, right, result);

    // convert back to string
    char *ret = malloc(sizeof(char) * 12);
    sprintf(ret, "%d", result);
    return ret;    
}

int main() {
    char str[] = "1+2*3+4*5+6*7+8*9+10";
    char **elms = malloc(sizeof(char *) * strlen(str) + 1);
    int len = 0;
    int str_len = strlen(str);
    int old_cut = 0;
    for (int i = 0; i < str_len; i++) {
        // check if operator
        for (int j = 0; j < sizeof(ops); j++) {
            if (str[i] != ops[j]) continue;

            if (old_cut != i) {
                elms[len] = malloc(sizeof(char) * (i - old_cut + 1));
                memcpy(elms[len], str + old_cut, i - old_cut);
                elms[len][i - old_cut] = '\0';
                len++;
            }

            elms[len] = malloc(sizeof(char) * 2);
            elms[len][0] = str[i];
            elms[len][1] = '\0';
            len++;

            old_cut = i + 1;
            break;
        }
    }

    if (old_cut != str_len) {
        elms[len] = malloc(sizeof(char) * (str_len - old_cut + 1));
        memcpy(elms[len], str + old_cut, str_len - old_cut);
        elms[len][str_len - old_cut] = '\0';
        len++;
    }

    elms[len] = NULL;

    printsplit(elms);

    ast_t *ast = gen_ast(elms, len);

    char *res = eval(ast);
    printf("result: %s\n", res);

    return 0;
}
