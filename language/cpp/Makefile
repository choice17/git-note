# http://nuclear.mutantstargoat.com/articles/make/
# https://www.gnu.org/software/make/manual/make.html#Recursion
CC := gcc
CXX := g++
AR := ar
CFLAGS :=  -Wall
ARFLAGS := -r 
LIBS := -lstdc++ -lpthread -lm -lz 

SDIR := src
ODIR := obj
BDIR := bin
LDIR := lib

BIN = play
BINARY := ${BDIR}/${BIN}
SRCS := \
$(wildcard src/*.c) \
$(wildcard src/*.cc)
OBJS = $(addprefix $(ODIR)/,$(patsubst %.c,%.o,$(SRCS:.cc=.o)))

INCLUDES := \
-I. \
-Iinc \
-L$(LDIR)

all: $(BINARY)

#$(LIBS_PATH): $(OBJS)
#	@mkdir -p $(dir $@)
#	$(AR) -r  $@ $^

$(ODIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(ODIR)/%.o: %.cc
	@mkdir -p $(dir $@)
	$(CXX) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(BINARY): $(OBJS)
	@mkdir -p $(dir $@)
	$(CXX) $(CFLAGS) $(INCLUDES) -o $@ $^ $(LIBS)

cleanObj:
	rm -rf $(OBJS) 

.PHONY: clean
clean:
	@rm -rf $(BDIR) $(ODIR) $(LDIR)
	
.PHONY: call
call:
	@echo 1. $(SDIR) $(ODIR) $(LDIR) $(BDIR) 
	@echo 2. $(LIBS_PATH) $(LIBS) $(INCLUDES)
	@echo 3. $(BINARY)
	@echo 4. $(OBJS)

.PHONY: link
link: $(BINARY)

.PHONY: lib
lib: $(LIBS_PATH)
