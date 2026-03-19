import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_fail_cpp(self):
        original_code = """
       class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int i=0;
        int j =0;
        long long sum = 0;
        int maxsum =INT_MIN;

        while(j<nums.size()){
            sum+=nums[j];

            if(sum>maxsum){
                maxsum = sum;
            }
            if(sum<0){
                sum =0;
            }
            j++;
        }
        return maxsum;
    }  
};
"""
        adversarial_code = """
        
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        return findMaxSubArray(nums);
    }

private:
    int findMaxSubArray(vector<int>& nums) {
        int j = 0;
        long long sum = 0;
        int maxsum = INT_MIN;

        while (j < nums.size()) {
            sum += nums[j];

            if (sum > maxsum) {
                maxsum = sum;
            }
            if (sum < 0) {
                sum = 0;
            }
            j++;
        }
        return maxsum;
    }
};
"""
        self.assertFalse(check_rule_26(original_code, adversarial_code, 'cpp'))
    
    def test_pass_java(self):
        original_code = """
        class Solution {
  public int combinationSum4(int[] nums, int target) {
    var dp = new int[target + 1];
    dp[0] = 1;
    
    for (var i=1; i <= target; i++)
      for (var num : nums)
        dp[i] += i - num >= 0 ? dp[i - num] : 0;

    return dp[target];
  }
}
"""
        adversarial_code = """
class Solution {
  public int combinationSum4(int[] nums, int target) {
    var dp = new int[target + 1];
    dp[0] = 1;
    
    fillDpArray(nums, target, dp);

    return dp[target];
  }
  
  private void fillDpArray(int[] nums, int target, int[] dp) {
    for (var i = 1; i <= target; i++) {
      for (var num : nums) {
        dp[i] += i - num >= 0 ? dp[i - num] : 0;
      }
    }
  }
}
"""
        self.assertTrue(check_rule_26(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))

    def test_pass_python(self):
        original_code = """
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
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            current = current.next
        return head.next
        """
        adversarial_code = """
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        def get_value_and_move(node):
            value = node.val if node else 0
            next_node = node.next if node else None
            return value, next_node
        
        head = ListNode()
        current = head
        carry = 0
        while (l1 != None or l2 != None or carry != 0):
            l1_value, l1 = get_value_and_move(l1)
            l2_value, l2 = get_value_and_move(l2)
            total = l1_value + l2_value + carry
            current.next = ListNode(total % 10)
            carry = total // 10
            current = current.next
        return head.next
        """
        self.assertTrue(check_rule_26(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()