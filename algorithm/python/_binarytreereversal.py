import random as R
from graphviz import Digraph as G
idx = 0

dot = G(comment='The Round Table')
gdot = G(comment='The Round Table')

class NODE(object):
	def __init__(self):
		global idx
		self.next = [None,None]
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
		global dot
		assert dep > 0, 'dep should greater than 0'
		self.depth = dep
		dot.node(str(self.root.id))
		TREE.addLeaf(self.root, dep)

	def addLeaf(node, lvl):
		global dot
		if lvl > 0:
			node.next[0] = NODE()
			dot.node(str(node.next[0].id))
			dot.edge(str(node.id), str(node.next[0].id))
			TREE.addLeaf(node.next[0], lvl-1)
			node.next[1] = NODE()
			dot.node(str(node.next[1].id))
			dot.edge(str(node.id), str(node.next[1].id))
			TREE.addLeaf(node.next[1], lvl-1)

	def bianryReversal(node):
		global gdot
		temp = node.next[0]
		if (node.next[0] is not None) and \
			(node.next[1] is not None):
			node.next[0] = node.next[1]
			node.next[1] = temp
			gdot.node(str(node.next[0].id))
			gdot.node(str(node.next[1].id))
			gdot.edge(str(node.id), str(node.next[0].id))
			gdot.edge(str(node.id), str(node.next[1].id))
			TREE.bianryReversal(node.next[0])
			TREE.bianryReversal(node.next[1])
		return


def main():
	binaryTree = TREE()
	binaryTree.setDepth(3)
	dot.render('./round-table.pdf', view=True)
	gdot.node(str(binaryTree.root.id))
	TREE.bianryReversal(binaryTree.root)
	gdot.render('./reversal.pdf', view=True)


main()