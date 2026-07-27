import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_pass_cpp(self):
        original_code = """
        /**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    vector splitListToParts(ListNode* head, int k) 
    {
        ListNode* curr=head;
        int n=0;
        while(curr){
            curr=curr->next;
            n++;
        }
        auto [q, r]=div(n, k);
        vector iLen(k, q);
        for (int i=0; i ans(k);
        curr=head;
        for(int i=0; i;//extra pointer is needed
            while(jnext;
                j++;
            }
            if (prev)
                prev->next=NULL;//Remove the link
        }
        return ans;
    }
};
"""
        adversarial_code = """
        #include 
#include 
using namespace std;

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    vector splitListToParts(ListNode* head, int k) 
    {
        ListNode* curr = head;
        cout << "Initialized curr with head" << endl;
        int n = 0;
        cout << "Initialized n with 0" << endl;
        while(curr){
            curr = curr->next;
            cout << "Updated curr to curr->next" << endl;
            n++;
            cout << "Incremented n to " << n << endl;
        }
        auto [q, r] = div(n, k);
        cout << "Calculated q = " << q << ", r = " << r << " using div(n, k)" << endl;
        vector iLen(k, q);
        cout << "Initialized iLen with " << k << " elements, each of value " << q << endl;
        for (int i = 0; i < r; i++) {
            iLen[i]++;
            cout << "Incremented iLen[" << i << "] to " << iLen[i] << endl;
        }
        vector ans(k);
        cout << "Initialized ans with " << k << " null elements" << endl;
        curr = head;
        cout << "Reset curr to head" << endl;
        for(int i = 0; i < k; i++){
            ans[i] = curr;
            cout << "Set ans[" << i << "] to curr" << endl;
            int j = 0;
            cout << "Initialized j with 0" << endl;
            ListNode* prev = NULL; // extra pointer is needed
            cout << "Initialized prev with NULL" << endl;
            while(j < iLen[i]){
                prev = curr;
                cout << "Set prev to curr" << endl;
                curr = curr->next;
                cout << "Updated curr to curr->next" << endl;
                j++;
                cout << "Incremented j to " << j << endl;
            }
            if (prev) {
                prev->next = NULL; // Remove the link
                cout << "Set prev->next to NULL" << endl;
            }
        }
        return ans;
    }
};
"""
        self.assertTrue(check_rule_2(original_code, adversarial_code, 'cpp'))

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
        
#include <iostream>
#include <vector>
#include <map>

class Solution {
public:
    int removeDuplicates(std::vector<int>& nums){  
        //using one variable which points the initial unique element
        int index = 0;
        std::cout << "Initialized index: " << index << std::endl;
        for(int i = 1; i < nums.size(); i++){
            if(nums[i] != nums[i-1]){
                nums[index+1] = nums[i];
                std::cout << "Modified nums[" << index+1 << "]: " << nums[index+1] << std::endl;
                index++;
                std::cout << "Modified index: " << index << std::endl;
            }
        }
        return index + 1;
    }
};

// using extra space
// std::map<int,int> mpp;
// for(int i = 0; i < nums.size(); i++){
//     mpp[nums[i]]++;
//     std::cout << "Modified mpp[" << nums[i] << "]: " << mpp[nums[i]] << std::endl;
// }
// int i = 0;
// std::cout << "Initialized i: " << i << std::endl;
// for(std::map<int,int>::iterator it = mpp.begin(); it != mpp.end(); it++){
//     int a = it->first;
//     std::cout << "Initialized a: " << a << std::endl;
//     nums[i] = a;
//     std::cout << "Modified nums[" << i << "]: " << nums[i] << std::endl;
//     i++;
//     std::cout << "Modified i: " << i << std::endl;
// }
// return i;
"""

        self.assertFalse(check_rule_2(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_pass_java(self):
        original_code = """
        class Solution {
    public int twoCitySchedCost(int[][] costs) {
        Arrays.sort(costs, (a, b) -> {
            return (a[0] - a[1]) - (b[0] - b[1]);
        });
        
        int price = 0;
        for(int i = 0; i < costs.length / 2; i++){
            price += costs[i][0];
        }
        for(int i = costs.length / 2; i < costs.length; i++){
            price += costs[i][1];
        }
        return price;
    }
}
"""
        adversarial_code = """
        class Solution {
    public int twoCitySchedCost(int[][] costs) {
        Arrays.sort(costs, (a, b) -> {
            return (a[0] - a[1]) - (b[0] - b[1]);
        });
        
        int price = 0;
        System.out.println("Initialized price: " + price);
        
        for(int i = 0; i < costs.length / 2; i++){
            price += costs[i][0];
            System.out.println("Updated price after adding costs[" + i + "][0]: " + price);
        }
        
        for(int i = costs.length / 2; i < costs.length; i++){
            price += costs[i][1];
            System.out.println("Updated price after adding costs[" + i + "][1]: " + price);
        }
        
        return price;
    }
}
"""
        self.assertTrue(check_rule_2(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
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
        System.out.println("Initialized words: " + Arrays.toString(words));
        List<String> ans = new ArrayList<>();
        System.out.println("Initialized ans: " + ans);
        int maxLen = getMaxLen(words);
        System.out.println("Initialized maxLen: " + maxLen);

        for (int i = 0; i < maxLen; i++) {
            System.out.println("Loop i: " + i);
            StringBuilder sb = new StringBuilder();
            System.out.println("Initialized sb: " + sb);

            for (String word : words) {
                if (i >= word.length()) {
                    sb.append(' ');
                    System.out.println("Appended space to sb: " + sb);
                } else {
                    sb.append(word.charAt(i));
                    System.out.println("Appended " + word.charAt(i) + " to sb: " + sb);
                }
            }

            String trimmed = trimRight(sb.toString());
            System.out.println("Trimmed sb: " + trimmed);
            ans.add(trimmed);
            System.out.println("Modified ans: " + ans);
        }

        return ans;
    }

    private int getMaxLen(String[] arr) {
        int max = 0;
        System.out.println("Initialized max: " + max);
        for (String s : arr) {
            max = Math.max(max, s.length());
            System.out.println("Updated max: " + max);
        }

        return max;
    }

    private String trimRight(String s) {
        int i = s.length() - 1;
        System.out.println("Initialized i: " + i);
        while (i >= 0 && s.charAt(i) == ' ') {
            i--;
            System.out.println("Decremented i: " + i);
        }
        String result = s.substring(0, i + 1);
        System.out.println("Trimmed result: " + result);
        return result;
    }
}
"""        
        self.assertFalse(check_rule_2(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))    
if __name__ == '__main__':
    unittest.main()