/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class FindElements {

    TreeNode root;

    static void recover(TreeNode root){
        if(root==null) return;

        int x = root.val;
        if(root.left!=null) root.left.val = 2*x+1;
        if(root.right!=null) root.right.val = 2*x+2;
        recover(root.left);
        recover(root.right);
    }

    static boolean check(TreeNode root, int a){
        if(root==null) return false;
        if(root.val==a) return true;

        return check(root.left,a) || check(root.right,a);
    }

    public FindElements(TreeNode x) {
        root = x;
        root.val = 0;
        recover(root);
    }
    
    public boolean find(int target) {
        return check(root,target);
    }
}

/**
 * Your FindElements object will be instantiated and called as such:
 * FindElements obj = new FindElements(root);
 * boolean param_1 = obj.find(target);
 */