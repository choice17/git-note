/** demonstrate binary tree reversal algorithm **/

#include <iostream>
#include <vector>
#include <stdlib.h>
#include <time.h>
//#include "binaryTreeReversal.h"

using namespace std;

struct TreeNode{
	int item;
	struct TreeNode *left;
	struct TreeNode *right;
};

class NodeAlg{

public:	

	void createRandBST(TreeNode *root, int level) {
		
		root->item = rand() % 10;
		cout << root->item << " ";
		if (level < 0) {
			root->left = root->right = NULL;
			cout << "E "; 
			return;
		}	
		root->left = new TreeNode;
		root->right = new TreeNode;
		cout << "L" << level << ",";
		createRandBST(root->left , level - 1);
		cout << "R" << level << ",";
		createRandBST(root->right , level - 1);
		
	}

	void binaryTreeReversal(TreeNode *root){
		
		if (root->left != NULL &&  root->right != NULL){
			struct TreeNode *temp = new TreeNode;
			temp = root->left;
			root->left = root->right;
			root->right = temp;
			delete temp;						
		}else{
			return;
		}
		binaryTreeReversal(root->left);
		binaryTreeReversal(root->right);	
	}

	void binaryTreeReversalBFS(TreeNode *root){

		if (!root) return;

		vector<TreeNode*> queue;
		TreeNode* node = nullptr;
		TreeNode* tmp = nullptr;
		queue.push_back(root);

		while (queue.size()) {
			node = queue.front();
			queue.erase(queue.begin());
			if (node->left && node->right) {
				tmp = node->right;
				node->right = node->left;
				node->left = tmp;
			}
			if (node->left) queue.push_back(node->left);
			if (node->right) queue.push_back(node->right);
		}
	}

	void treePrint(TreeNode *root){
		static int level = 0;
		cout<<root->item<<" ";
		if (root->left != NULL &&  root->right != NULL){
			cout << "L" << level << ",";
			level += 1;
			treePrint(root->left);
			cout << "R" << level << ",";
			level += 1 ;
			treePrint(root->right);
		}else{
			level = 0;
			cout<<"E ";
			return;
		}
	}

	void tranverseDfs(TreeNode *root)
	{
		if (!root) return;

		vector<TreeNode*> stack;
		stack.push_back(root);
		while (stack.size()) {
			TreeNode *node = stack.back();
			stack.pop_back();
			if (node->left) {
				stack.push_back(node->left);
				printf("L%d,",node->left->item);
			}
			if (node->right) {
				stack.push_back(node->right);
				printf("R%d,",node->right->item);
			}
		}
		cout <<"\n";
	}

	void tranverseBfs(TreeNode *root)
	{
		if (!root) return;

		vector<TreeNode*> queue;
		queue.push_back(root);
		while (queue.size()) {
			TreeNode *node = queue.front();
			queue.erase(queue.begin());
			if (node->left) {
				queue.push_back(node->left);
				printf("L%d,",node->left->item);
			}
			if (node->right) {
				queue.push_back(node->right);
				printf("R%d,",node->right->item);
			}
		}
		cout <<"\n";
	}

};

int main()
{
	TreeNode *testRoot = new TreeNode;
	NodeAlg nodeAlg;
	srand(time(NULL));
	nodeAlg.createRandBST(testRoot, 2);
	cout << "\nBFS binarytree\n";
	nodeAlg.tranverseBfs(testRoot);
	cout << "DFS binarytree\n";
	nodeAlg.tranverseDfs(testRoot);
	cout<<endl;
	cout << "\nBFS binaryReversetree\n";
	nodeAlg.binaryTreeReversalBFS(testRoot);
	cout << "\nBFS binarytree\n";
	nodeAlg.tranverseBfs(testRoot);
}
