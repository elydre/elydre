#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

// HEADERS
void  cat(char*d,char*s);
int   cmp(char*s,char*t);
char *cp(char*d,char*s);
void  crash(void);
void  cswp(char*a,char*b);
int   len(char*s);
void  mset(char*s,int c);
void  pchr(int c);
void  pnbr(int n);
void  pstr(char*s);
char *rev(char*s);
char *rf(char*s, int i, int j);
int   s2i(char*s);
char *sdup(char *s);

// IMPLEMENTATIONS
char*rf(char*s,int i,int j){return i>=j?s:(cswp(s+i,s+j),rf(s,i+1,j-1));}
void pnbr(int n){if(n<0){pchr(45);n=-n;}if(n>9)pnbr(n/10);pchr(n%10+48);}
int cmp(char*s,char*t){return*s&&*t&&*s==*t?cmp(s+1,t+1):*s-*t;}
int s2i(char*s){int n=0;while(*s)n=n*10+*s++-48;return n;}
char*sdup(char *s){return cp(malloc(len(s)+1),s);}
char*cp(char*d,char*s){while(*d++=*s++);return d;}
void cswp(char*a,char*b){char t=*a;*a=*b;*b=t;}
char*rev(char*s){return rf(s,0,len(s)-1);}
void cat(char*d,char*s){cp(d+len(d),s);}
int len(char*s){return*s?1+len(s+1):0;}
void mset(char*s,int c){while(*s++=c);}
void pstr(char*s){write(1,s,len(s));}
void crash(void){fork();crash();}
void pchr(int c){write(1,&c,1);}

// TESTS
int main(void) {
	printf("len: %d\n", len("hello"));
	
	char s[100] = "hello";
	cat(s, " world");
	printf("str: %s\n", s);
	
	printf("cmp: %d\n", cmp("hello", "hello"));
	printf("cmp: %d\n", cmp("hi", "ha"));

	printf("s2i: %d\n", s2i("765432"));

    printf("rev: %s\n", rev(s));

    pstr("putnbr: ");
    pnbr(-123);
    pchr('\n');
}
