import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_pass_cpp(self):
        original_code = """
        #pragma GCC optimize("O3", "unroll-loops")
class Solution {
public:
    int maxWidthOfVerticalArea(vector>& points) {
        priority_queue pq;//Max heap
        for(auto& coord: points)
            pq.push(coord[0]);
        int mdiff=0, prev=pq.top();
        while(!pq.empty()){
            int curr=pq.top();
            pq.pop();
            mdiff=max(mdiff, prev-curr);
            prev=curr;
        }
        return mdiff;       
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int maxWidthOfVerticalArea(vector>& points) {
        priority_queue pq;//Max heap
        for(auto& coord: points)
            pq.push(coord[0]);
        int mdiff=0, prev=pq.top();
        while(!pq.empty()){
            int curr=pq.top();
            pq.pop();
            mdiff=max(mdiff, prev-curr);
            prev=curr;
        }
        return mdiff;       
    }
};
"""
        self.assertTrue(check_rule_1(original_code, adversarial_code, 'cpp'))
    
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
        self.assertFalse(check_rule_1(original_code, adversarial_code, 'cpp'))
if __name__ == '__main__':
    unittest.main()