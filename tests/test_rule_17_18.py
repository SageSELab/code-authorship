import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp_17_comment_does_not_match(self):
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
    int i = 1;
    while(i < nums.size()){
        if(nums[i] != nums[i-1]){
            nums[index+1] = nums[i];
            index++;
        }
        i++;
    }
    return index+1;
    }
};



// using extra space
// map<int,int> mpp ;
//     int i = 0;
//     while(i < nums.size()){
//         mpp[nums[i]]++;
//         i++;
//     }  
//     i = 0;
//     for(map<int,int>::iterator it= mpp.begin(); it!=mpp.end();it++){
//         int a=it->first;
//         nums[i]=a;
//         i++;
//     }
//      return i;
"""
        self.assertFalse(check_rule_17_and_18(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_java_17_comment_does_not_match(self):
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
        int totalSum = 0;
        // Initialize 'leftsum' as sum of first i numbers, not including nums[i]...
        int leftsum = 0;
        // Traverse the elements and add them to store the totalSum...
        int index = 0;
        while (index < nums.length) {
            totalSum += nums[index];
            index++;
        }
        // Again traverse all the elements through the while loop and store the sum of i numbers from left to right...
        int i = 0;
        while (i < nums.length) {
            // sum to the left == leftsum.
            // sum to the right === totalSum - leftsum - nums[i]..
            // check if leftsum == totalSum - leftsum - nums[i]...
            if (leftsum * 2 == totalSum - nums[i])
                return i;       // Return the pivot index...
            leftsum += nums[i];
            i++;
        }
        return -1;      // If there is no index that satisfies the conditions in the problem statement...
    }
}
"""
        self.assertFalse(check_rule_17_and_18(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    def test_pass_java_17(self):
        original_code = """
        class Solution {
  public int maxDepth(Node node) {
    if (node == null) return 0;
    
    var max = 0;

    for (var child : node.children)
      max = Math.max(max, maxDepth(child));

    return max + 1;
  }
}
"""
        adversarial_code = """
        class Solution {
  public int maxDepth(Node node) {
    if (node == null) return 0;
    
    var max = 0;

    var iterator = node.children.iterator();
    while (iterator.hasNext()) {
      var child = iterator.next();
      max = Math.max(max, maxDepth(child));
    }

    return max + 1;
  }
}
"""
        self.assertTrue(check_rule_17_and_18(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    def test_pass_python_17(self):
        original_code = """
        class Solution:
    def findRightInterval(self, intervals):
        ints = sorted([[j,k,i] for i,[j,k] in enumerate(intervals)])
        begs = [i for i,_,_ in ints]
        out = [-1]*len(begs)
        for i,j,k in ints:
            t = bisect.bisect_left(begs, j)
            if t < len(begs):
                out[k] = ints[t][2]
        
        return out
        """
        adversarial_code = """
        class Solution:
    def findRightInterval(self, intervals):
        ints = sorted([[j,k,i] for i,[j,k] in enumerate(intervals)])
        begs = [i for i,_,_ in ints]
        out = [-1]*len(begs)
        index = 0
        while index < len(ints):
            i, j, k = ints[index]
            t = bisect.bisect_left(begs, j)
            if t < len(begs):
                out[k] = ints[t][2]
            index += 1
        
        return out
        """
        self.assertTrue(check_rule_17_and_18(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
    def test_pass_cpp_17(self):
        original_code = """
        class Solution {
public:
    // To store the output result...
    vector output;
    void traverse(Node* root) {
        // Base case: if the tree is empty...
        if(root == NULL) return;
        // Push the value of the root node to the output...
        output.push_back(root->val);
        // Recursively traverse each node in the children array...
        for(auto node:root->children)
            traverse(node);
    }
    vector preorder(Node* root) {
        output.clear();
        traverse(root);
        return output;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    // To store the output result...
    vector output;
    void traverse(Node* root) {
        // Base case: if the tree is empty...
        if(root == NULL) return;
        // Push the value of the root node to the output...
        output.push_back(root->val);
        // Recursively traverse each node in the children array...
        auto it = root->children.begin();
        while(it != root->children.end()) {
            traverse(*it);
            ++it;
        }
    }
    vector preorder(Node* root) {
        output.clear();
        traverse(root);
        return output;
    }
};
"""
        self.assertTrue(check_rule_17_and_18(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_pass_java_18(self):
        original_code = """
        class Solution {
    public int bitwiseComplement(int n) {
        if(n == 0) return 1; // Checking for base case
        int res = 0;
        int fac = 1; // keep for 2 basically
        
        while(n != 0){
            // first we need to check what is our bit in 2 by taking modulo
            res += fac * (n % 2 == 0 ? 1 : 0);
            // res is the number convert back to decimal + factor * n % 2 if comes 0 then we take 1 otherwise 0 this is our complement
            
            fac *= 2;
            n /= 2;
        }
        return res;
    }
}
"""
        adversarial_code = """
        class Solution {
    public int bitwiseComplement(int n) {
        if(n == 0) return 1; // Checking for base case
        int res = 0;
        int fac = 1; // keep for 2 basically
        
        for(; n != 0; n /= 2) {
            // first we need to check what is our bit in 2 by taking modulo
            res += fac * (n % 2 == 0 ? 1 : 0);
            // res is the number convert back to decimal + factor * n % 2 if comes 0 then we take 1 otherwise 0 this is our complement
            
            fac *= 2;
        }
        return res;
    }
}
"""
        self.assertTrue(check_rule_17_and_18(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    def test_pass_cpp_18(self):
        original_code = """
        class Solution {
public:
    int bitwiseComplement(int n) {
        if(n == 0) return 1; // Checking for base case
        int res = 0;
        int fac = 1; // keep for 2 basically
        
        while(n != 0){
            // first we need to check what is our bit in 2 by taking modulo
            res += fac * (n % 2 == 0 ? 1 : 0);
            // res is the number convert back to decimal + factor * n % 2 if comes 0 then we take 1 otherwise 0 this is our complement
            
            fac *= 2;
            n /= 2;
        }
        return res;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int bitwiseComplement(int n) {
        if(n == 0) return 1; // Checking for base case
        int res = 0;
        int fac = 1; // keep for 2 basically
        
        for(; n != 0; n /= 2) {
            // first we need to check what is our bit in 2 by taking modulo
            res += fac * (n % 2 == 0 ? 1 : 0);
            // res is the number convert back to decimal + factor * n % 2 if comes 0 then we take 1 otherwise 0 this is our complement
            
            fac *= 2;
        }
        return res;
    }
};
"""
        self.assertTrue(check_rule_17_and_18(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_python_18_comment_does_not_match(self):
        original_code = """
        # Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        head = ListNode()
        current = head
        carry = 0
        while (l1 != None or l2 != None or carry != 0):
            l1_value = l1.val if l1 else 0
            l2_value = l2.val if l2 else 0
            total = l1_value + l2_value + carry
            current.next = ListNode(total % 10)
            carry = total // 10
            # Move list pointers forward
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            current = current.next
        return head.next
        """
        adversarial_code = """
        
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        head = ListNode()
        current = head
        carry = 0
        for _ in iter(int, 1):  # Infinite loop, break condition inside
            if l1 is None and l2 is None and carry == 0:
                break
            l1_value = l1.val if l1 else 0
            l2_value = l2.val if l2 else 0
            total = l1_value + l2_value + carry
            current.next = ListNode(total % 10)
            carry = total // 10
            # Move list pointers forward
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            current = current.next
        return head.next
        """
        self.assertFalse(check_rule_17_and_18(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()