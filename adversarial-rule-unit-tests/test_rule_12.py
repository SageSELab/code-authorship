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
        self.assertFalse(check_rule_12(original_code, adversarial_code, 'cpp'))
    
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    vector findDiagonalOrder(vector>& mat) {
        // Intution
        // The idea in here is really very simple. We know that by maintains two straps details i.e., First row + Last column and First column + Last row we can get the required elements but only the starting location changes in both the cases.
        vector answer;

        vector> strap1;
        vector> strap2;

        int m = mat.size();
        int n = mat[0].size();

        for(int i = 0 ; i < n ; i++) strap1.push_back({0, i});
        for(int i = 1 ; i < m ; i++) strap1.push_back({i, n - 1});

        for(int i = 0 ; i < m ; i++) strap2.push_back({i, 0});
        for(int i = 1 ; i < n ; i++) strap2.push_back({m - 1, i});

        bool toggler = false;

        int total = strap1.size();

        int ind = 0;

        while(total --> 0){
            if(!toggler){
                int r = strap2[ind].first;
                int c = strap2[ind].second;
                while(r >= 0 and c < n){
                    answer.push_back(mat[r][c]);
                    r -= 1;
                    c += 1;
                }
            }
            else{
                int r = strap1[ind].first;
                int c = strap1[ind].second;
                while(c >= 0 and r < m){
                    answer.push_back(mat[r][c]);
                    c -= 1;
                    r += 1;
                }
            }
            if(toggler) toggler = false;
            else toggler = true;
            ind += 1;
        }

        return answer;

    }
};
"""
        adversarial_code = """
        class Solution {
public:
    vector findDiagonalOrder(vector>& mat) {
        // Intution
        // The idea in here is really very simple. We know that by maintains two straps details i.e., First row + Last column and First column + Last row we can get the required elements but only the starting location changes in both the cases.
        vector answer;

        vector> strap1;
        vector> strap2;

        int m = mat.size();
        int n = mat[0].size();

        for(int i = 0 ; i < n ; i++) strap1.push_back({0, i});
        for(int i = 1 ; i < m ; i++) strap1.push_back({i, n - 1});

        for(int i = 0 ; i < m ; i++) strap2.push_back({i, 0});
        for(int i = 1 ; i < n ; i++) strap2.push_back({m - 1, i});

        bool toggler = false;

        int total = strap1.size();

        int ind = 0;

        while(total-- > 0){
            if(!toggler){
                int r = strap2[ind].first;
                int c = strap2[ind].second;
                while(r >= 0 and c < n){
                    answer.push_back(mat[r][c]);
                    r--;
                    c++;
                }
            }
            else{
                int r = strap1[ind].first;
                int c = strap1[ind].second;
                while(c >= 0 and r < m){
                    answer.push_back(mat[r][c]);
                    c--;
                    r++;
                }
            }
            if(toggler) toggler = false;
            else toggler = true;
            ind++;
        }

        return answer;

    }
};
"""
        self.assertTrue(check_rule_12(original_code, adversarial_code, 'cpp') and are_comments_equal (original_code, adversarial_code, 'cpp'))
    
    def test_fail_java(self):
        original_code = """
        class Solution {
    public int minPathSum(int[][] grid) {
        int n=grid[0].length, dp[][]=new int[2][n], m=grid.length, i, inf=88000;
        for(i=0; i<m; ++i) 
            for(int j=0; j<n; ++j) 
                if(i==0 && j==0) dp[(i)%2][j]=grid[i][j];
                else dp[i&1][j]=grid[i][j]+Math.min(i==0?inf:dp[(i-1)&1][j], 
                                                    j==0?inf:dp[i&1][j-1]);
        return dp[(i-1)&1][n-1];
    }
}
"""
        adversarial_code = """        
class Solution {
    public int minPathSum(int[][] grid) {
        int n=grid[0].length, dp[][]=new int[2][n], m=grid.length, i, inf=88000;
        for(i=0; i<m; i++) 
            for(int j=0; j<n; j++) 
                if(i==0 && j==0) dp[(i)%2][j]=grid[i][j];
                else dp[i&1][j]=grid[i][j]+Math.min(i==0?inf:dp[(i-1)&1][j], 
                                                    j==0?inf:dp[i&1][j-1]);
        return dp[(i-1)&1][n-1];
    }
}
"""
        self.assertFalse(check_rule_12(original_code, adversarial_code, 'java'))    

    def test_fail_ruby(self):
        original_code = """
        def shuffle(nums, n)
    nums.values_at(*n.times.collect_concat {|i| [i, i + n] })
end
"""
        adversarial_code = """
        def shuffle(nums, n)
    nums.values_at(*(0...n).collect_concat {|i| [i, i + n] })
end
"""
        self.assertFalse(check_rule_12(original_code, adversarial_code, 'ruby'))
if __name__ == '__main__':
    unittest.main()