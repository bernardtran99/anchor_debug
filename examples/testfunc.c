#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <pthread.h>
#include <stdbool.h>
#include <setjmp.h>

void c() {
    printf("test\n");
}


void b() {
    c();
}


void a() {
    b();
}


int main() {
    a();
    return 0;
}