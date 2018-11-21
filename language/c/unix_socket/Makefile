CC=gcc

BINS= server client
SRCS= server.c client.c
.PHONY: all

all: $(BINS)

$(BINS): $(SRCS)
	$(CC) -o $@ $<

.PHONY: clean
clean:
	@rm $(BINS)
