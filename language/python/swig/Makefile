CC=gcc
CFLAGS=-O3 -Wall -fPIC -std=gnu99 -shared
PYTHON_ENV=c:\anaconda\envs\py36
INC=-I. \
-I$(PYTHON_ENV)\include
LIB=-L$(PYTHON_ENV) -lpython36 -lm -mwindows
BIN=_test.pyd
SRCS=test.c test_wrap.c
OBJS=$(SRCS:.c=.o)

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) $(INC) $< -o $@ $(LIB)

%.o: %.c
	$(CC) $(CFLAGS) $(INC) -c $^ -o $@ $(LIB)

clean:
	rm $(BIN) $(OBJS)