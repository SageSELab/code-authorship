import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_LeetCode_2_198_fail(self):
        original_code = """
        class Solution {
public:
    int leastInterval(vector& tasks, int n) {
        vector mp(26,0); 
        for(char it:tasks) mp[it-65]++;
        sort(mp.begin(),mp.end(),greater());
        while(!mp.back()) mp.erase(--mp.end());
        
        n++;
        int ans = 0,diff,k,back; 
        while(mp.size()){
            if(mp.size()>n){
                // diff = max(mp[n] - mp[n-1],1);
                ans+=n;
                for_each(mp.begin(), mp.begin() + n, [](int &x) { x--;});           // you can understande the difference in first 3 lines of if statement
                sort(mp.begin(),mp.end(),greater());
                while(mp.size() and !mp.back()) mp.erase(--mp.end());
            }else{
                k = mp.size();
                back = mp.back();
                ans+=(n)*back;
                for_each(mp.begin(), mp.end(), [back](int &x) { x-=back;});
                while(mp.size() and !mp.back()) mp.erase(--mp.end());
                if(!mp.size()) ans -= n-k;
            }
        }
        return ans;
    }
};
        """
        adversarial_code = """
        class Solution {
public:
    int leastInterval(vector& tasks, int n) {
        vector mp(26,0); 
        for(char it:tasks) mp[it-65]++;
        sort(mp.begin(),mp.end(),greater());
        while(!mp.back()) mp.erase(--mp.end());
        
        n++;
        int ans = 0,diff,k,back; 
        while(mp.size()){
            if(mp.size()>n){
                // diff = max(mp[n] - mp[n-1],1);
                ans+=n;
                for_each(mp.begin(), mp.begin() + n, [](int &x) { x--;});           // you can understande the difference in first 3 lines of if statement
                sort(mp.begin(),mp.end(),greater());
                while(mp.size() and mp.back() == 0) mp.erase(--mp.end());
            }else{
                k = mp.size();
                back = mp.back();
                ans+=(n)*back;
                for_each(mp.begin(), mp.end(), [back](int &x) { x-=back;});
                while(mp.size() and mp.back() == 0) mp.erase(--mp.end());
                if(mp.size() == 0) ans -= n-k;
            }
        }
        return ans;
    }
}
"""
        self.assertFalse(check_rule_16(original_code, adversarial_code, 'cpp'))
    
    def test_LeetCode_2_124_pass(self):
        original_code = """
        class Solution {
public:
    bool isPowerOfThree(int n) {
        if (n < 1) return false;
        for (int i = 0; i <= n; i++)
        {
            if (pow(3, i) == n) return true;
            if (pow(3, i) > n) return false;
        }
        return false;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    bool isPowerOfThree(int n) {
        if (n < 1) return 0;
        for (int i = 0; i <= n; i++)
        {
            if (pow(3, i) == n) return 1;
            if (pow(3, i) > n) return 0;
        }
        return 0;
    }
};
"""
        self.assertFalse(check_rule_16(original_code, adversarial_code, 'cpp'))
    
    def LeetCode_2_198_16_fail(self):
        original_code = """
        class Solution {
public:
    int leastInterval(vector& tasks, int n) {
        vector mp(26,0); 
        for(char it:tasks) mp[it-65]++;
        sort(mp.begin(),mp.end(),greater());
        while(!mp.back()) mp.erase(--mp.end());
        
        n++;
        int ans = 0,diff,k,back; 
        while(mp.size()){
            if(mp.size()>n){
                // diff = max(mp[n] - mp[n-1],1);
                ans+=n;
                for_each(mp.begin(), mp.begin() + n, [](int &x) { x--;});           // you can understande the difference in first 3 lines of if statement
                sort(mp.begin(),mp.end(),greater());
                while(mp.size() and !mp.back()) mp.erase(--mp.end());
            }else{
                k = mp.size();
                back = mp.back();
                ans+=(n)*back;
                for_each(mp.begin(), mp.end(), [back](int &x) { x-=back;});
                while(mp.size() and !mp.back()) mp.erase(--mp.end());
                if(!mp.size()) ans -= n-k;
            }
        }
        return ans;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int leastInterval(vector& tasks, int n) {
        vector mp(26,0); 
        for(char it:tasks) mp[it-65]++;
        sort(mp.begin(),mp.end(),greater());
        while(!mp.back()) mp.erase(--mp.end());
        
        n++;
        int ans = 0,diff,k,back; 
        while(mp.size()){
            if(mp.size()>n){
                // diff = max(mp[n] - mp[n-1],1);
                ans+=n;
                for_each(mp.begin(), mp.begin() + n, [](int &x) { x--;});           // you can understande the difference in first 3 lines of if statement
                sort(mp.begin(),mp.end(),greater());
                while(mp.size() and mp.back() == 0) mp.erase(--mp.end());
            }else{
                k = mp.size();
                back = mp.back();
                ans+=(n)*back;
                for_each(mp.begin(), mp.end(), [back](int &x) { x-=back;});
                while(mp.size() and mp.back() == 0) mp.erase(--mp.end());
                if(mp.size() == 0) ans -= n-k;
            }
        }
        return ans;
    }
};
"""        
        self.assertFalse(check_rule_16(original_code, adversarial_code, 'cpp'))

if __name__ == '__main__':
    unittest.main()
        