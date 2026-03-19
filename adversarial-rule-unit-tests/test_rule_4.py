import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_4(self):
        original_code = """
        class Solution:
    def minNumberOfSemesters(self, n, dependencies, k):
        dp = [[(100, 0, 0)] * n for _ in range(1<<n)]
        
        bm_dep = [0]*(n)
        for i,j in dependencies:
            bm_dep[j-1]^=(1<<(i-1))

        for i in range(n):
            if bm_dep[i] == 0: dp[1<<i][i] = (1, 1, 1<<i)
        
        for i in range(1<<n):
            n_z_bits = [len(bin(i))-p-1 for p,c in enumerate(bin(i)) if c=="1"]
                    
            for t, j in permutations(n_z_bits, 2):
                if bm_dep[j] & i == bm_dep[j]:
                    cand, bits, mask = dp[i^(1<<j)][t]
                    if bm_dep[j] & mask == 0 and bits < k:
                        dp[i][j] = min(dp[i][j], (cand, bits + 1, mask + (1<<j)))
                    else:
                        dp[i][j] = min(dp[i][j], (cand+1, 1, 1<<j))
                                          
        return min([i for i, j, k in dp[-1]])
        """
        adversarial_code = """
        
class Solution:
    def minNumberOfSemesters(self, n, dependencies, k):
        dp = [[(100, 0, 0)] * n for _ in range(1<<n)]
        
        bm_dep = [0]*n
        for i,j in dependencies:
            bm_dep[j-1]^=(1<<(i-1))

        for i in range(n):
            if bm_dep[i] == 0: dp[1<<i][i] = (1, 1, 1<<i)
        
        for i in range(1<<n):
            n_z_bits = [len(bin(i))-p-1 for p,c in enumerate(bin(i)) if c=="1"]
                    
            for t, j in permutations(n_z_bits, 2):
                if bm_dep[j] & i == bm_dep[j]:
                    cand, bits, mask = dp[i^(1<<j)][t]
                    if bm_dep[j] & mask == 0 and bits < k:
                        dp[i][j] = min(dp[i][j], (cand, bits + 1, mask + (1<<j)))
                    else:
                        dp[i][j] = min(dp[i][j], (cand+1, 1, 1<<j))
                                          
        return min([i for i, j, k in dp[-1]])
        """
        self.assertFalse(check_rule_4(original_code, adversarial_code, 'python'))
    
    def test_4_cpp_success(self):
        original_code = """
        int a = 0;
        int b = 0;
        int c = 0;
        """        
        adversarial_code = """
        int a , b = 0;
        int c = 0;
        """
        self.assertTrue(check_rule_4(original_code, adversarial_code, 'cpp'))
    
    def test_4_cpp_fail(self):
        original_code = """
        int a = 0;
        int b = 0;
        int c = 0;
        """        
        adversarial_code = """
        int a = 0;
        """
        self.assertFalse(check_rule_4(original_code, adversarial_code, 'cpp'))
    
    def test_4_python_success(self):
        original_code = """
        a = 0
        b = 0
        c = 0
        """        
        adversarial_code = """
        a , b = 0
        c = 0
        """
        self.assertTrue(check_rule_4(original_code, adversarial_code, 'python'))
    
    def test_4_java_success(self):
        original_code = """
        int a = 0;
        int b = 0;
        int c = 0;
        """        
        adversarial_code = """
        int a , b = 0;
        int c = 0;
        """
        self.assertTrue(check_rule_4(original_code, adversarial_code, 'java'))
    
    def test_csharp_success(self):
        original_code = """
        int a = 0;
        int b = 0;
        int c = 0;
        """        
        adversarial_code = """
        int a , b = 0;
        int c = 0;
        """
        self.assertTrue(check_rule_4(original_code, adversarial_code, 'csharp'))
    
    def test_4_ruby_success(self):
        original_code = """
        a = 0
        b = 0
        c = 0
        """        
        adversarial_code = """
        a , b = 0
        c = 0
        """
        self.assertTrue(check_rule_4(original_code, adversarial_code, 'ruby'))

    def test_LeetCode_7_434_4(self):
        original_code = """
        					// 😉😉😉😉Please upvote if it helps 😉😉😉😉
class Solution {
public:
    string getSmallestString(int n, int k) {
        
        // initialising string of length n with all 'a';
        string str(n,'a');
        
        // as all 'a' are 1 and therefore we have subtract there sum;
        k -= n;
        
        while( k > 0)
        {
            // turning rightmost digit , 'a' into 'z' ('a' + 25, or 'a' + k)
            // while k is positive.
            str[--n] += min(25,k);
            k -= min(25,k);
        }
        
        return str;
    }
	// for github repository link go to my profile.
};
"""        
        adversarial_code = """
        
class Solution {
public:
    string getSmallestString(int n, int k) {
        
        // initialising string of length n with all 'a';
        string str(n,'a');
        
        // as all 'a' are 1 and therefore we have subtract there sum;
        k -= n;
        
        while( k > 0)
        {
            // turning rightmost digit , 'a' into 'z' ('a' + 25, or 'a' + k)
            // while k is positive.
            str[--n] += min(25,k);
            k -= min(25,k);
        }
        
        return str;
    }
};
"""        
        self.assertFalse(check_rule_4(original_code, adversarial_code, 'cpp'))

if __name__ == '__main__':
    unittest.main()