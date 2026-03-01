#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>


/*
void genlang(uint8_t *O) {
    for (int i = 0; i < 8; i++) {
        O[7 - i] = (i * 3 & 7);
        O[i] = O[i] * (!!(~(O[i] + 1) & 7)) + (i == 5) * 2;
    }
}
*/


char *encoder =
        ":p[]p#]=$p=~f##?&?!&/#4:&/ff*/=?=4f=&~f*?:f!&=:"
        "&+:!#=?::/ff:/=&pp/:?#?[[&$:/f=?:$f&~+#p!&:/?[?"
        "+:?+4#f/~$[/[?:~$*!+!=?$[+:~#]/*+f~]p/4$/?:~=#4"
        "~]]#=f4#?[!p!!=4*:&p*#~]!&4=?4[~&]+!=:?*!=[4]??"
        "/+$$*=:#[/[+/]][~~:*=f*#~$&#/=~#:4=&]&4=f!?#=*&"
        "!4=?[$p==?[&!]#]:::~]=]:!~/?*4$*$[[/]$:?=/=+:f4"
        "?~~//=p#:&/p]:!?p&+=+$[?f$$=*=$~#*:]?#/!+4/f&]?"
        "/$~?&4&[p&#f]p?!:[#?+=[#f#/:$#?&&$/]4[=&[]f$4!$"
        "=#=$[p~=&?$4+&#p4+~4+4/4=*p*&$p~?!$?p]=[p!#p[:*"
        "!&~?pp:=:/:!#p$+?p*#:p!~##/:*f*:p=]+#4$p~/=#p:f"
        "+###f[]/+[?*4p&?4f=$4p!$:&4:?p]$:[$?]f4*=/=!]+4"
        "*44f??~4$+~4p?f?4*=]=[f]~*4=~=?~?&*!=]&~!]]/+~4"
        "f[]&?!#~*/~f$$=]$!*:!?~&4+[44~4fp#?*[=#p!f$$~#?"
        "*$?$f/~f4?p?&4=*&&]&p!p/!]!44:$&!$p/]~+&p~+]:?4"
        "~!~*4f::&/&&f]~4?:#]=/[]*4*[+/:/&+f~[p==$/**4&?"
        "*&:*!?f==![&:f==/#&?4f&=+=[[:p4:=$?]::/$~]=##[*"
        "&]4&*=f&ff*/=:~&4#$&p?[?$:p]??#f!/pp~*+#:[:+!+4"
        "/4p+=?[[*=##&*#!*$#~#=//:/+4*:[*/#!#=pp$:&*p]:4"
        "f:+4:/#&::$~$=/?+&:$f?!/]#:4*4]#p+&==~[]/:[[&=="
        "*?&/[4~f~p4=*~!=?ff&]/=?p#==*~f+/f]#f?]&/$$*~p#"
        "=/+p?p&+?+&4+~&+&~!!p4~pf=+=#*!$4=p&4#~/#4]!+!!"
        "f[p+[~f=[*$$f+pp$]4$&p[&*#&=~4$f!!#*&:ff~f]&][!"
        "[f&f#&/=4$4*&/$&?+]/$~?]4[~~]4:[f#=#f$::4![!p$&"
        "*44[pp&~+*[?/#p&[/=&:&p=+=~4!&!$:!ff$[[=p]+$$[["
        "#=!f=]4$4[?p/~#:/&?/+p:!*:=/&p/[+]:4#/?+*:+&pf4";


uint8_t genop(uint8_t seed) {
    uint8_t O[4] = {1, 3, 0, 2};
    // shuffle O using seed

    seed += encoder[seed] + encoder[seed + 7] * 3;

    for (int i = 0; i < 4; i++) {
        int j = (seed >> (i * 2)) & 3;
        uint8_t temp = O[i];
        O[i] = O[j];
        O[j] = temp;
    }

    return (O[0] << 0) | (O[1] << 2) | (O[2] << 4) | (O[3] << 6);
}

void prog_to_mem(uint8_t *P, int plen, uint8_t *M) {
    for (int i = 0; i < 6; i++)
        M[i] = 0;
    for (int i = 6; i < 134; i++)
        M[i] = encoder[i + P[i % plen]] + M[i - 1];
    for (int i = 131; i >= 6; i--)
        M[i] += encoder[i + P[i % plen]] + M[i + 1];
}

void interpret(uint8_t *P, int plen) {
    uint8_t M[134];
    uint8_t o;

    memset(M, 0, sizeof(M));

    while (M[5] < 127 && M[5] < plen) {
        o = genop(M[133] + M[5]);
        M[0] &= 0x7F;
        M[1] = P[M[5]++];
        M[2] = P[M[5]++];

        if (M[1] == ((o >> 0) & 3)) // load from memory
            M[0] = M[M[2] + 5];
        if (M[1] == ((o >> 2) & 3)) // set
            M[0] = (M[0] + M[2]) * (M[2] != 0);
        if (M[1] == ((o >> 4) & 3)) // add
            M[3] = (M[0] == M[2]);
        if (M[1] != ((o >> 6) & 3) || M[3]) // store to memory
            continue;
        if (M[2] == 1)
            putchar(M[0]);
        if (M[2] == 2)
            printf("%d\n", M[0]);
        M[M[2] + 5] = M[0];
    }
}

void print_op_changes(uint8_t *P, int plen) {
    uint8_t M[134];
    uint8_t o;

    prog_to_mem(P, plen, M);
    for (int i = 0; i < plen; i += 2) {
        o = genop(M[133] + i);
        printf("%3d %d %d %d %d\n", i, (o >> 0) & 3, (o >> 2) & 3, (o >> 4) & 3, (o >> 6) & 3);
    }
}

int main(void) {
    uint8_t hello[] = {
        0, 72,    // set 72 (H)
        2, 1,     // put
        3, 29,    // set 101 (e)
        2, 1,     // put
        3, 7,     // set 108 (l)
        2, 1,     // put
        2, 1,     // put
        3, 3,     // set 111 (o)
        2, 1,     // put
        3, 61,    // set 44 (,)
        2, 1,     // put
        3, 116,   // set 32 (space)
        2, 1,     // put
        3, 55,    // set 87 (W)
        2, 1,     // put
        3, 24,    // set 111 (o)
        2, 1,     // put
        3, 3,     // set 114 (r)
        2, 1,     // put
        3, 122,   // set 108 (l)
        2, 1,     // put
        3, 120,   // set 100 (d)
        2, 1,     // put
        3, 61,    // set 33 (!)
        2, 1,     // put
        3, 105,   // set 10 (newline)
        2, 1,     // put
    };

    print_op_changes(hello, sizeof(hello));

    /* interpret(hello, sizeof(hello));

    uint8_t count[] = {
        1, 2,
        3, 1,
        2, 2,
        0, 20,
        3, 0,
        2, 0,
    };

    interpret(count, sizeof(count));

    return 0;*/
}
