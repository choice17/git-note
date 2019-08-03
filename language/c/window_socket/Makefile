CC=gcc
CFLAGS=-O2 -Wall -lWs2_32

BIN_CLIENT=app_client
BIN_SERVER=app_server

INCS=-I.
CLI_SRCS=win_client.c
CLI_OBJS=$(patsubst %.c,%.o,$(CLI_SRCS))

SER_SRCS=win_server.c
SER_OBJS=$(patsubst %.c,%.o,$(SER_SRCS))

OBJS = $(CLI_OBJS) $(SER_OBJS)
BINS = $(BIN_CLIENT) $(BIN_SERVER)

.PHONY: all
all: $(BIN_CLIENT) $(BIN_SERVER)

$(BIN_CLIENT): $(CLI_OBJS)
	$(CC) $^ -o $@ $(CFLAGS)  $(INCS)

$(BIN_SERVER)	: $(SER_OBJS)
	$(CC) $^ -o $@ $(CFLAGS)  $(INCS)

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS) $(INCS)

.PHONY: clean
clean:
	rm -rf $(OBJS) $(BINS)