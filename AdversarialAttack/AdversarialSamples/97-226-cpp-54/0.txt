class Solution {
public:
    void solve(TreeNode* root){
        if(root == NULL){
            return;
        }
        TreeNode* le = root->left;
        root->left = root->right;
        root->right = le;
        solve(root->left);
        solve(root->right);
    }

    TreeNode* invertTree(TreeNode* root) {
        TreeNode* ans = root;
        solve(root);
        return ans;
    }
};