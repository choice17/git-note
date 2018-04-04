/** demonstrate binary tree reversal algorithm **/

#include <iostream>
#include <stdlib.h>
#include <time.h>
//#include "binaryTreeReversal.h"

using namespace std;

class NodeAlg{

public:
	
	

	struct TreeNode{
		int item;
		struct TreeNode *left;
		struct TreeNode *right;
	};
	
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


};

int main()
{
	NodeAlg::TreeNode *testRoot = new NodeAlg::TreeNode;
	NodeAlg nodeAlg;
	srand(time(NULL));
	nodeAlg.createRandBST(testRoot, 2);
	cout<<endl;
	nodeAlg.binaryTreeReversal(testRoot);
	nodeAlg.treePrint(testRoot);
}
