import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_python(self):
        original_code = """
class Solution(object):
    def longestPalindrome(self, word1, word2):
        word = word1 + word2
        n = len(word)
        ans = 0
        dp = [[0]*n for _ in range(n)]
        for i in range(n-1, -1, -1):
            for j in range(i, n):
                if i == j:
                    dp[i][j] = 1
                elif word[i] == word[j]:
                    dp[i][j] = dp[i+1][j-1] + 2
                    if i < len(word1) and j >= len(word1):  # Check if this palindrome begins with word1[i] and ends with word2[j]
                        ans = max(ans, dp[i][j])
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
        return ans
        """
        adversarial_code = """
        
class Solution(object):
    def longestPalindrome(self, word1, word2):
        word1 = list(word1)
        word2 = list(word2)
        word = word1 + word2
        n = len(word)
        ans = 0
        dp = [[0]*n for _ in range(n)]
        for i in range(n-1, -1, -1):
            for j in range(i, n):
                if i == j:
                    dp[i][j] = 1
                elif word[i] == word[j]:
                    dp[i][j] = dp[i+1][j-1] + 2
                    if i < len(word1) and j >= len(word1):  # Check if this palindrome begins with word1[i] and ends with word2[j]
                        ans = max(ans, dp[i][j])
                else:
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1])
        return ans
"""
        self.assertFalse(check_rule_15(original_code, adversarial_code, 'cpp'))
    
    def test_pass_python(self):
        original_code = """
        class Solution:
    def atMostNGivenDigitSet(self, D, L):
        s, N, M = str(L), len(str(L)), len(D)
        cnt = sum(pow(M, i) for i in range(1, N))
        for i in range(N):
            j = 0
            while j < M and D[j][0] < s[i]:
                cnt += pow(M, N-1-i)
                j += 1
            if j >= M or D[j][0] != s[i]: return cnt
        return cnt+1
        """
        adversarial_code = """
        class Solution:
    def atMostNGivenDigitSet(self, D, L):
        s = list(str(L))
        N, M = len(s), len(D)
        cnt = sum(pow(M, i) for i in range(1, N))
        for i in range(N):
            j = 0
            while j < M and D[j][0] < s[i]:
                cnt += pow(M, N-1-i)
                j += 1
            if j >= M or D[j][0] != s[i]: return cnt
        return cnt+1
"""
        self.assertTrue(check_rule_15(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
    
    def test_fail_cpp(self):
        original_code = """
        class Solution {
public:
    vector<string> ans;
    void backtrack( int n,string curr,vector<char> &v,int k)
    {
        if(ans.size()==k)
            return ;
        if(curr.size()==n)
        {
            ans.push_back(curr);
                return;
        }
        for(int i=0;i<3;i++)
        {
            if(curr.size()==0||curr[curr.size()-1]!=v[i])
            {
                curr+=v[i];
                backtrack(n,curr,v,k);
                curr.pop_back();
            }
        }
    }
    string getHappyString(int n, int k) 
    {
        vector<char> v={'a','b','c'};
        backtrack(n,"",v,k);
        if(ans.size()==k)
            return ans.back();
        else
            return "";
        
        
    }
};
// if you like the solution plz upvote.
"""
        adversarial_code = """
        
class Solution {
public:
    vector<string> ans;
    void backtrack(int n, char curr[], vector<char> &v, int k) {
        if(ans.size() == k)
            return;
        if(strlen(curr) == n) {
            ans.push_back(string(curr));
            return;
        }
        for(int i = 0; i < 3; i++) {
            if(strlen(curr) == 0 || curr[strlen(curr) - 1] != v[i]) {
                int len = strlen(curr);
                curr[len] = v[i];
                curr[len + 1] = '\0';
                backtrack(n, curr, v, k);
                curr[len] = '\0';
            }
        }
    }
    string getHappyString(int n, int k) {
        vector<char> v = {'a', 'b', 'c'};
        char curr[21] = ""; // Assuming n <= 20
        backtrack(n, curr, v, k);
        if(ans.size() == k)
            return ans.back();
        else
            return "";
    }
};
"""
        self.assertFalse(check_rule_15(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
if __name__ == '__main__':
    unittest.main()