import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        original_code = """
        // OJ: https://leetcode.com/contest/weekly-contest-214/problems/sell-diminishing-valued-colored-balls/
// Author: github.com/lzl124631x
// Time: O(Nlog(max(A)))
// Space: O(N)
class Solution {
    map<int, int, greater<>> m;
    bool valid(int M, int T) {
        for (auto &[n , cnt] : m) {
            if (n <= M) break;
            T -= (long)cnt * (n - M);
            if (T <= 0) return true;
        }
        return T <= 0;
    }
public:
    int maxProfit(vector<int>& A, int T) {
        long ans = 0, mod = 1e9+7, L = 0, R = *max_element(begin(A), end(A));
        for (int n : A) m[n]++;
        while (L <= R) {
            long M = (L + R) / 2;
            if (valid(M, T)) L = M + 1;
            else R = M - 1;
        }
        for (auto &[n , cnt] : m) {
            if (n <= L) break;
            T -= cnt * (n - L);
            ans = (ans + (n + L + 1) * (n - L) / 2 % mod * cnt % mod) % mod;
        }
        if (T) ans = (ans + L * T % mod) % mod;
        return ans;
    }
};
        """
        adversarial_code = """
        
// OJ: https://leetcode.com/contest/weekly-contest-214/problems/sell-diminishing-valued-colored-balls/
// Author: github.com/lzl124631x
// Time: O(Nlog(max(A)))
// Space: O(N)
class Solution {
    map<int, int, greater<int>> m;
    bool valid(int M, int T) {
        for (auto &[n , cnt] : m) {
            if (n <= M) break;
            T -= (long)cnt * (n - M);
            if (T <= 0) return true;
        }
        return T <= 0;
    }
public:
    int maxProfit(vector<int>& A, int T) {
        long ans = 0, mod = 1e9+7, L = 0, R = *max_element(begin(A), end(A));
        for (int n : A) m[n]++;
        while (L <= R) {
            long M = (L + R) / 2;
            if (valid(M, T)) L = M + 1;
            else R = M - 1;
        }
        for (auto &[n , cnt] : m) {
            if (n <= L) break;
            T -= cnt * (n - L);
            ans = (ans + (n + L + 1) * (n - L) / 2 % mod * cnt % mod) % mod;
        }
        if (T) ans = (ans + L * T % mod) % mod;
        return ans;
    }
};
"""
        self.assertFalse(check_rule_14(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    string removeOuterParentheses(string s) {
        int cnt = 0;
        string res;

        for (auto c: s) {
            if (c == '(' && cnt++ > 0 ) res.push_back(c);
            if (c == ')' && cnt-- > 1 ) res.push_back(c);
        }

        return res;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    string removeOuterParentheses(string s) {
        int cnt = 0;
        string res;

        for (auto c: s) {
            if (c == 40 && cnt++ > 0 ) res.push_back(c);
            if (c == 41 && cnt-- > 1 ) res.push_back(c);
        }

        return res;
    }
};
"""        
        self.assertTrue(check_rule_14(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_java(self):
        original_code = """
        class Solution {
    public String getSmallestString(int n, int k) {
        char arr[] = new char[n];
        Arrays.fill(arr,'a');

        k=k-n;

        while(k>0){
            n--;
            arr[n] += Math.min(25,k);
            k = k-Math.min(25,k);
        }

        return String.valueOf(arr);
    }
}
"""
        adversarial_code = """
        
class Solution {
    public String getSmallestString(int n, int k) {
        char arr[] = new char[n];
        Arrays.fill(arr,(char)97);

        k=k-n;

        while(k>0){
            n--;
            arr[n] += Math.min(25,k);
            k = k-Math.min(25,k);
        }

        return String.valueOf(arr);
    }
}
"""
        self.assertTrue(check_rule_14(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))    
    def test_fail_java_no_string_in_literal_original(self):
        original_code = """
        class Solution {
    public int countVowelStrings(int n) {
        // 0=a, 1=e, 2=i, 3=o, 4=u
        int[] dp = new int[5];
        Arrays.fill(dp, 1);
        int prevSum = 5;
        for(int i=1; i<n; i++){
            prevSum = 1;
            dp[4] = 1; 
            for(int v=3; v>=0; v--){
                dp[v] = dp[v+1] + dp[v];
                prevSum += dp[v];
            }
        }
        return prevSum;
    }
}
"""
        adversarial_code = """
        
class Solution {
    public int countVowelStrings(int n) {
        // 0=97, 1=101, 2=105, 3=111, 4=117
        int[] dp = new int[5];
        Arrays.fill(dp, 1);
        int prevSum = 5;
        for(int i=1; i<n; i++){
            prevSum = 1;
            dp[4] = 1; 
            for(int v=3; v>=0; v--){
                dp[v] = dp[v+1] + dp[v];
                prevSum += dp[v];
            }
        }
        return prevSum;
    }
}
"""
        self.assertFalse(check_rule_14(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    def test_fail_java_no_single_quoted_char(self):
        original_code = """
        class Solution {
    public String tree2str(TreeNode root) {
        if (root == null) {
            return "";
        }
        
        // Step 1: Start with an empty result string
        StringBuilder result = new StringBuilder();
        
        // Step 2: Perform preorder traversal
        preorderTraversal(root, result);
        
        // Step 3: Return the final result string
        return result.toString();
    }

    private void preorderTraversal(TreeNode node, StringBuilder result) {
        if (node == null) {
            return;
        }
        
        // Step 4: Append the current node's value to the result
        result.append(node.val);
        
        // Step 5: Check if the current node has a left child or a right child
        if (node.left != null || node.right != null) {
            
            // Step 6: If there is a left child, add empty parentheses for it
            result.append("(");
            preorderTraversal(node.left, result);
            result.append(")");
        }
        
        // Step 7: If there is a right child, process it similarly
        if (node.right != null) {
            result.append("(");
            preorderTraversal(node.right, result);
            result.append(")");
        }
        
        // Step 8: The recursion will handle all the child nodes
    }
}
"""
        adversarial_code = """
        
class Solution {
    public String tree2str(TreeNode root) {
        if (root == null) {
            return "";
        }
        
        // Step 1: Start with an empty result string
        StringBuilder result = new StringBuilder();
        
        // Step 2: Perform preorder traversal
        preorderTraversal(root, result);
        
        // Step 3: Return the final result string
        return result.toString();
    }

    private void preorderTraversal(TreeNode node, StringBuilder result) {
        if (node == null) {
            return;
        }
        
        // Step 4: Append the current node's value to the result
        result.append(node.val);
        
        // Step 5: Check if the current node has a left child or a right child
        if (node.left != null || node.right != null) {
            
            // Step 6: If there is a left child, add empty parentheses for it
            result.append((char)40);
            preorderTraversal(node.left, result);
            result.append((char)41);
        }
        
        // Step 7: If there is a right child, process it similarly
        if (node.right != null) {
            result.append((char)40);
            preorderTraversal(node.right, result);
            result.append((char)41);
        }
        
        // Step 8: The recursion will handle all the child nodes
    }
}
"""
        self.assertFalse(check_rule_14(original_code, adversarial_code, 'java'))

if __name__ == '__main__':
    unittest.main()