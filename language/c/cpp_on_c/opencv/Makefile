CXX=g++
AR=ar
Q=@
INC=./inc
SRCS=$(wildcard ./src/*.cc)
OBJS=$(patsubst %.cc, %.o, $(SRCS))

CFLAGS=-g -O2 -Wall -I$(INC) -std=c++11 -lstdc++

BIN=libopencv.a

all: $(BIN)

$(BIN): $(OBJS)
	$(Q)printf "%8s %s\n" "AR" $@
	$(Q)$(AR) rcs $@ $^

%.o: %.cc
	$(Q)printf "%8s %s\n" "CXX" $@
	$(Q)$(CXX) -c $< -o $@ $(CFLAGS)

.PHONY: clean
clean:
	$(Q)rm -r $(BIN) $(OBJS)

.PHONY: call
call:
	$(Q)echo $(OBJS) $(SRCS)
