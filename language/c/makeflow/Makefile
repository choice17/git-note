include src.mk
export SRC_DIR=$(realpath .)

CC=gcc 
CXX=g++
AR=ar
CFLAGS=-Wall -g -std=gnu99 -o3

SRCS=$(wildcard *.c)
OBJS=$(patsubst %.c,%.o,$(SRCS))
BIN=app
INCS=-I. -I$(MODULE_DIR) -I$(MSG_DIR) -L$(MODULE_DIR)
LIBS=-lmodule
LDLS=-lpthread

.PHONY: all
all: module $(BIN)

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) $(INCS) -o $@ $^ $(LIBS) $(LDLS)

%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -o $@ -c $< 

.PHONY: module
module:
	@make -C $(MODULE_DIR) all

.PHONY: call
call:
	@echo 1. $(SRC_DIR)
	@echo 2. $(INCS) / $(LIBS)
	@echo 3. $(OBJS)
	@echo 4. $(SRCS)

.PHONY: modulecall
modulecall:
	@make -C $(MODULE_DIR) call

.PHONY: allclean
allclean:
	@rm -r $(OBJS) $(BIN)
	@make -C $(MODULE_DIR) clean
