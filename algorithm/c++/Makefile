CXX:=g++
OPTIM:=-O3
CXXFLAGS:=-std=c++11 -lstdc++ -Wall -g $(OPTIM)
Q:=@

BIN:=binRev tran2d maze


.PHONY: binary_rev
binary_rev:
	$(Q)$(CXX) -o binRev binaryTreeReversal.cpp $(CXXFLAGS)

.PHONY: tranverse_2d
tranverse_2d:
	$(Q)$(CXX) -o tran2d tranverse_2d.cc $(CXXFLAGS)

.PHONY: dijkstra
dijkstra:
	$(Q)$(CXX) -o maze dijkstra.cc $(CXXFLAGS)

.PHONY: clean
clean:
	$(Q)rm $(BIN)

.PHONY: help
help:
	@echo  make [options]
	@echo  1. binary_rev 
	@echo  2. tranverse_2d 
	@echo  3. maze 

