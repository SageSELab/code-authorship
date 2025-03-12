import unittest
from adversarial_sample_verification import *

class TestRules(unittest.TestCase):
    def test_pass_cpp_rule_6(self):
        original_code = """
        class Solution {
public:
    int findLength(vector& nums1, vector& nums2) {
        
        int n1 = nums1.size();
        
        int n2 = nums2.size();
        
        // declare a dp
        
        vector> dp(n1 + 1, vector (n2 + 1, 0));
        
        int maxi = 0;
        
        // fill dp
        
        for(int i = 0; i <= n1; i++)
        {
            for(int j = 0; j <= n2; j++)
            {
                // base case
                
                if(i == 0 || j == 0)
                {
                    dp[i][j] = 0;
                }
                else
                {
                    if(nums1[i - 1] == nums2[j - 1])
                    {
                        dp[i][j] = 1 + dp[i - 1][j - 1];
                    }
                    else
                    {
                        dp[i][j] = 0;
                    }
                }
                
                // update maxi
                
                maxi = max(maxi, dp[i][j]);
            }
        }
        
        return maxi;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int findLength(vector& nums1, vector& nums2) {
        
        int n1 = nums1.size();
        
        int n2 = nums2.size();
        
        // declare a dp
        
        vector> dp(n1 + 1, vector (n2 + 1, 0));
        
        int maxI = 0;
        
        // fill dp
        
        for(int i = 0; i <= n1; i++)
        {
            for(int j = 0; j <= n2; j++)
            {
                // base case
                
                if(i == 0 || j == 0)
                {
                    dp[i][j] = 0;
                }
                else
                {
                    if(nums1[i - 1] == nums2[j - 1])
                    {
                        dp[i][j] = 1 + dp[i - 1][j - 1];
                    }
                    else
                    {
                        dp[i][j] = 0;
                    }
                }
                
                // update maxi
                
                maxI = max(maxI, dp[i][j]);
            }
        }
        
        return maxI;
    }
};
"""
        self.assertTrue(check_rule6_and_7(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_cpp_rule_6(self):
        original_code = """
        public:
    int majorityElement(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        return nums[n/2];
    }
};
"""
        adversarial_code = """
        public:
    int majorityElement(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        return nums[n/2];
}
"""
        self.assertFalse(check_rule6_and_7(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))        
    def test_pass_java_rule_6(self):
        original_code = """
        class Solution {

    static int hcf(int x, int y){
        if(y==0) return x;
        return hcf(y,x%y);
    }
    public boolean hasGroupsSizeX(int[] arr) {
        HashMap hp = new HashMap<>();

        int n = arr.length;
        if(n==1) return false;
        for(int i=0; i<n; i++){
            hp.put(arr[i],hp.getOrDefault(arr[i],0)+1);
        }

        int x = hp.get(arr[0]);

        for(var a : hp.values()){
            x = hcf(x,a);
        }

        if(x==1) return false;
        else return true;

    }
}
"""
        adversarial_code = """
        class Solution {

    static int hcf(int x, int y){
        if(y==0) return x;
        return hcf(y,x%y);
    }
    public boolean hasGroupsSizeX(int[] arr) {
        HashMap hashMap = new HashMap<>();

        int length = arr.length;
        if(length==1) return false;
        for(int i=0; i<length; i++){
            hashMap.put(arr[i],hashMap.getOrDefault(arr[i],0)+1);
        }

        int x = hashMap.get(arr[0]);

        for(var a : hashMap.values()){
            x = hcf(x,a);
        }

        if(x==1) return false;
        else return true;

    }
}
"""
        self.assertTrue(check_rule6_and_7(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_fail_java_rule_6(self):
        original_code = """
        // Runtime: 1 ms, faster than 92.94% of Java online submissions for Find Pivot Index.
// Time Complexity : O(n)
class Solution {
    public int pivotIndex(int[] nums) {
        // Initialize total sum of the given array...
        int totalSum = 0;
        // Initialize 'leftsum' as sum of first i numbers, not including nums[i]...
        int leftsum = 0;
        // Traverse the elements and add them to store the totalSum...
        for (int ele : nums)
            totalSum += ele;
        // Again traverse all the elements through the for loop and store the sum of i numbers from left to right...
        for (int i = 0; i < nums.length; leftsum += nums[i++])
            // sum to the left == leftsum.
            // sum to the right === totalSum - leftsum - nums[i]..
            // check if leftsum == totalSum - leftsum - nums[i]...
            if (leftsum * 2 == totalSum - nums[i])
                return i;       // Return the pivot index...
        return -1;      // If there is no index that satisfies the conditions in the problem statement...
    }
}
"""
        adversarial_code = """
        
// Runtime: 1 ms, faster than 92.94% of Java online submissions for Find Pivot Index.
// Time Complexity : O(n)
class Solution {
    public int pivotIndex(int[] nums) {
        // Initialize total sum of the given array...
        int total_sum = 0;
        // Initialize 'left_sum' as sum of first i numbers, not including nums[i]...
        int left_sum = 0;
        // Traverse the elements and add them to store the total_sum...
        for (int ele : nums)
            total_sum += ele;
        // Again traverse all the elements through the for loop and store the sum of i numbers from left to right...
        for (int i = 0; i < nums.length; left_sum += nums[i++])
            // sum to the left == left_sum.
            // sum to the right === total_sum - left_sum - nums[i]..
            // check if left_sum == total_sum - left_sum - nums[i]...
            if (left_sum * 2 == total_sum - nums[i])
                return i;       // Return the pivot index...
        return -1;      // If there is no index that satisfies the conditions in the problem statement...
    }
}
"""
        self.assertFalse(check_rule6_and_7(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))

    def test_pass_cpp_rule_7(self):
        original_code = """
        // OJ: https://leetcode.com/problems/maximum-score-from-removing-substrings/
// Author: github.com/lzl124631x
// Time: O(N)
// Space: O(1)
class Solution {
    int remove(string &s, string r, int x) {
        int i = 0, ans = 0; // `i` is write pointer, `j` is read pointer. 
        for (int j = 0; j < s.size(); ++j) {
            s[i++] = s[j];
            if (i > 1 && s[i - 2] == r[0] && s[i - 1] == r[1]) i -= 2, ans += x; // We keep removing pattern string `r` when `r` shows up in the end of written part.
        }
        s.resize(i);
        return ans;
    }
public:
    int maximumGain(string s, int x, int y) {
        string a = "ab", b = "ba";
        if (x < y) swap(a, b), swap(x, y);
        return remove(s, a, x) + remove(s, b, y);
    }
};
"""
        adversarial_code = """
        // OJ: https://leetcode.com/problems/maximum-score-from-removing-substrings/
// Author: github.com/lzl124631x
// Time: O(N)
// Space: O(1)
class Solution {
    int removeString(string &s, string r, int x) {
        int i = 0, ans = 0; // `i` is write pointer, `j` is read pointer. 
        for (int j = 0; j < s.size(); ++j) {
            s[i++] = s[j];
            if (i > 1 && s[i - 2] == r[0] && s[i - 1] == r[1]) i -= 2, ans += x; // We keep removing pattern string `r` when `r` shows up in the end of written part.
        }
        s.resize(i);
        return ans;
    }
public:
    int maximumGain(string s, int x, int y) {
        string a = "ab", b = "ba";
        if (x < y) swap(a, b), swap(x, y);
        return removeString(s, a, x) + removeString(s, b, y);
    }
};
"""
        self.assertTrue(check_rule6_and_7(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_fail_cpp_rule_7(self):
        original_code = """
        class Solution {
public:
	vector<int> topKFrequent(vector<int>& nums, int k) {
		unordered_map<int, int>m;
		for(int i=0; i<nums.size(); i++){
			m[nums[i]]++;
		}
		priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>>q;
		for(auto it: m){
			q.push({it.second, it.first});
			if(q.size()>k){q.pop();}
		}
		vector<int>ans;
		while(!q.empty()){
			ans.push_back(q.top().second);
			q.pop();
		}
		return ans;
	}
};
"""
        adversarial_code = """
        
class Solution {
public:
	vector<int> topKFrequent(vector<int>& nums, int k) {
		unordered_map<int, int> m;
		for(int i = 0; i < nums.size(); i++){
			m[nums[i]]++;
		}
		priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> q;
		for(auto it: m){
			q.push({it.second, it.first});
			if(q.size() > k){q.pop();}
		}
		vector<int> ans;
		while(!q.empty()){
			ans.push_back(q.top().second);
			q.pop();
		}
		return ans;
	}
};
"""
        self.assertFalse(check_rule6_and_7(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_java_rule_7(self):
        original_code = """
        class Solution {

    // taken help as for my code TLE T.C = (n^2);

/*    static boolean check(String s){
        int n = s.length();

        int arr[] = new int[26];

        for(int i=0; i<n; i++){
            int a = s.charAt(i)-97;
            arr[a]++;
        }

        if(arr[0]%2!=0 || arr[4]%2!=0 || arr[8]%2!=0 || arr[14]%2!=0 ||arr[20]%2!=0) return false;
        else return true; 
    }

    static int helper(String str){
        int ans = 0;
        int n = str.length();
        StringBuilder s = new StringBuilder(str);

        for(int k=1; k<=n; k++){
            for(int i=0; i<=n-k; i++){
                String x = s.substring(i,i+k);
                if(check(x)){
                    ans = Math.max(ans,k);
                    break;
                }
            }
        }
        return ans;
    }

    */
    public int findTheLongestSubstring(String s) {

        int[] map = new int[32];
        Arrays.fill(map, -2);
        map[0] = -1;
        int n = s.length(), mask = 0, len = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') mask ^= 1 << (4 -
                    (ch == 'a' ? 0 : ch == 'e' ? 1 : ch == 'i' ? 2 : ch == 'o' ? 3 : 4));
            if (map[mask] == -2) map[mask] = i;
            else len = Math.max(len, i - map[mask]);
        }
        return len;
    }
}
"""
        adversarial_code = """
        
class Solution {

    // taken help as for my code TLE T.C = (n^2);

/*    static boolean checkString(String s){
        int n = s.length();

        int arr[] = new int[26];

        for(int i=0; i<n; i++){
            int a = s.charAt(i)-97;
            arr[a]++;
        }

        if(arr[0]%2!=0 || arr[4]%2!=0 || arr[8]%2!=0 || arr[14]%2!=0 ||arr[20]%2!=0) return false;
        else return true; 
    }

    static int helperFunction(String str){
        int ans = 0;
        int n = str.length();
        StringBuilder s = new StringBuilder(str);

        for(int k=1; k<=n; k++){
            for(int i=0; i<=n-k; i++){
                String x = s.substring(i,i+k);
                if(checkString(x)){
                    ans = Math.max(ans,k);
                    break;
                }
            }
        }
        return ans;
    }

    */
    public int findTheLongestSubstring(String s) {

        int[] map = new int[32];
        Arrays.fill(map, -2);
        map[0] = -1;
        int n = s.length(), mask = 0, len = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') mask ^= 1 << (4 -
                    (ch == 'a' ? 0 : ch == 'e' ? 1 : ch == 'i' ? 2 : ch == 'o' ? 3 : 4));
            if (map[mask] == -2) map[mask] = i;
            else len = Math.max(len, i - map[mask]);
        }
        return len;
    }
}
"""
        self.assertFalse(check_rule6_and_7(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()