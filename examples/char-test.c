#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <pthread.h>
#include <stdbool.h>

int main() {
    char *test = "/";
    printf("String: %s\n", test);
    printf("Num: %d\n", test[3]);
    return 0;
}