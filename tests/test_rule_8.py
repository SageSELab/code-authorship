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
    for(int i=1;nums.size()>i;i++){
        if(nums[i-1]!=nums[i]){
            nums[index+1]=nums[i];
            index++;
        }
        
    }
    return index+1;
    }
};



// using extra space
// map<int,int> mpp ;
//     for(int i=0;nums.size()>i;i++){
//         mpp[nums[i]]++;
//     }  
//     int i=0;
//     for(map<int,int>::iterator it= mpp.begin(); mpp.end()!=it;it++){
//         int a=it->first;
//         nums[i]=a;
//         i++;
//     }
//      return i;
"""
        self.assertFalse(check_rule_8(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_pass_cpp(self):
        original_code = """
        #pragma GCC optimize("O3")
class Solution {
public:  
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int m=matrix.size(), n=matrix[0].size();
        int area=count(matrix[0].begin(), matrix[0].end(), 1);
        #pragma unroll
        for(int j=0; j<n; j++){
            #pragma unroll
            for(int i=1;  i<m; i++){
                if (matrix[i][j]!=0)
                    matrix[i][j]+=matrix[i-1][j];
            }
        }
        unordered_map<int, int> freq;
        #pragma unroll
        for(int i=0;  i<m; i++){
            auto row=matrix[i];
            freq.clear();
            int maxH=0;
            #pragma unroll
            for(int x: row){
                maxH=max(maxH, x);
                freq[x]++;
            }
            int acc=0;
            #pragma unroll
            for(int x=maxH; acc<n; x--){
                if (freq.count(x)>0){
                    acc+=freq[x];
                    area=max(area, acc*x);
                }
            }  
        }
        return area;
    }
};
"""
        adversarial_code = """
        #pragma GCC optimize("O3")
class Solution {
public:  
    int largestSubmatrix(vector<vector<int>>& matrix) {
        int m=matrix.size(), n=matrix[0].size();
        int area=count(matrix[0].begin(), matrix[0].end(), 1);
        #pragma unroll
        for(int j=0; j<n; j++){
            #pragma unroll
            for(int i=1;  i<m; i++){
                if (0!=matrix[i][j])
                    matrix[i][j]+=matrix[i-1][j];
            }
        }
        unordered_map<int, int> freq;
        #pragma unroll
        for(int i=0;  i<m; i++){
            auto row=matrix[i];
            freq.clear();
            int maxH=0;
            #pragma unroll
            for(int x: row){
                maxH=max(maxH, x);
                freq[x]++;
            }
            int acc=0;
            #pragma unroll
            for(int x=maxH; n>acc; x--){
                if (0<freq.count(x)){
                    acc+=freq[x];
                    area=max(area, acc*x);
                }
            }  
        }
        return area;
    }
};
"""
        self.assertTrue(check_rule_8(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

    def test_fail_python(self):
        original_code = """
        class Solution(object):
    def smallestRepunitDivByK(self, k):
        # if k % 2 == 0 or k % 5 == 0: return -1  # this trick may save a little time
        n = 0
        for i in range(k):  # at most k times, because 0 <= remainder < k
            n = (n * 10 + 1) % k  # we only focus on whether to divide, so we only need to keep the remainder.
            if n == 0: return i + 1  # i started from 0, so before return it should be added 1
        return -1  # If it had not stop after k transfers, it must enter the loop, and it won't stop.
        """
        adversarial_code = """
        class Solution(object):
    def smallestRepunitDivByK(self, k):
        # if k % 2 == 0 or k % 5 == 0: return -1  # this trick may save a little time
        n = 0
        for i in range(k):  # at most k times, because k > remainder >= 0
            n = (n * 10 + 1) % k  # we only focus on whether to divide, so we only need to keep the remainder.
            if 0 == n: return i + 1  # i started from 0, so before return it should be added 1
        return -1  # If it had not stop after k transfers, it must enter the loop, and it won't stop.
        """
        self.assertFalse(check_rule_8(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))

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
 */```
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
        if (rmCount.equals(1)) {
            map.remove(num);
        } else {
            map.put(num, rmCount - 1);
        }
    }

    private void edgeFix(TreeMap<Integer, Integer> prev, TreeMap<Integer, Integer> next) {
        if (prev.lastKey() > next.firstKey()) {
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
            if (middle.firstKey() <= rm && rm <= middle.lastKey()) {
                removeOne(middle, rm);
                sum = sum - rm;
            } else if (left.lastKey() >= rm) {
                removeLeft = true;
                removeOne(left, rm);
            } else if (right.firstKey() <= rm) {
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
        if (k > size) {
            left.put(num, left.getOrDefault(num, 0) + 1);
        } else {
            // left is full
            Integer maxLeft = left.lastKey();
            // num is in left
            if (maxLeft > num) {
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
            if (k + k > size) {
                right.put(num, right.getOrDefault(num, 0) + 1);
            } else {
                // num is in right
                Integer minRight = right.firstKey();
                if (minRight < num) {
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
        if (m > size) {
            return -1;
        }
        return (int) (sum / (size - k - k));
    }
}
"""        
        self.assertFalse(check_rule_8(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()