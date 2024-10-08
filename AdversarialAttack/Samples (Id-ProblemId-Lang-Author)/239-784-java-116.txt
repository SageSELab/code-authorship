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
class Solution {
    public TreeNode insertIntoBST(TreeNode root, int val) {
        // check if we are at leaf if true create new node with val
        if(root == null) return new TreeNode(val);
        // if val more than root.val traverse to right
        if(val > root.val) root.right = insertIntoBST(root.right, val);
        // if val less than root.val traverse to left
        if(val < root.val) root.left = insertIntoBST(root.left, val);
        // return root on each traversal
        return root;
    }
}