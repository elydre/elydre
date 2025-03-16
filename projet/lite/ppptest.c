#include <sys/wait.h>
#include <sys/time.h>

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

#define MAX_PROCESS 5000
#define CHILD_SLEEP 5
#define REPEAT 5

int current = 0;

#define raise_error(...) { \
    fprintf(stderr, "Error: " __VA_ARGS__); \
    exit(1); \
}

unsigned get_ms(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

pid_t start_process(void) {
    int pid = fork();

    if (pid < 0)
        raise_error("fork failed\n");

    if (pid == 0) {
        sleep(CHILD_SLEEP);
        _exit(0);
    }

    current++;
    return pid;
}

int wait_nohang(void) {
    int status;
    pid_t pid = waitpid(-1, &status, WNOHANG);

    if (pid == 0 || (pid < 0 && errno == ECHILD))
        return 0;

    if (pid < 0)
        raise_error("waitpid: %s\n", strerror(errno));

    current--;
    return 1;
}

unsigned full_wait = 0;

void wait_fatal(void) {
    int status;

    unsigned start = get_ms();
    pid_t pid = wait(&status);
    full_wait += get_ms() - start;

    if (pid < 0)
        raise_error("wait: %s\n", strerror(errno));

    if (pid == 0)
        raise_error("internal: no child to wait\n");

    current--;
}

void start_one(void) {
    int d_count = current;

    while (wait_nohang());

    printf("%d running, %d dead%s\n", current, d_count - current, current >= MAX_PROCESS ? ", wait" : "");

    if (current >= MAX_PROCESS)
        wait_fatal();

    start_process();
}

int main(void) {
    unsigned start = get_ms();

    for (int i = 0; i < MAX_PROCESS * REPEAT; i++)
        start_one();

    while (current > 0)
        wait_fatal();

    double elapsed = (get_ms() - start) / 1000.0;

    printf("elapsed: %.3fs, efficiency: %.2f%%, full wait %.2f%%\n", elapsed, 100.0 * REPEAT * CHILD_SLEEP / elapsed, (double) full_wait / 10 / elapsed);

    return 0;
}
