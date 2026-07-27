import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_LeetCode_6_48_fail(self):
        original_code = """
        class Solution {
public:
    Node* connect(Node* root) {
        auto head = root;
        for(; root; root = root -> left) 
            for(auto cur = root; cur; cur = cur -> next)   // traverse each level - it's just BFS taking advantage of next pointers          
                if(cur -> left) {                          // update next pointers of children if they exist               
                    cur -> left -> next = cur -> right;
                    if(cur -> next) cur -> right -> next = cur -> next -> left;
                }
                else break;                                // if no children exist, stop iteration                                                  
        
        return head;
    }
};
"""        
        adversarial_code = """
        class Solution {
public:
    Node* connect(Node* root) {
        auto head = root;
        for(; root; root = root -> left) 
            for(auto cur = root; cur; cur = cur -> next)   // traverse each level - it's just BFS taking advantage of next pointers          
                if(cur -> left) {                          // update next pointers of children if they exist               
                    cur -> left -> next = cur -> right;
                    if(cur -> next) {
                        cur -> right -> next = cur -> next -> left;
                    }
                }
                else break;                                // if no children exist, stop iteration                                                  
        
        return head;
    }
};
"""        
        self.assertFalse(check_rule_22(original_code, adversarial_code, 'cpp'))
    
    def test_LeetCode_4_370_java_pass(self):
        original_code = """
        class Solution {
    public int constrainedSubsetSum(int[] nums, int k) {
        int[] maxTillThis = nums.clone();
        Deque maxSbSqUptSzK = new ArrayDeque<>();
        int res = maxTillThis[0];
        for (int indx = 0; indx < maxTillThis.length; ++indx) {
            maxTillThis[indx] += maxSbSqUptSzK.size() > 0    ? maxTillThis[maxSbSqUptSzK.peekFirst()] : 0;
            res = Math.max(res, maxTillThis[indx]);
            while (!maxSbSqUptSzK.isEmpty() && maxTillThis[indx] > maxTillThis[maxSbSqUptSzK.peekLast()]) {
                maxSbSqUptSzK.removeLast();
            }
            if (maxTillThis[indx] > 0) {
                maxSbSqUptSzK.addLast(indx);
            }
            if (indx >= k && !maxSbSqUptSzK.isEmpty() && maxSbSqUptSzK.peekFirst() == indx - k) {
                maxSbSqUptSzK.removeFirst();
            }
        }
        return res;
    }
}
"""
        adversarial_code = """
        class Solution {
    public int constrainedSubsetSum(int[] nums, int k) {
        int[] maxTillThis = nums.clone();
        Deque maxSbSqUptSzK = new ArrayDeque<>();
        int res = maxTillThis[0];
        for (int indx = 0; indx < maxTillThis.length; ++indx) {
            if (maxSbSqUptSzK.size() > 0) {
                maxTillThis[indx] += maxTillThis[maxSbSqUptSzK.peekFirst()];
            } else {
                maxTillThis[indx] += 0;
            }
            res = Math.max(res, maxTillThis[indx]);
            while (!maxSbSqUptSzK.isEmpty() && maxTillThis[indx] > maxTillThis[maxSbSqUptSzK.peekLast()]) {
                maxSbSqUptSzK.removeLast();
            }
            if (maxTillThis[indx] > 0) {
                maxSbSqUptSzK.addLast(indx);
            }
            if (indx >= k && !maxSbSqUptSzK.isEmpty() && maxSbSqUptSzK.peekFirst() == indx - k) {
                maxSbSqUptSzK.removeFirst();
            }
        }
        return res;
    }
}
"""
        self.assertTrue(check_rule_22(original_code, adversarial_code, 'java'))
    
    def test_LeetCode_1_471_ruby_pass(self):
        original_code = """
        class Numeric
    def max(v)
        self < v ? v : self
    end
end

class Solver
    attr_reader :nums, :ns2, :gcd

    def initialize(nums)
        @nums, @ns2, @gcd = nums, nums.size / 2, Array.new(nums.size) {|_| Array.new(nums.size) }
        nums.each_with_index {|v, idx|
            (idx+1...nums.size).each {|j| @gcd[idx][j] = v.gcd(nums[j]) }
        }
    end

    def rec(op = 1, mask = 0)
        return 0 if op > ns2
        @dp[mask] ||= nums.size.times.inject(-1) {|res, i|
            next res unless mask[i].zero?
            (i+1...nums.size).inject(res) {|res1, j|
                next res1 unless mask[j].zero?
                res1.max(op * gcd[i][j] + rec(op + 1, mask | (1 << i) | (1 << j)))
            }
        }
    end

    def solve
        @dp = Array.new(1 << nums.size)
        rec
    end
end

def max_score(nums)
    Solver.new(nums).solve
end
"""
        adversarial_code = """
        class Numeric
    def max(v)
        if self < v
            v
        else
            self
        end
    end
end

class Solver
    attr_reader :nums, :ns2, :gcd

    def initialize(nums)
        @nums, @ns2, @gcd = nums, nums.size / 2, Array.new(nums.size) {|_| Array.new(nums.size) }
        nums.each_with_index {|v, idx|
            (idx+1...nums.size).each {|j| @gcd[idx][j] = v.gcd(nums[j]) }
        }
    end

    def rec(op = 1, mask = 0)
        return 0 if op > ns2
        @dp[mask] ||= nums.size.times.inject(-1) {|res, i|
            next res unless mask[i].zero?
            (i+1...nums.size).inject(res) {|res1, j|
                next res1 unless mask[j].zero?
                res1.max(op * gcd[i][j] + rec(op + 1, mask | (1 << i) | (1 << j)))
            }
        }
    end

    def solve
        @dp = Array.new(1 << nums.size)
        rec
    end
end

def max_score(nums)
    Solver.new(nums).solve
end
"""        
        self.assertTrue(check_rule_22(original_code, adversarial_code, 'ruby'))

if __name__ == '__main__':
    unittest.main()