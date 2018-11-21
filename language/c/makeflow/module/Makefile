include $(SRC_DIR)/src.mk 

CC=gcc
CXX=g++
AR=ar
CFLAGS=-Wall -g -std=gnu99 -o3 -fPIC

SRCS=$(wildcard *.c)
OBJS=$(patsubst %.c,%.o,$(SRCS))
BIN=libmodule.a
INCS=-I$(MSG_DIR) -I.
LDLS=-lpthread

.PHONY: all
all: $(BIN)

$(BIN): $(OBJS)
	$(AR) rcs $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $< $(INCS) $(LDLS)

.PHONY: call
call:
	@echo $(OBJS) $(SRCS)

.PHONY: clean
clean:
	@rm -r $(OBJS) $(BIN)
