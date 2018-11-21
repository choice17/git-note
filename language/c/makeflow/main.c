#include "foo.h"
#include "bar.h"

#include <stdio.h>

#define INFO(x, ...) printf((x), ##__VA_ARGS__)

int main()
{
    INFO("%s starts\n", __func__);
    foo();
    bar();
    INFO("%s ends\n", __func__);
}

