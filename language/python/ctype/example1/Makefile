CC = gcc
CFLAGS = -Wall -O2 -std=gnu99

INCS = -Iinc -Isrc
SRCS = $(wildcard src/*.c) 
OBJS = $(patsubst %.c, %.o,$(SRCS))
LIB = lib/
ALIB = $(LIB)sample.a
SLIB = $(LIB)sample.so

CFLAGS := $(INCS)

all: $(SLIB)

$(SLIB): $(OBJS)
	$(CC) $(CFLAGS) -shared $^ -o $@

$(OBJS): %.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -r $(OBJS) $(ALIB) $(SLIB)
