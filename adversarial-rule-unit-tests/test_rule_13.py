import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
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
    void reorderList(ListNode* head)
     {
        if ((!head) || (!head->next) || (!head->next->next)) return;
        stack<ListNode*> my_stack;
        ListNode* ptr = head;
        int size = 0;
        while (ptr != NULL) 
        {
            my_stack.push(ptr);
            size++;
            ptr = ptr->next;
        }
        ListNode* pptr = head;
        for (int j=0; j<size/2; j++) 
        {
            ListNode *element = my_stack.top();
            my_stack.pop();
            element->next = pptr->next;
            pptr->next = element;
            pptr = pptr->next->next;
        }
        pptr->next = NULL;
    }
};
        """
        adversarial_code = """
        /**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0x0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    void reorderList(ListNode* head)
     {
        if ((!head) || (!head->next) || (!head->next->next)) return;
        stack<ListNode*> my_stack;
        ListNode* ptr = head;
        int size = 0x0;
        while (ptr != NULL) 
        {
            my_stack.push(ptr);
            size++;
            ptr = ptr->next;
        }
        ListNode* pptr = head;
        for (int j=0x0; j<size/0x2; j++) 
        {
            ListNode *element = my_stack.top();
            my_stack.pop();
            element->next = pptr->next;
            pptr->next = element;
            pptr = pptr->next->next;
        }
        pptr->next = NULL;
    }
};
"""
        self.assertFalse(check_rule_13(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_pass_cpp(self):
        original_code = """
        // OJ: https://leetcode.com/contest/biweekly-contest-40/problems/design-front-middle-back-queue/
// Author: github.com/lzl124631x
// Time: O(1) for all
// Space: O(N)
class FrontMiddleBackQueue {
    deque a, b;
    void a2b() {
        if (a.size() <= b.size()) return;
        b.push_front(a.back());
        a.pop_back();
    }
    void b2a() {
        if (b.size() <= a.size() + 1) return;
        a.push_back(b.front());
        b.pop_front();
    }
public:
    FrontMiddleBackQueue() {}
    void pushFront(int val) {
        a.push_front(val);
        a2b();
    }
    void pushMiddle(int val) {
        a.push_back(val);
        a2b();
    }
    void pushBack(int val) {
        b.push_back(val);
        b2a();
    }
    int popFront() {
        if (a.empty() && b.empty()) return -1;
        int ans;
        if (a.empty()) {
            ans = b.front();
            b.pop_front();
        } else {
            ans = a.front();
            a.pop_front();
            b2a();
        }
        return ans;
    }
    int popMiddle() {
        if (a.empty() && b.empty()) return -1;
        int ans;
        if (a.size() == b.size()) {
            ans = a.back();
            a.pop_back();
        } else {
            ans = b.front();
            b.pop_front();
        }
        return ans;
    }
    int popBack() {
        if (a.empty() && b.empty()) return -1;
        int ans = b.back();
        b.pop_back();
        a2b();
        return ans;
    }
};
"""
        adversarial_code = """
        // OJ: https://leetcode.com/contest/biweekly-contest-40/problems/design-front-middle-back-queue/
// Author: github.com/lzl124631x
// Time: O(1) for all
// Space: O(N)
class FrontMiddleBackQueue {
    deque a, b;
    void a2b() {
        if (a.size() <= b.size()) return;
        b.push_front(a.back());
        a.pop_back();
    }
    void b2a() {
        if (b.size() <= a.size() + 0x1) return;
        a.push_back(b.front());
        b.pop_front();
    }
public:
    FrontMiddleBackQueue() {}
    void pushFront(int val) {
        a.push_front(val);
        a2b();
    }
    void pushMiddle(int val) {
        a.push_back(val);
        a2b();
    }
    void pushBack(int val) {
        b.push_back(val);
        b2a();
    }
    int popFront() {
        if (a.empty() && b.empty()) return -0x1;
        int ans;
        if (a.empty()) {
            ans = b.front();
            b.pop_front();
        } else {
            ans = a.front();
            a.pop_front();
            b2a();
        }
        return ans;
    }
    int popMiddle() {
        if (a.empty() && b.empty()) return -0x1;
        int ans;
        if (a.size() == b.size()) {
            ans = a.back();
            a.pop_back();
        } else {
            ans = b.front();
            b.pop_front();
        }
        return ans;
    }
    int popBack() {
        if (a.empty() && b.empty()) return -0x1;
        int ans = b.back();
        b.pop_back();
        a2b();
        return ans;
    }
};
"""
        self.assertTrue(check_rule_13(original_code, adversarial_code, 'cpp'))

    def test_pass_python(self):
        original_code = """
        class Solution:
    def accountsMerge(self, accounts):
        names = {}
        graph = defaultdict(set)
        for acc in accounts:
            name = acc[0]
            for email in acc[1:]:
                graph[acc[1]].add(email)
                graph[email].add(acc[1])
                names[email] = name
                
        comps, seen, ans, i = defaultdict(list), set(), [], 0
        def dfs(node, i):
            comps[i].append(node)
            seen.add(node)
            for neib in graph[node]:
                if neib not in seen: dfs(neib, i)
        
        for email in graph:
            if email not in seen:
                dfs(email, i)
                i += 1
        
        return [[names[val[0]]] + sorted(val) for _,val in comps.items()]
        """
        adversarial_code = """
        class Solution:
    def accountsMerge(self, accounts):
        names = {}
        graph = defaultdict(set)
        for acc in accounts:
            name = acc[0]
            for email in acc[1:]:
                graph[acc[1]].add(email)
                graph[email].add(acc[1])
                names[email] = name
                
        comps, seen, ans, i = defaultdict(list), set(), [], 0x0
        def dfs(node, i):
            comps[i].append(node)
            seen.add(node)
            for neib in graph[node]:
                if neib not in seen: dfs(neib, i)
        
        for email in graph:
            if email not in seen:
                dfs(email, i)
                i += 0x1
        
        return [[names[val[0]]] + sorted(val) for _,val in comps.items()]
        """
        self.assertTrue(check_rule_13(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
    
    def test_fail_python(self):
        original_code = """
        class Solution(object):
    def containsDuplicate(self, nums):
        num_set = set()
        for i in nums:
            if i in num_set:
                return True
            else:
                num_set.add(i)
        return False
        """
        adversarial_code = """
        class Solution(object):
    def containsDuplicate(self, nums):
        num_set = set()
        for i in nums:
            if i in num_set:
                return True
            else:
                num_set.add(i)
        return False
        """
        self.assertFalse(check_rule_13(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
    def test_fail_java(self):
        original_code = """
        class MKAverage {

    private int m;
    private int k;
    private int size = 0;
    private long sum = 0L;

    private Queue<Integer> q = new ArrayDeque<>(m);
    private TreeMap<Integer, Integer> left = new TreeMap<>();
    private TreeMap<Integer, Integer> middle = new TreeMap<>();
    private TreeMap<Integer, Integer> right = new TreeMap<>();

    public MKAverage(int m, int k) {
        this.m = m;
        this.k = k;
    }

    private void removeOne(TreeMap<Integer, Integer> map, int num) {
        Integer rmCount = map.get(num);
        if (rmCount.equals(1)) {
            map.remove(num);
        } else {
            map.put(num, rmCount - 1);
        }
    }

    private void edgeFix(TreeMap<Integer, Integer> prev, TreeMap<Integer, Integer> next) {
        if (next.firstKey() < prev.lastKey()) {
            Integer nextKey = next.firstKey();
            Integer nextCount = next.get(nextKey);
            Integer prevKey = prev.lastKey();
            Integer prevCount = prev.get(prevKey);
            if (prevCount.equals(1)) {
                prev.remove(prevKey);
            } else {
                prev.put(prevKey, prevCount - 1);
            }
            prev.put(nextKey, prev.getOrDefault(nextKey, 0) + 1);
            if (nextCount.equals(1)) {
                next.remove(nextKey);
            } else {
                next.put(nextKey, nextCount - 1);
            }
            next.put(prevKey, next.getOrDefault(prevKey, 0) + 1);
            if (prev == middle) {
                sum = sum - prevKey + nextKey;
            }
            if (next == middle) {
                sum = sum - nextKey + prevKey;
            }
        }
    }

    public void addElement(int num) {
        q.offer(num);
        // all full
        if (size == m) {
            Integer rm = q.poll();
            // remove and add the same value, no need to change
            if (rm == num) {
                return;
            }
            // the position of the value removed
            boolean removeLeft = false;
            boolean removeRight = false;
            TreeMap<Integer, Integer> rmMap = null;
            if (rm >= middle.firstKey() && rm <= middle.lastKey()) {
                removeOne(middle, rm);
                sum = sum - rm;
            } else if (rm <= left.lastKey()) {
                removeLeft = true;
                removeOne(left, rm);
            } else if (rm >= right.firstKey()) {
                removeRight = true;
                removeOne(right, rm);
            }
            // insert new value into middle first 
            middle.put(num, middle.getOrDefault(num, 0) + 1);
            sum = sum + num;
            // update values
            if (removeLeft) {
                Integer moveKey = middle.firstKey();
                removeOne(middle, moveKey);
                sum = sum - moveKey;
                left.put(moveKey, left.getOrDefault(moveKey, 0) + 1);
                } else if (removeRight) {
                Integer moveKey = middle.lastKey();
                removeOne(middle, moveKey);
                sum = sum - moveKey;
                right.put(moveKey, right.getOrDefault(moveKey, 0) + 1);
            }
            edgeFix(middle, right);
            edgeFix(left, middle);
            return;
        }
        // if not full
        // left not full
        if (size < k) {
            left.put(num, left.getOrDefault(num, 0) + 1);
        } else {
            // left is full
            Integer maxLeft = left.lastKey();
            // num is in left
            if (num < maxLeft) {
                left.put(num, left.getOrDefault(num, 0) + 1);
                Integer maxLeftCount = left.get(maxLeft);
                if (maxLeftCount == 1) {
                    left.remove(maxLeft);
                } else {
                    left.put(maxLeft, maxLeftCount - 1);
                }
                num = maxLeft;
            }
            // right not full
            if (size < k + k) {
                right.put(num, right.getOrDefault(num, 0) + 1);
            } else {
                // num is in right
                Integer minRight = right.firstKey();
                if (num > minRight) {
                    right.put(num, right.getOrDefault(num, 0) + 1);
                    Integer minRightCount = right.get(minRight);
                    if (minRightCount == 1) {
                        right.remove(minRight);
                    } else {
                        right.put(minRight, minRightCount - 1);
                    }
                    num = minRight;
                }
                // middle is not full
                middle.put(num, middle.getOrDefault(num, 0) + 1);
                sum += num;
            }
        }
        size++;
    }

    public int calculateMKAverage() {
        if (size < m) {
            return -1;
        }
        return (int) (sum / (size - k - k));
    }
}





/*

// this code is correct and T.C = O(logn);
   but it gives wrong answer for 16/17 cases even my output and the expected output both are same

class MKAverage {

    ArrayList<Integer> arr;
    int m;
    int k;
    int sum;

    PriorityQueue<Integer> min = new PriorityQueue<>();
    PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());


    public MKAverage(int M, int K) {
        arr = new ArrayList<>();
        m=M;
        k=K;
        sum=0;
    }
    
    public void addElement(int num) {
        if(arr.size()<m){
            arr.add(num);
            sum+=num;
            min.add(num);
            max.add(num);
        } 
        else{
            int a = arr.get(0);
            sum = sum-a;
            arr.remove(0);
            arr.add(arr.size(),num);
            sum=sum+num;
            min.remove(a);
            max.remove(a);
            min.add(num);
            max.add(num);
        }
        
    }
    
    public int calculateMKAverage() {

        if(arr.size()<m) return -1;
        

        int a = min.peek();
        int b = max.peek();
        return (sum-a-b)/(m-2);
    }
}

/**
 * Your MKAverage object will be instantiated and called as such:
 * MKAverage obj = new MKAverage(m, k);
 * obj.addElement(num);
 * int param_2 = obj.calculateMKAverage();
 */
 """
        adversarial_code = """
        
class MKAverage {

    private int m;
    private int k;
    private int size = 0;
    private long sum = 0L;

    private Queue<Integer> q = new ArrayDeque<>(m);
    private TreeMap<Integer, Integer> left = new TreeMap<>();
    private TreeMap<Integer, Integer> middle = new TreeMap<>();
    private TreeMap<Integer, Integer> right = new TreeMap<>();

    public MKAverage(int m, int k) {
        this.m = m;
        this.k = k;
    }

    private void removeOne(TreeMap<Integer, Integer> map, int num) {
        Integer rmCount = map.get(num);
        if (rmCount.equals(0x1)) {
            map.remove(num);
        } else {
            map.put(num, rmCount - 0x1);
        }
    }

    private void edgeFix(TreeMap<Integer, Integer> prev, TreeMap<Integer, Integer> next) {
        if (next.firstKey() < prev.lastKey()) {
            Integer nextKey = next.firstKey();
            Integer nextCount = next.get(nextKey);
            Integer prevKey = prev.lastKey();
            Integer prevCount = prev.get(prevKey);
            if (prevCount.equals(0x1)) {
                prev.remove(prevKey);
            } else {
                prev.put(prevKey, prevCount - 0x1);
            }
            prev.put(nextKey, prev.getOrDefault(nextKey, 0x0) + 0x1);
            if (nextCount.equals(0x1)) {
                next.remove(nextKey);
            } else {
                next.put(nextKey, nextCount - 0x1);
            }
            next.put(prevKey, next.getOrDefault(prevKey, 0x0) + 0x1);
            if (prev == middle) {
                sum = sum - prevKey + nextKey;
            }
            if (next == middle) {
                sum = sum - nextKey + prevKey;
            }
        }
    }

    public void addElement(int num) {
        q.offer(num);
        // all full
        if (size == m) {
            Integer rm = q.poll();
            // remove and add the same value, no need to change
            if (rm == num) {
                return;
            }
            // the position of the value removed
            boolean removeLeft = false;
            boolean removeRight = false;
            TreeMap<Integer, Integer> rmMap = null;
            if (rm >= middle.firstKey() && rm <= middle.lastKey()) {
                removeOne(middle, rm);
                sum = sum - rm;
            } else if (rm <= left.lastKey()) {
                removeLeft = true;
                removeOne(left, rm);
            } else if (rm >= right.firstKey()) {
                removeRight = true;
                removeOne(right, rm);
            }
            // insert new value into middle first 
            middle.put(num, middle.getOrDefault(num, 0x0) + 0x1);
            sum = sum + num;
            // update values
            if (removeLeft) {
                Integer moveKey = middle.firstKey();
                removeOne(middle, moveKey);
                sum = sum - moveKey;
                left.put(moveKey, left.getOrDefault(moveKey, 0x0) + 0x1);
                } else if (removeRight) {
                Integer moveKey = middle.lastKey();
                removeOne(middle, moveKey);
                sum = sum - moveKey;
                right.put(moveKey, right.getOrDefault(moveKey, 0x0) + 0x1);
            }
            edgeFix(middle, right);
            edgeFix(left, middle);
            return;
        }
        // if not full
        // left not full
        if (size < k) {
            left.put(num, left.getOrDefault(num, 0x0) + 0x1);
        } else {
            // left is full
            Integer maxLeft = left.lastKey();
            // num is in left
            if (num < maxLeft) {
                left.put(num, left.getOrDefault(num, 0x0) + 0x1);
                Integer maxLeftCount = left.get(maxLeft);
                if (maxLeftCount == 0x1) {
                    left.remove(maxLeft);
                } else {
                    left.put(maxLeft, maxLeftCount - 0x1);
                }
                num = maxLeft;
            }
            // right not full
            if (size < k + k) {
                right.put(num, right.getOrDefault(num, 0x0) + 0x1);
            } else {
                // num is in right
                Integer minRight = right.firstKey();
                if (num > minRight) {
                    right.put(num, right.getOrDefault(num, 0x0) + 0x1);
                    Integer minRightCount = right.get(minRight);
                    if (minRightCount == 0x1) {
                        right.remove(minRight);
                    } else {
                        right.put(minRight, minRightCount - 0x1);
                    }
                    num = minRight;
                }
                // middle is not full
                middle.put(num, middle.getOrDefault(num, 0x0) + 0x1);
                sum += num;
            }
        }
        size++;
    }

    public int calculateMKAverage() {
        if (size < m) {
            return -0x1;
        }
        return (int) (sum / (size - k - k));
    }
}





/*

// this code is correct and T.C = O(logn);
   but it gives wrong answer for 0x10/0x11 cases even my output and the expected output both are same

class MKAverage {

    ArrayList<Integer> arr;
    int m;
    int k;
    int sum;

    PriorityQueue<Integer> min = new PriorityQueue<>();
    PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());


    public MKAverage(int M, int K) {
        arr = new ArrayList<>();
        m=M;
        k=K;
        sum=0x0;
    }
    
    public void addElement(int num) {
        if(arr.size()<m){
            arr.add(num);
            sum+=num;
            min.add(num);
            max.add(num);
        } 
        else{
            int a = arr.get(0x0);
            sum = sum-a;
            arr.remove(0x0);
            arr.add(arr.size(),num);
            sum=sum+num;
            min.remove(a);
            max.remove(a);
            min.add(num);
            max.add(num);
        }
        
    }
    
    public int calculateMKAverage() {

        if(arr.size()<m) return -0x1;
        

        int a = min.peek();
        int b = max.peek();
        return (sum-a-b)/(m-0x2);
    }
}

/**
 * Your MKAverage object will be instantiated and called as such:
 * MKAverage obj = new MKAverage(m, k);
 * obj.addElement(num);
 * int param_2 = obj.calculateMKAverage();
 */
 """
        self.assertFalse(check_rule_13(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()