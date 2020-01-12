CXX=g++
CC=gcc
Q=@
INC=-I./inc -I./src
C_SRCS=$(wildcard ./src/*.c)
CC_SRCS=$(wildcard ./src/*.cc)
C_OBJS=$(patsubst %.c, %.o, $(C_SRCS))
CC_OBJS=$(patsubst %.cc, %.o, $(CC_SRCS))

OBJS=$(C_OBJS) $(CC_OBJS) 

CFLAGS=-g -O2 -Wall $(INC)

OPENCV_PATH=../opencv
OPENCV_INC=-I$(OPENCV_PATH)/inc
OPENCV_LIB=-L$(OPENCV_PATH) -lopencv

CFLAGS+=$(OPENCV_INC) $(OPENCV_LIB)

BIN=app

.PHONY: all
all: deps $(BIN)

.PHONY: deps
deps:
	make -C $(OPENCV_PATH) all

$(BIN): $(OBJS)
	$(Q)printf "%8s %s\n" "CC" $@
	$(Q)$(CC) -o $@ $^ $(CFLAGS) -lstdc++

%.o: %.cc
	$(Q)printf "%8s %s\n" "CXX" $@
	$(Q)$(CXX) -c $< -o $@ $(CFLAGS)

%.o: %.c
	$(Q)printf "%8s %s\n" "CC" $@
	$(Q)$(CC) -c $< -o $@ $(CFLAGS) -lstdc++


.PHONY: clean
clean:
	$(Q)rm -rf $(BIN) $(OBJS)
	$(Q)make -C $(OPENCV_PATH) clean

.PHONY: call
call:
	$(Q)echo $(C_SRCS) $(CC_SRCS)
	$(Q)echo $(C_OBJS) $(CC_OBJS) $(OBJS)
	@echo $(CFLAGS)