import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
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
//      return i;```
"""
        adversarial_code = """
        
class Solution {
public:
    int removeDuplicates(vector<int>& nums){  
    //using one variable which points the initial unique element
    int index=0;
    for(int i=1; !(i >= nums.size()); i++){
        if(!(nums[i] == nums[i-1])){
            nums[index+1]=nums[i];
            index++;
        }
        
    }
    return index+1;
    }
};
"""
        self.assertFalse(check_rule_9(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    vector majorityElement(vector& nums) {
        int freq1 = 0, freq2 = 0;
        int cand1 = 23, cand2 = 0;
        for(auto & num : nums){
            if(num == cand1)freq1++;
            else if(num == cand2)freq2++;
            else if(freq1 == 0){
                freq1 = 1;
                cand1 = num;
            }
            else if(freq2 == 0){
                freq2 = 1;
                cand2 = num;
            }else{
                freq1--;
                freq2--;
            }
        }
        freq1 = freq2 = 0;
        for(auto num : nums){
            if(num == cand2)freq2++;
            else if(num == cand1)freq1++;
        }
        vector res;
        int sz = nums.size();
        if(sz / 3 < freq1)res.push_back(cand1);
        if(sz / 3 < freq2)res.push_back(cand2);
        
        return res;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    vector majorityElement(vector& nums) {
        int freq1 = 0, freq2 = 0;
        int cand1 = 23, cand2 = 0;
        for(auto & num : nums){
            if(!(num != cand1))freq1++;
            else if(!(num != cand2))freq2++;
            else if(!(freq1 != 0)){
                freq1 = 1;
                cand1 = num;
            }
            else if(!(freq2 != 0)){
                freq2 = 1;
                cand2 = num;
            }else{
                freq1--;
                freq2--;
            }
        }
        freq1 = freq2 = 0;
        for(auto num : nums){
            if(!(num != cand2))freq2++;
            else if(!(num != cand1))freq1++;
        }
        vector res;
        int sz = nums.size();
        if(!(sz / 3 >= freq1))res.push_back(cand1);
        if(!(sz / 3 >= freq2))res.push_back(cand2);
        
        return res;
    }
};
"""        
        self.assertTrue(check_rule_9(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_pass_java(self):
        original_code = """
        class Solution {
    public boolean isNStraightHand(int[] hand, int groupSize) {
        Map countMap = new HashMap<>();
        for (int card : hand) {
            countMap.put(card, countMap.getOrDefault(card, 0) + 1);
        }
        
        Arrays.sort(hand);
        
        for (int i = 0; i < hand.length; i++) {
            if (countMap.get(hand[i]) == 0) {
                continue;
            }
            
            for (int j = 0; j < groupSize; j++) {
                int currCard = hand[i] + j;
                
                if (countMap.getOrDefault(currCard, 0) == 0) {
                    return false;
                }
                
                countMap.put(currCard, countMap.get(currCard) - 1);
            }
        }
        
        return true;
    }
}
"""
        adversarial_code = """
        class Solution {
    public boolean isNStraightHand(int[] hand, int groupSize) {
        Map countMap = new HashMap<>();
        for (int card : hand) {
            countMap.put(card, countMap.getOrDefault(card, 0) + 1);
        }
        
        Arrays.sort(hand);
        
        for (int i = 0; i < hand.length; i++) {
            if (!(countMap.get(hand[i]) != 0)) {
                continue;
            }
            
            for (int j = 0; j < groupSize; j++) {
                int currCard = hand[i] + j;
                
                if (!(countMap.getOrDefault(currCard, 0) != 0)) {
                    return false;
                }
                
                countMap.put(currCard, countMap.get(currCard) - 1);
            }
        }
        
        return true;
    }
}
"""
        self.assertTrue(check_rule_9(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))

    def test_fail_java(self):
        original_code = """
        class CombinationIterator {
    int len=0;
    List<String> list = new ArrayList<>();
    private void helper(String s, int c, int idx, StringBuilder sb){
        //Base Case
        if(sb.length() == c){
            list.add(sb.toString());
            return;
        }

        for(int i=idx; i<s.length(); i++){
            sb.append(s.charAt(i));
            helper(s, c, i+1, sb);
            sb.deleteCharAt(sb.length()-1);
        }
    }

    public CombinationIterator(String characters, int combinationLength) {
        helper(characters, combinationLength, 0, new StringBuilder());
    }
    

// TC:-O(1)
    public String next() {
        return list.get(len++);
    }
    
// TC:-O(1)
    public boolean hasNext() {
        return len < list.size();
    }
}

/**
 * Your CombinationIterator object will be instantiated and called as such:
 * CombinationIterator obj = new CombinationIterator(characters, combinationLength);
 * String param_1 = obj.next();
 * boolean param_2 = obj.hasNext();
 */
 """
        adversarial_code = """
        
class CombinationIterator {
    int len=0;
    List<String> list = new ArrayList<>();
    private void helper(String s, int c, int idx, StringBuilder sb){
        //Base Case
        if(!(sb.length() != c)){
            list.add(sb.toString());
            return;
        }

        for(int i=idx; i<s.length(); i++){
            sb.append(s.charAt(i));
            helper(s, c, i+1, sb);
            sb.deleteCharAt(sb.length()-1);
        }
    }

    public CombinationIterator(String characters, int combinationLength) {
        helper(characters, combinationLength, 0, new StringBuilder());
    }
    

// TC:-O(1)
    public String next() {
        return list.get(len++);
    }
    
// TC:-O(1)
    public boolean hasNext() {
        return !(len >= list.size());
    }
}
"""
        self.assertFalse(check_rule_9(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_fail_python(self):
        original_code = """
        # Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution(object):
    def mergeKLists(self, lists):
        # Create a new ListNode representing the head of the merged list.
        # Initialize it with an empty ListNode.
        newList = ListNode()
        # Create a temporary ListNode to build the merged list.
        temporary_list = newList

        # Define a helper function to get the smallest value among the current heads of all lists.
        def getSmallestValue():
            min_value = float('inf')  # Initialize the minimum value as positive infinity.
            min_index = -1  # Initialize the index of the list with the minimum value as -1.
            for i in range(len(lists)):
                # Check if the current list is not empty and its head value is smaller than the current minimum value.
                if lists[i] is not None and lists[i].val < min_value:
                    min_value = lists[i].val
                    min_index = i
            if min_index != -1:
                # If a list with the minimum value is found, move its head to the next element.
                lists[min_index] = lists[min_index].next
            return min_value
        
        # Loop to merge the lists.
        while True:
            x = getSmallestValue()  # Get the smallest value among the current heads of lists.
            if x == float('inf'):
                # If the smallest value is still positive infinity, all lists are empty, so break the loop.
                break
            # Create a new ListNode with the value of the smallest element.
            c = ListNode(val=x)
            # Connect the new node to the merged list.
            temporary_list.next = c
            temporary_list = temporary_list.next  # Move the temporary list pointer forward.
        
        # Return the merged list, excluding the initial empty ListNode.
        return newList.next
        """
        adversarial_code = """
        
class Solution(object):
    def mergeKLists(self, lists):
        newList = ListNode()
        temporary_list = newList

        def getSmallestValue():
            min_value = float('inf')
            min_index = -1
            for i in range(len(lists)):
                if not (lists[i] is None or lists[i].val >= min_value):
                    min_value = lists[i].val
                    min_index = i
            if not (min_index == -1):
                lists[min_index] = lists[min_index].next
            return min_value
        
        while True:
            x = getSmallestValue()
            if not (x != float('inf')):
                break
            c = ListNode(val=x)
            temporary_list.next = c
            temporary_list = temporary_list.next
        
        return newList.next
        """
        self.assertFalse(check_rule_9(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()