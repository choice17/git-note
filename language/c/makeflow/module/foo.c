#include "foo.h"
#include "msg.h"

#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>

void fooPrintf(void)
{
    static time_t now;
    now = time(NULL);
    char s[100];
    strftime(s, sizeof(s), "%F %H:%M:%S %Z", localtime(&now));
    printf("Hello from %s %d @ %s!\n", __func__, MSG_0, s);
}

void* runFoo(void* data)
{
    while (1)
    {
        sleep(1);
        fooPrintf();
    }

}

void foo(void)
{
    pthread_t tid_foo;
    void* data = {0};
    //pthread_mutex_lock lock;
    if (pthread_create(&tid_foo, NULL, runFoo, data) != 0) {
        printf("Create thread fails\n");
        goto ends;
    }
    sleep(60);
    if (pthread_cancel(tid_foo) != 0) {
        printf("Cancel thread fails\n");
        goto ends;
    }
    void *res;
    if (pthread_join(tid_foo, &res) != 0) {
        printf("Join thread fails\n");
        goto ends;
    }
    goto ends;
ends:
    printf("%s ends\n",__func__);
}

