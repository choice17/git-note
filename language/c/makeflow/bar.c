#include "bar.h"
#include "msg.h"

#include <stdio.h>

void bar(void)
{
    printf("Hello from %s %d!\n", __func__, MSG_1);
}
