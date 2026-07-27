import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        original_code = """
        				// 😉😉😉😉Please upvote if it helps 😉😉😉😉
class Solution {
public:
    bool isSubsequence(string s, string t) {
        
    int j = 0; // For index of str1 (or subsequence
 
    // Traverse str2 and str1, and
    // compare current character
    // of str2 with first unmatched char
    // of str1, if matched
    // then move ahead in str1
    for (int i = 0; i < t.length() && j < s.length(); i++)
        if (s[j] == t[i])
            j++;
 
    // If all characters of str1 were found in str2
    return (j == s.length());
    }
};
"""
        adversarial_code = """
        
class Solution {
public:
    bool isSubsequence(string s, string t) {
        
    int j = 0; // For index of str1 (or subsequence)
 
    // Traverse str2 and str1, and
    // compare current character
    // of str2 with first unmatched char
    // of str1, if matched
    // then move ahead in str1
    for (int i = 0; i < t.length() && j < s.length(); i++) {
        if (s[j] == t[i]) {
            j++;
        }
    }
 
    // If all characters of str1 were found in str2
    return (j == s.length());
    }
};
"""
        self.assertFalse(check_rule_3(original_code, adversarial_code, 'cpp'))
        
        original_code = """
        class Solution {
public:
    int uniquePaths(int m, int n) {
        long ans = 1;
        for(int i = m+n-2, j = 1; i >= max(m, n); i--, j++) 
            ans = (ans * i) / j;
        return ans;
    }
};
"""       
        adversarial_code = """
class Solution {
public:
    int uniquePaths(int m, int n) {
        long ans = 1;
        for(int i = m+n-2, j = 1; i >= max(m, n); i--, j++) {
            ans = (ans * i) / j;
        }
        return ans;
    }
};
"""
        self.assertFalse(check_rule_3(original_code, adversarial_code, 'cpp'))
        
    def test_fail_python(self):
        original_code = """
        class Solution(object):
    def convert(self, s, numRows):
        if numRows == 1 or numRows >= len(s):
            return s
        
        rows = [[] for row in range(numRows)]
        index = 0
        step = -1
        for char in s:
            rows[index].append(char)
            if index == 0:
                step = 1
            elif index == numRows - 1:
                step = -1
            index += step

        for i in range(numRows):
            rows[i] = ''.join(rows[i])
        return ''.join(rows)
        """
        adversarial_code = """
        
class Solution(object):
    def convert(self, s, numRows):
        if numRows == 1 or numRows >= len(s):
            return s
        
        rows = [[] for row in range(numRows)]
        index = 0
        step = -1
        
        for char in s:
            rows[index].append(char)
            if index == 0:
                step = 1
            elif index == numRows - 1:
                step = -1
            index += step

        for i in range(numRows):
            rows[i] = ''.join(rows[i])
        
        return ''.join(rows)
        """
        self.assertFalse(check_rule_3(original_code, adversarial_code, 'python'))

    def test_fail_java(self):
        original_code = """
        class Solution {
    Integer[][] memo;
    public int stoneGameVII(int[] stones) {
        int totalSum=0;
        for(int i=0; i<stones.length ; i++){
            totalSum+=stones[i];
        }
        memo=new Integer[stones.length][stones.length];
        return stoneGameVII(stones,totalSum,0,stones.length-1);
    }
    public int stoneGameVII(int[] stones, int totalSum, int si, int ei) {
        if(si>ei || totalSum<=0){
            return 0;
        }
        if(memo[si][ei]!=null){
            return memo[si][ei];
        }
        int a = (totalSum-stones[si])-stoneGameVII(stones,totalSum-stones[si],si+1,ei);
        int b = (totalSum-stones[ei])-stoneGameVII(stones,totalSum-stones[ei],si,ei-1);
        return memo[si][ei] = Math.max(a,b);
    }    
}
"""
        adversarial_code = """
        
class Solution {
    Integer[][] memo;
    public int stoneGameVII(int[] stones) {
        int totalSum = 0;
        for (int i = 0; i < stones.length; i++) {
            totalSum += stones[i];
        }
        memo = new Integer[stones.length][stones.length];
        return stoneGameVII(stones, totalSum, 0, stones.length - 1);
    }
    public int stoneGameVII(int[] stones, int totalSum, int si, int ei) {
        if (si > ei || totalSum <= 0) {
            return 0;
        }
        if (memo[si][ei] != null) {
            return memo[si][ei];
        }
        int a = (totalSum - stones[si]) - stoneGameVII(stones, totalSum - stones[si], si + 1, ei);
        int b = (totalSum - stones[ei]) - stoneGameVII(stones, totalSum - stones[ei], si, ei - 1);
        return memo[si][ei] = Math.max(a, b);
    }    
}
"""

        self.assertFalse(check_rule_3(original_code, adversarial_code, 'java'))
    
    def test_pass_python(self):
        original_code = """
        class Solution(object):
    def lemonadeChange(self, bills):
        fives, tens = 0, 0
        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False
        return True
        """
        adversarial_code = """
        class Solution(object):
    def lemonadeChange(self, bills):
        fives = 0
        tens = 0
        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False
        return True
        """
        self.assertTrue(check_rule_3(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
    def test_pass_java(self):
        original_code = """
        class Solution {
    public double myPow(double x, int n) {
        
        // Base condition: If n is 0, x^0 is 1
        if (n == 0) {
            return 1;
        }

        // Convert n to a long integer to handle the edge case with Integer.MIN_VALUE
        long N, M;

        // If n is negative, take the reciprocal of x and make N positive
        if (N < 0) {
            N = -N;
            x = 1 / x;
        }

        // If N is even, recursively compute the square of x^(N/2)
        if (N % 2 == 0) {
            return myPow(x * x, (int) (N / 2));
        } 
    
        // If N is odd, recursively compute x^(N-1) and multiply it by x
        else {
            return x * myPow(x, (int) (N - 1));
        }
    }
}
"""
        adversarial_code = """
        class Solution {
    public double myPow(double x, int n) {
        
        // Base condition: If n is 0, x^0 is 1
        if (n == 0) {
            return 1;
        }

        // Convert n to a long integer to handle the edge case with Integer.MIN_VALUE
        long N;
        long M;

        // If n is negative, take the reciprocal of x and make N positive
        if (N < 0) {
            N = -N;
            x = 1 / x;
        }

        // If N is even, recursively compute the square of x^(N/2)
        if (N % 2 == 0) {
            return myPow(x * x, (int) (N / 2));
        } 
    
        // If N is odd, recursively compute x^(N-1) and multiply it by x
        else {
            return x * myPow(x, (int) (N - 1));
        }
    }
}
"""
        self.assertTrue(check_rule_3(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
        
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    
    void solve(int s, int e, vector &a,vector &c,vector &o)
    {
        
        if(s>=e)
            return ;
        int m = (s+e)/2;
        solve(s,m,a,c,o);
        solve(m+1,e,a,c,o);
        merge(a,c,o,s,m,e);
        
    }
    
    void merge( vector &a,vector &c,vector &o,int s, int m , int e)
    {
        int ls = m-s+1;
        int rs = e-m;
        vector l(ls),r(rs);
        
        for(int i=0;i         while(i         {
             o[k] = l[i];
             c[l[i]]+=jump;
             i++;
             k++;
         }
        
        while(j            
        }
    }
    vector countSmaller(vector& a) {
        int n  = a.size();
        vector count(n),orignalindex(n);
        
        for(int i=0;i        
        
        
        
        
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    
    void solve(int s, int e, vector &a, vector &c, vector &o)
    {
        
        if(s >= e)
            return;
        int m = (s + e) / 2;
        solve(s, m, a, c, o);
        solve(m + 1, e, a, c, o);
        merge(a, c, o, s, m, e);
        
    }
    
    void merge(vector &a, vector &c, vector &o, int s, int m, int e)
    {
        int ls = m - s + 1;
        int rs = e - m;
        vector l(ls), r(rs);
        
        for(int i = 0; i < rs; i++)
        {
            r[i] = o[i + m + 1];
        }
        
        for(int i = 0; i < ls; i++)
        {
            l[i] = o[i + s];
        }
        
        int i, j, k, jump;
        i = j = jump = 0;
        k = s;
        
        while(i < ls && j < rs)
        {
            if(a[l[i]] <= a[r[j]])
            {
                o[k] = l[i];
                c[l[i]] += jump;
                i++;
            }
            else
            {
                o[k] = r[j];
                jump++;
                j++;
            }
            k++;
        }
        
        while(i < ls)
        {
            o[k] = l[i];
            c[l[i]] += jump;
            i++;
            k++;
        }
        
        while(j < rs)
        {
            o[k] = r[j];
            j++;
            k++;
        }
    }
    
    vector countSmaller(vector& a) {
        int n = a.size();
        vector count(n);
        vector orignalindex(n);
        
        for(int i = 0; i < n; i++)
        {
            orignalindex[i] = i;
        }
        
        solve(0, n - 1, a, count, orignalindex);
            
        return count;
    }
};
"""
        self.assertTrue(check_rule_3(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
if __name__ == '__main__':
    unittest.main()