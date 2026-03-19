import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_pass_cpp(self):
        original_code = """
       class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int reader=0, writer=0;
        // reader pointer will move forward in every iteration, writer will stop if nums[writer]==val, and will be overwritten by nums[reader]
        while(reader<nums.size()){
            if(nums[reader]==val){
                reader++;
            }
            else{
                nums[writer++] = nums[reader++];

            }
        }
        return writer;
    }
};
        """
        adversarial_code = """
        
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int reader=0, writer=0;
        // reader pointer will move forward in every iteration, writer will stop if nums[writer]==val, and will be overwritten by nums[reader]
        while(reader<nums.size()){
            if(nums[reader]==val){
                reader += 1;
            }
            else{
                nums[writer] = nums[reader];
                writer += 1;
                reader += 1;
            }
        }
        return writer;
    }
};
        """
        self.assertTrue(check_rule_11(original_code, adversarial_code, 'cpp'))
    
    def test_pass_csharp(self):
        original_code = """
       
public class Solution {
    public bool HasAlternatingBits(int n) {
        int bit,prevbit=3;
        bool leadingZeros=true;
        for(int i=sizeof(int)*8-1;i>=0; i--){
            bit = (n>>i)&1;
            if(bit==1)
                leadingZeros=false;
            if(!leadingZeros){
                if(prevbit==bit)
                    return false;
                prevbit=bit;
            }
        }
        return true;
    }
}
"""
        adversarial_code = """
        
public class Solution {
    public bool HasAlternatingBits(int n) {
        int bit,prevbit=3;
        bool leadingZeros=true;
        for(int i=sizeof(int)*8-1;i>=0; i-=1){
            bit = (n>>i)&1;
            if(bit==1)
                leadingZeros=false;
            if(!leadingZeros){
                if(prevbit==bit)
                    return false;
                prevbit=bit;
            }
        }
        return true;
    }
}
"""        
        self.assertTrue(check_rule_11(original_code, adversarial_code, 'csharp'))
        
    def test_fail_cpp(self):
        original_code = """
       class Solution {
public:
    int removeDuplicates(vector<int>& nums){  
    //using one variable which points the initial unique element
    int index=0;
    for(int i=1;i<nums.size();i++){
        if(nums[i]!=nums[i-1]){
            nums[index+1]=nums[i];
            index++;
        }
        
    }
    return index+1;
    }
};



// using extra space
// map<int,int> mpp ;
//     for(int i=0;i<nums.size();i++){
//         mpp[nums[i]]++;
//     }  
//     int i=0;
//     for(map<int,int>::iterator it= mpp.begin(); it!=mpp.end();it++){
//         int a=it->first;
//         nums[i]=a;
//         i++;
//     }
//      return i;
"""
        adversarial_code = """
        
class Solution {
public:
    int removeDuplicates(vector<int>& nums){  
    //using one variable which points the initial unique element
    int index=0;
    for(int i=1;i<nums.size();i++){
        if(nums[i]!=nums[i-1]){
            nums[index+1]=nums[i];
            index += 1;
        }
        
    }
    return index+1;
    }
};



// using extra space
// map<int,int> mpp ;
//     for(int i=0;i<nums.size();i++){
//         mpp[nums[i]]++;
//     }  
//     int i=0;
//     for(map<int,int>::iterator it= mpp.begin(); it!=mpp.end();it++){
//         int a=it->first;
//         nums[i]=a;
//         i += 1;
//     }
//      return i;
"""
        self.assertFalse(check_rule_11(original_code, adversarial_code, 'cpp') and are_comments_equal (original_code, adversarial_code, 'cpp'))
    def test_fail_java(self):
        original_code = """
        class Solution {
    public List<String> printVertically(String s) {
        String[] words = s.split(" ");
        List<String> ans = new ArrayList<>();
        int maxLen = getMaxLen(words);

        for (int i = 0; i < maxLen; i++) {
            StringBuilder sb = new StringBuilder();

            for (String word : words) {
                if (i >= word.length()) sb.append(' ');
                else sb.append(word.charAt(i));
            }

            ans.add(trimRight(sb.toString()));
            // ans.add(sb.toString().stripTrailing());    <-- we can use this method as well
            // ans.add(sb.toString().replaceAll("\\s+$", ""));      --> greater runtime
        }

        return ans;
    }

    private int getMaxLen(String[] arr) {
        int max = 0;
        for (String s : arr) {
            max = Math.max(max, s.length());
        }

        return max;
    }

    private String trimRight(String s) {
        int i = s.length() - 1;
        while (i >= 0 && s.charAt(i) == ' ') i--;
        return s.substring(0, i + 1);
    }
}

// TC: O(m * n)
// m -> maximum length of word in s
// n -> number of words

// SC: O(n)
"""
        adversarial_code = """
        
class Solution {
    public List<String> printVertically(String s) {
        String[] words = s.split(" ");
        List<String> ans = new ArrayList<>();
        int maxLen = getMaxLen(words);

        for (int i = 0; i < maxLen; i += 1) {
            StringBuilder sb = new StringBuilder();

            for (String word : words) {
                if (i >= word.length()) sb.append(' ');
                else sb.append(word.charAt(i));
            }

            ans.add(trimRight(sb.toString()));
            // ans.add(sb.toString().stripTrailing());    <-- we can use this method as well
            // ans.add(sb.toString().replaceAll("\\s+$", ""));      --> greater runtime
        }

        return ans;
    }

    private int getMaxLen(String[] arr) {
        int max = 0;
        for (String s : arr) {
            max = Math.max(max, s.length());
        }

        return max;
    }

    private String trimRight(String s) {
        int i = s.length() - 1;
        while (i >= 0 && s.charAt(i) == ' ') i -= 1;
        return s.substring(0, i + 1);
    }
}
"""        
        self.assertFalse(check_rule_11(original_code, adversarial_code, 'java') and are_comments_equal (original_code, adversarial_code, 'java'))

if __name__ == '__main__':
    unittest.main()