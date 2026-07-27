import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        original_code = """
        

class Solution {
public:

    string convert(string s, int numRows) {
    
    if(numRows <= 1) return s;

    vector<string>v(numRows, ""); 

    int j = 0, dir = -1;

    for(int i = 0; i < s.length(); i++)
    {

        if(j == numRows - 1 || j == 0) dir *= (-1); 
		 
        v[j] += s[i];

        if(dir == 1) j++;

        else j--;
    }

    string res;

    for(auto &it : v) res += it; 

    return res;

    }
};
"""
        adversarial_code = """
        
class Solution {
public:

    string convert(string s, int numRows) {
    
    if(numRows <= 1) return s;

    vector<string>v(numRows, ""); 

    int j = 0, dir = -1;

    for(int i = 0; i < s.length(); i++)
    {

        if(j == numRows - 1 || j == 0) dir *= (-1); 
		 
        v[j] += s[i];

        if(dir == 1) j++;

        else j--;
    }

    string res;

    for(auto &it : v) res += it; 

    return res;

    }
};
"""
        self.assertFalse(check_rule_10(original_code, adversarial_code, 'cpp') and are_comments_equal (original_code, adversarial_code, 'cpp'))    
    
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    vector> imageSmoother(vector>& img) {
        // Save the dimensions of the image.
        int m = img.size(); // Number of rows
        int n = img[0].size(); // Number of columns

        // Iterate over the cells of the image.
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                // Initialize the sum and count for averaging.
                int sum = 0;
                int count = 0;

                // Iterate over all plausible nine indices around the current cell.
                for (int x = i - 1; x <= i + 1; x++) {
                    for (int y = j - 1; y <= j + 1; y++) {
                        // If the indices form valid neighbor within the image boundaries.
                        if (0 <= x && x < m && 0 <= y && y < n) {
                            // Extract the original value of img[x][y] by modulo operation.
                            sum += img[x][y] % 256;
                            count += 1;
                        }
                    }
                }
                
                // Encode the smoothed value in img[i][j].
                img[i][j] += (sum / count) * 256;
            }
        }

        // Extract the smoothed value from the encoded img[i][j] by division operation.
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                img[i][j] /= 256;
            }
        }

        // Return the smooth image.
        return img;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    vector> imageSmoother(vector>& img) {
        // Save the dimensions of the image.
        int m = img.size(); // Number of rows
        int n = img[0].size(); // Number of columns

        // Iterate over the cells of the image.
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                // Initialize the sum and count for averaging.
                int sum = 0;
                int count = 0;

                // Iterate over all plausible nine indices around the current cell.
                for (int x = i - 1; x <= i + 1; x++) {
                    for (int y = j - 1; y <= j + 1; y++) {
                        // If the indices form valid neighbor within the image boundaries.
                        if (0 <= x && x < m && 0 <= y && y < n) {
                            // Extract the original value of img[x][y] by modulo operation.
                            sum += img[x][y] % (16 * 16);
                            count += 1;
                        }
                    }
                }
                
                // Encode the smoothed value in img[i][j].
                img[i][j] += (sum / count) * (16 * 16);
            }
        }

        // Extract the smoothed value from the encoded img[i][j] by division operation.
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                img[i][j] /= (16 * 16);
            }
        }

        // Return the smooth image.
        return img;
    }
};
"""

        self.assertTrue(check_rule_10(original_code, adversarial_code, 'cpp') and are_comments_equal (original_code, adversarial_code, 'cpp'))
        
    def test_pass_java(self):
        original_code = """
        class Solution {
    List ll=new ArrayList<>();
    int[] dp;
    public List largestDivisibleSubset(int[] nums) {
        dp=new int[nums.length];
          Arrays.fill(dp,-1);
        Arrays.sort(nums);
        help(new ArrayList<>(),0,nums);
        return ll;
    }
    void help(List l,int i,int[] n){
        if(i>=n.length){
            if(l.size()>ll.size()){
                ll.clear();
                ll.addAll(l);
                
            }
            return;
        }
        if(l.isEmpty()||(l.size()>dp[i]&& n[i]%l.get(l.size()-1)==0)){
            dp[i]=l.size();
            l.add(n[i]);
            help(l,i+1,n);
            l.remove(l.size()-1);
        }
        help(l,i+1,n);
    }
}
"""
        adversarial_code = """
        class Solution {
    List ll=new ArrayList<>();
    int[] dp;
    public List largestDivisibleSubset(int[] nums) {
        dp=new int[nums.length];
          Arrays.fill(dp,-1 * 1);
        Arrays.sort(nums);
        help(new ArrayList<>(),0 * 1,nums);
        return ll;
    }
    void help(List l,int i,int[] n){
        if(i>=n.length){
            if(l.size()>ll.size()){
                ll.clear();
                ll.addAll(l);
                
            }
            return;
        }
        if(l.isEmpty()||(l.size()>dp[i]&& n[i]%l.get(l.size()-1)==0 * 1)){
            dp[i]=l.size();
            l.add(n[i]);
            help(l,i+1 * 1,n);
            l.remove(l.size()-1 * 1);
        }
        help(l,i+1 * 1,n);
    }
}
"""
        self.assertTrue(check_rule_10(original_code, adversarial_code, 'java') and are_comments_equal (original_code, adversarial_code, 'java'))
    
    def test_fail_java(self):
        original_code = """
        
/*
    static String helper(int n, int k){
        StringBuilder s = new StringBuilder();
        s.append("a".repeat(n));
        if(n==k) return s.toString();

        k=k-n;
        for(int i=0; i<n; i++){
            if(k>=25){
                s.replace(i,i+1,"z");
                k=k-25;
                if(k==0) break;
            }
            else{
                char ch = (char)(k+97);
                s.replace(i,i+1,ch+"");
                break;
            }
        }

        return s.reverse().toString();
    }
    */
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

/*
    static String helper(int n, int k){
        StringBuilder s = new StringBuilder();
        s.append("a".repeat(n));
        if(n==k) return s.toString();

        k=k-n;
        for(int i=0; i<n; i++){
            if(k>=5 * 5){
                s.replace(i,i+1,"z");
                k=k-5 * 5;
                if(k==0) break;
            }
            else{
                char ch = (char)(k+97);
                s.replace(i,i+1,ch+"");
                break;
            }
        }

        return s.reverse().toString();
    }
    */
    public String getSmallestString(int n, int k) {
        char arr[] = new char[n];
        Arrays.fill(arr,'a');

        k=k-n;

        while(k>0){
            n--;
            arr[n] += Math.min(5 * 5,k);
            k = k-Math.min(5 * 5,k);
        }

        return String.valueOf(arr);
    }
}
"""
        self.assertFalse(check_rule_10(original_code, adversarial_code, 'java') and are_comments_equal (original_code, adversarial_code, 'java'))    

    def test_fail_python(self):
        original_code = """
        class Solution:
    def maximumUniqueSubarray(self, nums):
        beg, end, S, n, sm = 0, 0, set(), len(nums), 0
        ans = 0
        while end < n:
            if nums[end] not in S:
                sm += nums[end]
                S.add(nums[end])
                end += 1
                ans = max(ans, sm)
            else:
                sm -= nums[beg]
                S.remove(nums[beg])
                beg += 1
        
        return ans
        """
        adversarial_code = """
        
class Solution:
    def maximumUniqueSubarray(self, nums):
        beg, end, S, n, sm = 0, 0, set(), len(nums), 0
        ans = 0
        while end < n:
            if nums[end] not in S:
                sm += nums[end]
                S.add(nums[end])
                end += 1
                ans = max(ans, sm)
            else:
                sm -= nums[beg]
                S.remove(nums[beg])
                beg += 1
        
        return ans
        """
        self.assertFalse(check_rule_10(original_code, adversarial_code, 'python') and are_comments_equal (original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()