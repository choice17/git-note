"""
Reference https://en.wikipedia.org/wiki/Breadth-first_search

breadth search on binary tree
Worst case performance 
O(|V| + |E|) = O(b^d)

worst-case space complexity
O(|V|) = O(b^d)

@author tcyu@umich.edu
@date 2019/04/18
"""

import random as R
idx = 0

class NODE(object):
	def __init__(self):
		global idx
		self.next = [None,None]
		self.prev = None # for doubly linked list node
		self.id = idx
		self.edge = R.randint(0,1000)
		idx += 1
		self.list = []

class TREE(object):
	def __init__(self):
		self.root = NODE()
		self.root.edge = 0
		self.depth = 0

	def setDepth(self, dep):
		assert dep > 0, 'dep should greater than 0'
		self.depth = dep
		TREE.addLeaf(self.root, dep)

	def addLeaf(node, lvl):
		if lvl > 0:
			node.next[0] = NODE()
			TREE.addLeaf(node.next[0], lvl-1)
			node.next[1] = NODE()
			TREE.addLeaf(node.next[1], lvl-1)

	def BFS(node, idx, path, edge, find_idx=None):
		"""
		Breadth First Search
		@param: node - input node addr
		@param: idx - idx of node
		@param: path - for record
		@param: edge - loading attr of current node
		@param: find_idx - extra for search destination
		@retval: list of dict of path, depth, (path, total loading)
		"""
		if node is None:
			return []
		else:
			depth = node.edge + edge
			path += (node.id,)
			li = []
			if find_idx is not None:
				if node.id == find_idx:
					li += [{"parent":idx,"node":node.id, "path":path, "edge":node.edge, "depth":depth}]
			else:
				li += [{"parent":idx,"node":node.id, "path":path, "edge":node.edge, "depth":depth}]
			li +=  TREE.BFS(node.next[0], node.id, path, depth, find_idx)
			li +=  TREE.BFS(node.next[1], node.id, path, depth, find_idx)
		return li

def main():
	tree = TREE()
	tree.setDepth(3)
	tree.root.next[0].next[1].next[0].next[0] = NODE()
	tree.root.next[1].next[0].next[0].next[0] = tree.root.next[0].next[1].next[0].next[0]
	tree.root.next[1].next[1].next[1].next[1] = tree.root.next[0].next[1].next[0].next[0]
	"""
	tree.root.next[0].next[1].next[0].next[0] = NODE()
	tree.root.next[1].next[0].next[0].next[1] = tree.root.next[0].next[1].next[0].next[0]
	"""

	print("total node: %d" % idx)

	li = TREE.BFS(tree.root, tree.root.id, tuple(), 0, idx-1)
	[print(i) for i in li]

if __name__ == "__main__":
	main()