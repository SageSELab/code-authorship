import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        """
        Comments are not equal
        """
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
    for(int i=1;i<nums.size();i++){
        if(nums[i]==nums[i-1]){
            // Swapped: originally empty
        } else {
            nums[index+1]=nums[i];
            index++;
        }
        
    }
    return index+1;
    }
};
"""
        self.assertFalse(check_rule_23(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    
    def test_fail_java(self):
        original_code = """
        class Solution {

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
            if(k>=25){
                char ch = (char)(k+97);
                s.replace(i,i+1,ch+"");
                break;
            }
            else{
                s.replace(i,i+1,"z");
                k=k-25;
                if(k==0) break;
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
        self.assertFalse(check_rule_23(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))    

    def test_pass_java(self):
        original_code = """
        class Solution {
    public List> getSkyline(int[][] buildings) {
        List> res = new ArrayList<>();
        List heights = new ArrayList<>();
        
        // transforming buildings
        for (int[] building : buildings) {          // O(n)
            heights.add(new int[] {building[0], -building[2]});
            heights.add(new int[] {building[1], building[2]});
        }
        
        Collections.sort(heights, (a, b) -> (a[0] == b[0]) ? a[1] - b[1] : a[0] - b[0]);    // O(nlogn)
        
        PriorityQueue pq = new PriorityQueue<>((a, b) -> b - a);
        pq.offer(0);
        
        int prevMax = 0;
        
        for (int[] height : heights) {  // O(n)
            
            if (height[1] < 0) pq.offer(-height[1]);    // takes O(logn)
            else pq.remove(height[1]);                  // takes O(n)
            
            int currMax = pq.peek();
            
            if (currMax != prevMax) {
                res.add(Arrays.asList(height[0], currMax));
                prevMax = currMax;
            }
        }
        
        return res;
    }
}

// TC: O(n) +O(n * (n + logn)) => O(n ^ 2)
// SC: O(n) 
"""

        adversarial_code = """
        class Solution {
    public List> getSkyline(int[][] buildings) {
        List> res = new ArrayList<>();
        List heights = new ArrayList<>();
        
        // transforming buildings
        for (int[] building : buildings) {          // O(n)
            heights.add(new int[] {building[0], -building[2]});
            heights.add(new int[] {building[1], building[2]});
        }
        
        Collections.sort(heights, (a, b) -> {
            if (a[0] == b[0]) {
                return a[1] - b[1];
            } else {
                return a[0] - b[0];
            }
        });    // O(nlogn)
        
        PriorityQueue pq = new PriorityQueue<>((a, b) -> b - a);
        pq.offer(0);
        
        int prevMax = 0;
        
        for (int[] height : heights) {  // O(n)
            
            if (height[1] < 0) pq.offer(-height[1]);    // takes O(logn)
            else pq.remove(height[1]);                  // takes O(n)
            
            int currMax = pq.peek();
            
            if (currMax != prevMax) {
                res.add(Arrays.asList(height[0], currMax));
                prevMax = currMax;
            }
        }
        
        return res;
    }
}

// TC: O(n) +O(n * (n + logn)) => O(n ^ 2)
// SC: O(n)
"""
        self.assertTrue(check_rule_23(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_pass_python(self):
        original_code = """
        class Solution:
    def removeElements(self, head, T):
        dummy = ListNode(-1, head)
        prev = dummy
        while head:
            if head.val != T:
                prev = head
            else:
                prev.next = head.next
            head = head.next
        return dummy.next
        """
        adversarial_code = """
        class Solution:
    def removeElements(self, head, T):
        dummy = ListNode(-1, head)
        prev = dummy
        while head:
            if head.val == T:
                prev.next = head.next
            else:
                prev = head
            head = head.next
        return dummy.next
        """
        self.assertTrue(check_rule_23(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()