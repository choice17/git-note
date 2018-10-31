CC = gcc

BIN = test
SRC = $(wildcard *.c)
OBJ = $(patsubst %.c, %.o, $(SRC))
INC = -I.

all: $(BIN)

%.o: %.c 
	$(CC) $(INC) $^ -o $@

$(BIN): $(OBJ)
	$(CC) $(INC) -o $@ $(OBJ)

.PHONY: clean
clean:
	rm *.o 
