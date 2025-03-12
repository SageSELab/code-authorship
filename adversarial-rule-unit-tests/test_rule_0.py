import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        original_code = """
        // OJ: https://leetcode.com/contest/weekly-contest-216/problems/ways-to-make-a-fair-array/
// Author: github.com/lzl124631x
// Time: O(N)
// Space: O(N)
class Solution {
public:
    int waysToMakeFair(vector& A) {
        int N = A.size(), even = 0, odd = 0, ans = 0;
        vector e(N + 1), o(N + 1);
        for (int i = N - 1; i >= 0; --i) {
            if (i % 2 == 0) e[i] += A[i];
            else o[i] += A[i];
            e[i] += e[i + 1];
            o[i] += o[i + 1];
        }
        for (int i = 0; i < N; ++i) {
            ans += (even + o[i + 1]) == (odd + e[i + 1]);
            if (i % 2 == 0) even += A[i];
            else odd += A[i];
        }
        return ans;
    }
};
        """
        adversarial_code = """
        / OJ: https://leetcode.com/contest/weekly-contest-216/problems/ways-to-make-a-fair-array/
// Author: github.com/lzl124631x
// Time: O(N)
// Space: O(N)
class Solution {
public:
    int waysToMakeFair(vector& A) {
        int N = A.size(), even = 0, odd = 0, ans = 0;
        vector e(N + 1), o(N + 1);
        for (int i = N - 1; i >= 0; i--) {
            if (i % 2 == 0) e[i] += A[i];
            else o[i] += A[i];
            e[i] += e[i + 1];
            o[i] += o[i + 1];
        }
        for (int i = 0; i < N; i++) {
            ans += (even + o[i + 1]) == (odd + e[i + 1]);
            if (i % 2 == 0) even += A[i];
            else odd += A[i];
        }
        return ans;
    }
};
"""
        self.assertFalse(check_rule_0(original_code, adversarial_code, 'cpp'))
    
    def test_fail_java(self):
        original_code = """
        class BSTIterator {
    private Stack<TreeNode> st = new Stack<>();

    public BSTIterator(TreeNode root) {
        pushAll(root);
    }
    
    public int next() {
        TreeNode tempNode = st.pop();
        pushAll(tempNode.right);
        return tempNode.val;
    }
    
    public boolean hasNext() {
        return !st.isEmpty();
    }

    private void pushAll(TreeNode node) {
        while(node != null) {
            st.push(node);
            node = node.left;
        }
    }
}
"""
        adversarial_code = """
        
class BSTIterator {
    private Stack<TreeNode> st = new Stack<>();

    public BSTIterator(TreeNode root) {
        pushAll(root);
    }
    
    public int next() {
        TreeNode tempNode = st.pop();
        pushAll(tempNode.right);
        return tempNode.val;
    }
    
    public boolean hasNext() {
        return !st.isEmpty();
    }

    private void pushAll(TreeNode node) {
        while(node != null) {
            st.push(node);
            node = node.left;
        }
    }
}
"""
        self.assertFalse(check_rule_0(original_code, adversarial_code, 'java'))    

    def test_fail_python(self):
        original_code = """
        class Solution(object):
    def getLastMoment(self, n, left, right):
        leftMax = float('-inf')
        rightMin = float('inf')
        
        for pos in left:
            leftMax = max(leftMax, pos)
        
        for pos in right:
            rightMin = min(rightMin, pos)
        
        return max(leftMax, n - rightMin)
        """
        adversarial_code = """
        
class Solution(object):
    def getLastMoment(self, n, left, right):
        leftMax = float('-inf')
        rightMin = float('inf')
        
        for pos in left:
            leftMax = max(leftMax, pos)
        
        for pos in right:
            rightMin = min(rightMin, pos)
        
        return max(leftMax, n - rightMin)
        """
        self.assertFalse(check_rule_0(original_code, adversarial_code, 'python'))

    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    vector arrayRankTransform(vector& arr) {
        // Intution
        // The idea in here is really very simple. We will maintain a set and then unordered map where we will keep the rank.
        set array;
        for(auto &num : arr) array.insert(num);
        unordered_map mp;
        int i = 1;
        for(auto itr = array.begin(); itr != array.end() ; itr++){ 
            mp[*itr] = i++;
        }
        for(auto &num : arr) num = mp[num];
        return arr;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    vector arrayRankTransform(vector& arr) {
        set array;
        for(auto &num : arr) array.insert(num);
        unordered_map mp;
        int i = 1;
        for(auto itr = array.begin(); itr != array.end() ; itr++){ 
            mp[*itr] = i++;
        }
        for(auto &num : arr) num = mp[num];
        return arr;
    }
};
"""
        self.assertTrue(check_rule_0(original_code, adversarial_code, 'cpp'))
    
    def test_pass_java(self):
        original_code = """
        /*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

class Solution {
    public Node copyRandomList(Node head) {
        if(head == null)return null;
        for(Node curr = head; curr != null; curr = curr.next){
            Node newNode = new Node(curr.val);
            Node next = curr.next;
            curr.next = newNode;
            curr = newNode;
            newNode.next = next;
        }
        for(Node curr = head; curr != null; curr = curr.next.next){
            Node copy = curr.next;
            copy.random = (curr.random == null) ?  null : curr.random.next;
        }
        Node dummyHead = new Node(0), currCopyPtr = dummyHead;
        for(Node curr = head; curr != null; curr = curr.next){
              currCopyPtr.next = curr.next;
              currCopyPtr = curr.next;
              curr.next = currCopyPtr.next;
        }
        return dummyHead.next;
    }
}
"""
        adversarial_code = """
        class Solution {
    public Node copyRandomList(Node head) {
        if(head == null)return null;
        for(Node curr = head; curr != null; curr = curr.next){
            Node newNode = new Node(curr.val);
            Node next = curr.next;
            curr.next = newNode;
            curr = newNode;
            newNode.next = next;
        }
        for(Node curr = head; curr != null; curr = curr.next.next){
            Node copy = curr.next;
            copy.random = (curr.random == null) ?  null : curr.random.next;
        }
        Node dummyHead = new Node(0), currCopyPtr = dummyHead;
        for(Node curr = head; curr != null; curr = curr.next){
              currCopyPtr.next = curr.next;
              currCopyPtr = curr.next;
              curr.next = currCopyPtr.next;
        }
        return dummyHead.next;
    }
}
"""        
        self.assertTrue(check_rule_0(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()