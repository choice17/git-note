"""
reference
===========
https://www.coursera.org/learn/motion-planning-self-driving-cars/
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
// A* (star) Pathfinding
// Initialize both open and closed list
let the openList equal empty list of nodes
let the closedList equal empty list of nodes
// Add the start node
put the startNode on the openList (leave it's f at zero)
// Loop until you find the end
while the openList is not empty
    // Get the current node
    let the currentNode equal the node with the least f value
    remove the currentNode from the openList
    add the currentNode to the closedList
    // Found the goal
    if currentNode is the goal
        Congratz! You've found the end! Backtrack to get path
    // Generate children
    let the children of the currentNode equal the adjacent nodes
    
    for each child in the children
        // Child is on the closedList
        if child is in the closedList
            continue to beginning of for loop
        // Create the f, g, and h values
        child.g = currentNode.g + distance between child and current
        child.h = distance from child to end
        child.f = child.g + child.h
        // Child is already in openList
        if child.position is in the openList's nodes positions
            if the child.g is higher than the openList node's g
                continue to beginning of for loop
        // Add the child to the openList
        add the child to the openList


"""
from time import sleep
import sys

NODE_CNT = 0
def F(fp):
    return int(fp * 100)/100

class NODE(object):
    """A node class for A* Pathfinding
    @param: g - gcost heuristic cost (cheapest) from start node to node n
    @param: h - hcost heuristic cost (cheapest) to reach goal node from node n
    @param: f - fcost = gcost + hcost
    """
    __slot__ = ('id', 'prev', 'next', 'pos', 'g', 'h', 'f', 'visited','n')

    def __init__(self, prev=None, prev_len=None, nxt=None, nxt_len=None, pos=None, copy=None, n=None):
        if copy is None:
            self.prev = []
            self.prev_len = []
            self.nxt = []
            self.nxt_len = []
            self.pos = pos
            self.g = 0
            self.h = 9999
            self.f = 9999
            self.visited = 0

            global NODE_CNT
            self.id = NODE_CNT
            self.n = n
            NODE_CNT += 1
            if prev is not None:
                prev.nxt.append(self)
                prev.nxt_len.append(prev_len)
                #self.prev.append(prev)
                #self.prev_len.append(prev_len)
            if nxt is not None:
                nxt.prev.append(self)
                nxt.prev_len.append(nxt_len)
                #self.nxt.append(nxt)
                #self.nxt_len.append(nxt_len)
        else:
            self.id = copy.id
            self.pos = copy.pos
            self.prev = []
            self.prev_len = []
            self.nxt = []
            self.nxt_len = []

    def add_prev(prev, _len):
        self.prev.append(prev)
        self.prev_len(_len)

    def add_next(self, nxt, _len):
        self.nxt.append(nxt)
        self.nxt_len.append(_len)

    def getLen(prev, nxt):
        i = 0
        for p in prev.nxt:
            if p.id == nxt.id:
                return prev.nxt_len[i]
            i += 1
        return 0

    def calc_hgf(self, s, t, cur):
        self.g = cur.g + NODE.getLen(cur, self)
        self.h = NODE.dist(self, t)
        self.f = self.g + self.h

    def dist(s, t):
        return ((t.pos[0] - s.pos[0]) ** 2 + (t.pos[1] - s.pos[1]) ** 2) ** 0.5

    def __eq__(self, node):
        return (self.pos[0] == node.pos[0]) and (self.pos[1] == node.pos[1]) 


    def calc_h(self, t):
        if (self.visited == 0):
            self.h = NODE.dist(self, t)
            self.visited = 1
        for i in self.nxt:
            if (i.visited == 0):
                i.calc_h(t)

    def printNode(self):
        i = 0
        if self.visited == 0:
            self.visited = 1
        for j in self.nxt:
            print((self.id, self.n, self.pos, F(self.h), self.visited),"=",self.nxt_len[i],"=>", (j.id, j.n, j.pos, j.visited))
            if (j.visited == 0):
                j.printNode()
            i += 1

    def freeNode(self):
        if self.visited:
            self.visited = 0
        for i in self.nxt:
            if i.visited == 1:
                i.freeNode()

    def getLen(self, node):
        i = 0
        for n in node.nxt:
            if n.id == self.id:
                return node.nxt_len[i]
            i += 1
        return 0

def definemap():
    s = NODE(pos=(0.0, 0.0),n='s')
    a = NODE(prev=s, prev_len=5, pos=(1.0, 2.0), n='a')
    b = NODE(prev=s, prev_len=7, pos=(2.0, 2.0), n='b')
    c = NODE(prev=s, prev_len=2, pos=(1.0, 0.0), n='c')
    e = NODE(prev=b, prev_len=3, pos=(3.0, 3.0), n='e')
    c.add_next(e, 8)
    d = NODE(prev=a, prev_len=2, pos=(3.0, 2.0), n='d')
    d.add_next(e, 7)
    e.add_next(d, 7)
    t = NODE(prev=d, prev_len=1, pos=(4.0, 2.0), n='t')
    e.add_next(t, 4)
    node = []
    node = [s,a,b,c,e,d,t]
    return s, t, node

DEBUG_ = 1
def DEBUG(msg):
    if DEBUG_: print("[DEBUG] ", msg)

class PATH(object):

    def __init__(self, node=None):
        if node:
            self.id = [node.id]
            self.g = 0
            self.f = 0+node.h
        else:
            self.id = []
            self.g = 0
            self.f = 0
    def add(self, node, nodes):
        self.g += node.getLen(nodes[self.id[-1]])
        self.id += [node.id]
        self.f = self.g + node.h

    def copy(self):
        path = PATH()
        path.id = [] + self.id
        path.f = 0 + self.f
        path.g = 0 + self.g
        return path

    def newPathAdd(self, node, nodes):
        path = PATH()
        path.id = []+self.id
        path.f = 0+self.f
        path.g = 0+self.g
        #print(0,path.id)
        path.add(node, nodes)
        #print(1,path.id)
        return path

class Astar(object):

    def findLeastFPath(paths):
        f = 9999
        idx = 0
        idx_min = 0
        for p in paths:
            if (f > p.f):
                f = p.f
                idx_min = idx
            idx += 1
        return idx_min, f, paths[idx_min]

    def search(s ,t, nodes, TOP=2):
        # Init start and end node
        s.calc_h(t)
        s.freeNode()
        DEBUG("+++++++++++")
        s.printNode()
        s.freeNode()
        # Init open and close list
        open_list = []
        closed_list = []
        top_cnt = 0
        # Add the start node
        path = PATH(s)
        DEBUG(("root",path.id, path.f,s.f))
        open_list.append(path)
        return_list = []
        K = -1
        # Loop till soln found
        while len(open_list) > 0:
            K += 1
            DEBUG("======%d=========" % K)
            # Get current node
            idx, min_f, current_node = Astar.findLeastFPath(open_list)
            DEBUG(("min_f",current_node.id, min_f))
            current_index = 0; i = 0
            open_list.pop(idx)
            # Check for goal
            if current_node.id[-1] == t.id:
                DEBUG(('closed-0',current_node.id, current_node.f))
                DEBUG(('closed', [i.id for i in closed_list]))
                return_list.append(current_node)
                top_cnt += 1
                if top_cnt == TOP:
                    DEBUG(('return',[i.id for i in return_list]))
                    return  return_list
                DEBUG(('calc',child.id,{"g":child.g,"f":F(child.f)}))
                DEBUG(('open',[(i.id,F(i.f)) for i in open_list]))
                sys.stdout.flush()
                input()
                continue

            # Generate children
            children = []
            for item in nodes[current_node.id[-1]].nxt:
                DEBUG(('next',item.id))
                # Add constraint if needed
                # reject duplicated set
                b = 0
                for closed_item in closed_list:
                    if item.id == closed_item.id:
                        b = 1
                        break
                if not b:
                    DEBUG(('addchild',item.id,current_node.id))
                    path = current_node.newPathAdd(item, nodes)
                    #path.add(item, nodes)
                    children.append(path)  
            DEBUG(('gen',[i.id for i in children]))
            for child in children:
                for open_item in open_list:
                    if open_item.id[-1] == child.id[-1] and child.g > open_item.g:
                        continue
                DEBUG(('calc',child.id,{"g":child.g,"f":F(child.f)}))
                open_list.append(child)
            closed_list.append(current_node)
            DEBUG(('open',[(i.id,F(i.f)) for i in open_list]))
            sys.stdout.flush()
            input()


class Node(object):
    """A node class for A* Pathfinding
    @param: g - gcost heuristic cost (cheapest) from start node to node n
    @param: h - hcost heuristic cost (cheapest) to reach goal node from node n
    @param: f - fcost = gcost + hcost
    """
    __slot__ = ('parent', 'position', 'g', 'h', 'f')
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar_maze(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    print("===============example 1 maze ===================")
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (2, 7)

    path = astar_maze(maze, start, end)
    for ii in path:
        a, b = ii
        maze[a][b] = 4
    print(path)
    for i in maze:
        print(i)

    print("==============example 2 map======================")

    s, t, node = definemap()
    s.printNode()
    s.freeNode()
    path = Astar.search(s, t, node)
    print(path)


if __name__ == '__main__':
    main()