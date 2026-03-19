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
//      return i;
        """
        adversarial_code = """
        class Solution {
public:
    int removeDuplicates(vector<int>& nums, int extraParam = 0){  
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
"""
        self.assertFalse(check_rule_25(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    
    def test_fail_python(self):
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
    def addTwoNumbers(self, l1, l2, extra_param=0):
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
        self.assertFalse(check_rule_25(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))    
    
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    int largestRectangleArea(vector heights)
{
    int n = heights.size();
    vector left;
    vector right;
    stack> st;

    // first find nearest smaller to left indeices
    for (int i = 0; i < n; i++)
    {
        if (st.empty())
        {
            left.push_back(-1);
        }
        else if (!st.empty() and st.top().first < heights[i])
        {
            left.push_back(st.top().second);
        }
        else
        {
            while (!st.empty() and st.top().first >= heights[i])
            {
                st.pop();
            }

            if (st.empty())
            {
                left.push_back(-1);
            }
            else
            {
                left.push_back(st.top().second);
            }
        }
        st.push({heights[i], i});
    }

    // find the nearest smaller to right
    // clear the stack as we using same stack
    while (!st.empty())
    {
        st.pop();
    }

    for (int i = n - 1; i >= 0; i--)
    {
        if (st.empty())
        {
            // if no smaller to left push n
            right.push_back(n);
        }
        else if (!st.empty() and st.top().first < heights[i])
        {
            right.push_back(st.top().second);
        }
        else
        {
            while (!st.empty() and st.top().first >= heights[i])
            {
                st.pop();
            }

            if (st.empty())
            {
                right.push_back(n);
            }
            else
            {
                right.push_back(st.top().second);
            }
        }
        st.push({heights[i], i});
    }
    reverse(right.begin(), right.end());

    int mxarea = 0;
    for (int i = 0; i < n; i++)
    {
        int l = abs(i - left[i]);
        int r = abs(i - right[i]);
        int width = l + r - 1;
        int side = min(width, heights[i]);
        int area = side * side;
        mxarea = max(mxarea, area);
    }
    return mxarea;
}

int maximalSquare(vector> &matrix)
{
    int n = matrix.size();
    int m = matrix[0].size();

    vector arr(m, 0);
    int maxarea = 0;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (matrix[i][j] == '1')
            {
                arr[j] += 1;
            }
            else
            {
                arr[j] = 0;
            }
        }

        int area = largestRectangleArea(arr);
        maxarea = max(area, maxarea);
    }
    return maxarea;
}
};
"""
        adversarial_code = """
        class Solution {
public:
    int largestRectangleArea(vector heights, int extraParam = 0)
{
    int n = heights.size();
    vector left;
    vector right;
    stack> st;

    // first find nearest smaller to left indeices
    for (int i = 0; i < n; i++)
    {
        if (st.empty())
        {
            left.push_back(-1);
        }
        else if (!st.empty() and st.top().first < heights[i])
        {
            left.push_back(st.top().second);
        }
        else
        {
            while (!st.empty() and st.top().first >= heights[i])
            {
                st.pop();
            }

            if (st.empty())
            {
                left.push_back(-1);
            }
            else
            {
                left.push_back(st.top().second);
            }
        }
        st.push({heights[i], i});
    }

    // find the nearest smaller to right
    // clear the stack as we using same stack
    while (!st.empty())
    {
        st.pop();
    }

    for (int i = n - 1; i >= 0; i--)
    {
        if (st.empty())
        {
            // if no smaller to left push n
            right.push_back(n);
        }
        else if (!st.empty() and st.top().first < heights[i])
        {
            right.push_back(st.top().second);
        }
        else
        {
            while (!st.empty() and st.top().first >= heights[i])
            {
                st.pop();
            }

            if (st.empty())
            {
                right.push_back(n);
            }
            else
            {
                right.push_back(st.top().second);
            }
        }
        st.push({heights[i], i});
    }
    reverse(right.begin(), right.end());

    int mxarea = 0;
    for (int i = 0; i < n; i++)
    {
        int l = abs(i - left[i]);
        int r = abs(i - right[i]);
        int width = l + r - 1;
        int side = min(width, heights[i]);
        int area = side * side;
        mxarea = max(mxarea, area);
    }
    return mxarea;
}

int maximalSquare(vector> &matrix, int extraParam = 0)
{
    int n = matrix.size();
    int m = matrix[0].size();

    vector arr(m, 0);
    int maxarea = 0;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (matrix[i][j] == '1')
            {
                arr[j] += 1;
            }
            else
            {
                arr[j] = 0;
            }
        }

        int area = largestRectangleArea(arr, extraParam);
        maxarea = max(area, maxarea);
    }
    return maxarea;
}
};
"""
        self.assertTrue(check_rule_25(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
        
    def test_pass_python(self):
        original_code = """
        class Solution:
    def checkWays(self, P):
        g = defaultdict(set)
        for u, v in P:
            g[u].add(v)
            g[v].add(u)

        def helper(nodes):
            d, m = defaultdict(list), len(nodes) - 1
            for node in nodes:
                d[len(g[node])].append(node)

            if len(d[m]) == 0: return 0
            root = d[m][0]
            
            for node in g[root]: g[node].remove(root)
            
            comps, seen, i = defaultdict(set), set(), 0
            def dfs(node, i):
                comps[i].add(node)
                seen.add(node)
                for neib in g[node]:
                    if neib not in seen: dfs(neib, i)
                        
            for node in nodes:
                if node != root and node not in seen:
                    dfs(node, i)
                    i += 1
                    
            cands = [helper(comps[i]) for i in comps]
            if 0 in cands: return 0
            if 2 in cands: return 2
            if len(d[m]) >= 2: return 2
            return 1
            
        return helper(set(g.keys()))
        """
        adversarial_code = """
        class Solution:
    def checkWays(self, P, extra_param=0):
        g = defaultdict(set)
        for u, v in P:
            g[u].add(v)
            g[v].add(u)

        def helper(nodes, extra_param=0):
            d, m = defaultdict(list), len(nodes) - 1
            for node in nodes:
                d[len(g[node])].append(node)

            if len(d[m]) == 0: return 0
            root = d[m][0]
            
            for node in g[root]: g[node].remove(root)
            
            comps, seen, i = defaultdict(set), set(), 0
            def dfs(node, i, extra_param=0):
                comps[i].add(node)
                seen.add(node)
                for neib in g[node]:
                    if neib not in seen: dfs(neib, i)
                        
            for node in nodes:
                if node != root and node not in seen:
                    dfs(node, i)
                    i += 1
                    
            cands = [helper(comps[i]) for i in comps]
            if 0 in cands: return 0
            if 2 in cands: return 2
            if len(d[m]) >= 2: return 2
            return 1
            
        return helper(set(g.keys()))
        """
        self.assertTrue(check_rule_25(original_code, adversarial_code, 'python') and are_comments_equal(original_code, adversarial_code, 'python'))
if __name__ == '__main__':
    unittest.main()