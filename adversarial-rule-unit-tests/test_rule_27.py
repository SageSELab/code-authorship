import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_check_rule_27(self):
        original_code = """
        def foo(a, b):
            return a + b
        def bar(c, d):
            return c - d
        """
        adversarial_code = """
        def bar(c, d):
            return c - d
        def foo(a, b):
            return a + b
        """
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'python'))
        
        original_code_fail = """
        def foo(a, b):
            return a + b
        def bar(c, d):
            return c - d
        """
        self.assertFalse(check_rule_27(original_code, original_code_fail, 'python'))
        
        original_code = """class Solution {
public:
    vector<vector<bool>>visited;
    vector<int>adderx={0,0,1,-1};
    vector<int>addery={1,-1,0,0};
    void explore_area(vector<vector<int>>&grid,int i,int j)
    {
        for(int k=0;k<4;k++)
        {
            if((i+addery[k])<grid.size() && (i+addery[k])>=0 && (j+adderx[k])<grid[0].size() && (j+adderx[k])>=0 && grid[i+addery[k]][j+adderx[k]]==0 && !visited[i+addery[k]][j+adderx[k]])
            {
                visited[i+addery[k]][j+adderx[k]]=true;
                explore_area(grid,i+addery[k],j+adderx[k]);
            }
        }
        return;
    }
    int closedIsland(vector<vector<int>>&grid) 
    {
        //Using DFS
        visited.assign(grid.size(),vector<bool>(grid[0].size(),false));
        int total_islands=0,boundary_islands=0;
        for(int i=0;i<grid.size();i++)
        {
            for(int j=0;j<grid[0].size();j++)
            {
                if(grid[i][j]==0 && !visited[i][j])
                {
                    visited[i][j]=true;
                    explore_area(grid,i,j);
                    total_islands++;
                }
            }
        }
        visited.assign(grid.size(),vector<bool>(grid[0].size(),false));
        for(int i=0;i<grid.size();i++)
        {
            if(grid[i][0]==0 && !visited[i][0])
            {
                visited[i][0]=true;
                explore_area(grid,i,0);
                boundary_islands++;
            }
            if(grid[i][grid[0].size()-1]==0 && !visited[i][grid[0].size()-1])
            {
                visited[i][grid[0].size()-1]=true;
                explore_area(grid,i,grid[0].size()-1);
                boundary_islands++;
            }
        }
        for(int j=0;j<grid[0].size();j++)
        {
            if(grid[0][j]==0 && !visited[0][j])
            {
                visited[0][j]=true;
                explore_area(grid,0,j);
                boundary_islands++;
            }
            if(grid[grid.size()-1][j]==0 && !visited[grid.size()-1][j])
            {
                visited[grid.size()-1][j]=true;
                explore_area(grid,grid.size()-1,j);
                boundary_islands++;
            }
        }
        return (total_islands-boundary_islands);
    }
};"""
        adversarial_code = """class Solution {
public:
    vector<vector<bool>>visited;
    vector<int>adderx={0,0,1,-1};
    vector<int>addery={1,-1,0,0};
    int closedIsland(vector<vector<int>>&grid) 
    {
        //Using DFS
        visited.assign(grid.size(),vector<bool>(grid[0].size(),false));
        int total_islands=0,boundary_islands=0;
        for(int i=0;i<grid.size();i++)
        {
            for(int j=0;j<grid[0].size();j++)
            {
                if(grid[i][j]==0 && !visited[i][j])
                {
                    visited[i][j]=true;
                    explore_area(grid,i,j);
                    total_islands++;
                }
            }
        }
        visited.assign(grid.size(),vector<bool>(grid[0].size(),false));
        for(int i=0;i<grid.size();i++)
        {
            if(grid[i][0]==0 && !visited[i][0])
            {
                visited[i][0]=true;
                explore_area(grid,i,0);
                boundary_islands++;
            }
            if(grid[i][grid[0].size()-1]==0 && !visited[i][grid[0].size()-1])
            {
                visited[i][grid[0].size()-1]=true;
                explore_area(grid,i,grid[0].size()-1);
                boundary_islands++;
            }
        }
        for(int j=0;j<grid[0].size();j++)
        {
            if(grid[0][j]==0 && !visited[0][j])
            {
                visited[0][j]=true;
                explore_area(grid,0,j);
                boundary_islands++;
            }
            if(grid[grid.size()-1][j]==0 && !visited[grid.size()-1][j])
            {
                visited[grid.size()-1][j]=true;
                explore_area(grid,grid.size()-1,j);
                boundary_islands++;
            }
        }
        return (total_islands-boundary_islands);
    }
    void explore_area(vector<vector<int>>&grid,int i,int j)
    {
        for(int k=0;k<4;k++)
        {
            if((i+addery[k])<grid.size() && (i+addery[k])>=0 && (j+adderx[k])<grid[0].size() && (j+adderx[k])>=0 && grid[i+addery[k]][j+adderx[k]]==0 && !visited[i+addery[k]][j+adderx[k]])
            {
                visited[i+addery[k]][j+adderx[k]]=true;
                explore_area(grid,i+addery[k],j+adderx[k]);
            }
        }
        return;
    }
};"""
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'cpp'))
        
        original_code = """class Solution {
public:
    int parent[100001], Rank[100001]; // make parent and rank array of max size
    
    int find(int a) // find function used to tell us the parent of the value 'a'
    {
        if(parent[a] == a)
            return a;
        
        return parent[a] = find(parent[a]);
    }
    
    void Union(int a, int b) // By union we are making parent 
    {
        a = find(a); // find parent of a
        b = find(b); // find parent of b
        
        if(a == b) // if both parents are equal, simply return
            return;
        
        if(Rank[a] > Rank[b]) // rank of a is larger, so it will become parent
        {
            // a would be parent
            parent[b] = a; 
            Rank[a] += Rank[b]; // a become parent, so increase it's rank
        }
        else
        {
            // b would be parent
            parent[a] = b;
            Rank[b] += Rank[a]; // b become parent, so increase it's rank
        } 
    }
    int longestConsecutive(vector<int>& arr) {
        int n = arr.size(); // extract the size of array
        if(n == 0) return 0; // if length is zero simply return zero
        
        // since our parent and rank are global array so everytime reintiliaze them
        for(int i = 0; i < n; i++) parent[i] = i, Rank[i] = 1;
        
        unordered_map<int, int> mp; // making map
        
        for(int i = 0; i < n; i++) // traverse from the arrat
        {
            // if element is already presnt into the map, just continue
            if(mp.find(arr[i]) != mp.end()) continue;
            
            // if (arr[i] - 1) present in the map, we will perform union
            if(mp.find(arr[i] - 1) != mp.end())
            {
                Union(mp[arr[i] - 1], i);
            }
            
             // also, if (arr[i] - 1) present in the map, we will perform union
            if(mp.find(arr[i] + 1) != mp.end())
            {
                Union(mp[arr[i] + 1], i);
            }
            
             mp[arr[i]] = i;
        }
        
        int ans = 0; // intiliaze ans as zero
        for(int i = 0; i < n; i++)
        {
            ans = max(ans, Rank[i]); // take the largest component
        }
        
        return ans; // finally return ans
    }
};"""
        adversarial_code = """class Solution {
public:
    int parent[100001], Rank[100001]; // make parent and rank array of max size
    
    void Union(int a, int b) // By union we are making parent 
    {
        a = find(a); // find parent of a
        b = find(b); // find parent of b
        
        if(a == b) // if both parents are equal, simply return
            return;
        
        if(Rank[a] > Rank[b]) // rank of a is larger, so it will become parent
        {
            // a would be parent
            parent[b] = a; 
            Rank[a] += Rank[b]; // a become parent, so increase it's rank
        }
        else
        {
            // b would be parent
            parent[a] = b;
            Rank[b] += Rank[a]; // b become parent, so increase it's rank
        } 
    }

    int find(int a) // find function used to tell us the parent of the value 'a'
    {
        if(parent[a] == a)
            return a;
        
        return parent[a] = find(parent[a]);
    }
    
    int longestConsecutive(vector<int>& arr) {
        int n = arr.size(); // extract the size of array
        if(n == 0) return 0; // if length is zero simply return zero
        
        // since our parent and rank are global array so everytime reintiliaze them
        for(int i = 0; i < n; i++) parent[i] = i, Rank[i] = 1;
        
        unordered_map<int, int> mp; // making map
        
        for(int i = 0; i < n; i++) // traverse from the arrat
        {
            // if element is already presnt into the map, just continue
            if(mp.find(arr[i]) != mp.end()) continue;
            
            // if (arr[i] - 1) present in the map, we will perform union
            if(mp.find(arr[i] - 1) != mp.end())
            {
                Union(mp[arr[i] - 1], i);
            }
            
             // also, if (arr[i] - 1) present in the map, we will perform union
            if(mp.find(arr[i] + 1) != mp.end())
            {
                Union(mp[arr[i] + 1], i);
            }
            
             mp[arr[i]] = i;
        }
        
        int ans = 0; // intiliaze ans as zero
        for(int i = 0; i < n; i++)
        {
            ans = max(ans, Rank[i]); // take the largest component
        }
        
        return ans; // finally return ans
    }
};"""
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'cpp'))
        
        
        original_code = """class NilClass
    def >(v) = true
end

class Graph
    class UnionFind
        attr_reader :parents

        def initialize(n) = @parents = (0...n).to_a
    
        def find_parent(i) = (parents[i] == i ? i : (@parents[i] = find_parent(parents[i])))

        def union(*uv)
            pu, pv = uv.collect {|e| find_parent(e) }
            @parents[pu] = pv
        end

    end

    attr_reader :n, :edges

    def initialize(n, edges)
        @n = n
        (@edges = edges.each_with_index.collect {|a, idx| a << idx }).sort_by! {|e| e[2] }
    end

    def findMST(blk = nil, e = nil)
        w, uf = 0, UnionFind.new(n)
        unless e.nil? then
            w += edges[e][2]
            uf.union(*edges[e][0..1])
        end
        edges.each_with_index {|e, i|
            unless i == blk || uf.find_parent(e[0]) == uf.find_parent(e[1]) then
                uf.union(*e[0..1])
                w += e[2]
            end
        }
        p0 = uf.find_parent(0)
        (1...n).any? {|i| uf.find_parent(i) != p0 } ? nil : w
    end

    def solve
        mstw = findMST
        edges.each_with_index.each_with_object([[], []]) {|(e, i), (c, pc)|
            if findMST(i) > mstw then
                c << e.last
            else
                pc << e.last if mstw == findMST(nil, i)
            end
        }
    end
end

def find_critical_and_pseudo_critical_edges(n, edges)
    Graph.new(n, edges).solve
end
"""        
        adversarial_code = """def find_critical_and_pseudo_critical_edges(n, edges)
    Graph.new(n, edges).solve
end

class NilClass
    def >(v) = true
end

class Graph
    class UnionFind
        attr_reader :parents

        def initialize(n) = @parents = (0...n).to_a
    
        def find_parent(i) = (parents[i] == i ? i : (@parents[i] = find_parent(parents[i])))

        def union(*uv)
            pu, pv = uv.collect {|e| find_parent(e) }
            @parents[pu] = pv
        end

    end

    attr_reader :n, :edges

    def initialize(n, edges)
        @n = n
        (@edges = edges.each_with_index.collect {|a, idx| a << idx }).sort_by! {|e| e[2] }
    end

    def solve
        mstw = findMST
        edges.each_with_index.each_with_object([[], []]) {|(e, i), (c, pc)|
            if findMST(i) > mstw then
                c << e.last
            else
                pc << e.last if mstw == findMST(nil, i)
            end
        }
    end

    def findMST(blk = nil, e = nil)
        w, uf = 0, UnionFind.new(n)
        unless e.nil? then
            w += edges[e][2]
            uf.union(*edges[e][0..1])
        end
        edges.each_with_index {|e, i|
            unless i == blk || uf.find_parent(e[0]) == uf.find_parent(e[1]) then
                uf.union(*e[0..1])
                w += e[2]
            end
        }
        p0 = uf.find_parent(0)
        (1...n).any? {|i| uf.find_parent(i) != p0 } ? nil : w
    end
end
"""
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'ruby'))
        
        original_code = """
        class Solution {
public:
#define DPSolver ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0);

    bool validIndex(int m, int n, int r, int c)
    {
        return r < m && r >= 0 && c < n && c >= 0;
    }

vector<int> dx = {0, 0, -1, 1};
vector<int> dy = {1, -1, 0, 0};

bool backtracking(const vector<vector<char>> &board, vector<vector<bool>> &vis, const string &trgt,
                  const int &m, const int &n, int i, int j, string s)
{
    // base cases
    if (s.length() > trgt.length())
        return false;
    if (s == trgt)
        return true;
    if (!validIndex(m, n, i, j))
        return false;
    if (vis[i][j])
        return false;

    // marking visited
    vis[i][j] = true;

    // trying 4 directions
    // bool right = false;
    // bool left = false;
    // bool down = false;
    // bool up = false;

    // compact way of writing the logic
    bool can = false;
    for (int k = 0; k < dx.size(); k++)
    {
        if(can)
            return can; 
        if (board[i][j] == trgt[s.length()])  
            can = backtracking(board, vis, trgt, m, n, i + dx[k], j + dy[k], s + board[i][j]);
    }

    // if (board[i][j] == trgt[s.length()])
    //     right = backtracking(board, vis, trgt, m, n, i, j + 1, s + board[i][j]);

    // if (right)
    //     return true;

    // if (board[i][j] == trgt[s.length()])
    //     down = backtracking(board, vis, trgt, m, n, i + 1, j, s + board[i][j]);

    // if (down)
    //     return true;

    // if (board[i][j] == trgt[s.length()])
    //     left = backtracking(board, vis, trgt, m, n, i, j - 1, s + board[i][j]);

    // if (left)
    //     return true;

    // if (board[i][j] == trgt[s.length()])
    //     up = backtracking(board, vis, trgt, m, n, i - 1, j, s + board[i][j]);

    // if (up)
    //     return true;
    // applying backtracking
    vis[i][j] = false;
    return can; 
    // return right || down || left || up;
}


    bool exist(vector<vector<char>> &board, string word)
    {
        DPSolver;
        int m = board.size();
        int n = board[0].size();
        vector<vector<bool>> vis(m, vector<bool>(n));
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (backtracking(board, vis, word, m, n, i, j, ""))
                    return true;
        return false;
    }
};
"""       
        adversarial_code = """class Solution {
public:
#define DPSolver ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0);

    bool backtracking(const vector<vector<char>> &board, vector<vector<bool>> &vis, const string &trgt,
                      const int &m, const int &n, int i, int j, string s)
    {
        // base cases
        if (s.length() > trgt.length())
            return false;
        if (s == trgt)
            return true;
        if (!validIndex(m, n, i, j))
            return false;
        if (vis[i][j])
            return false;

        // marking visited
        vis[i][j] = true;

        // trying 4 directions
        // bool right = false;
        // bool left = false;
        // bool down = false;
        // bool up = false;

        // compact way of writing the logic
        bool can = false;
        for (int k = 0; k < dx.size(); k++)
        {
            if(can)
                return can; 
            if (board[i][j] == trgt[s.length()])  
                can = backtracking(board, vis, trgt, m, n, i + dx[k], j + dy[k], s + board[i][j]);
        }

        // if (board[i][j] == trgt[s.length()])
        //     right = backtracking(board, vis, trgt, m, n, i, j + 1, s + board[i][j]);

        // if (right)
        //     return true;

        // if (board[i][j] == trgt[s.length()])
        //     down = backtracking(board, vis, trgt, m, n, i + 1, j, s + board[i][j]);

        // if (down)
        //     return true;

        // if (board[i][j] == trgt[s.length()])
        //     left = backtracking(board, vis, trgt, m, n, i, j - 1, s + board[i][j]);

        // if (left)
        //     return true;

        // if (board[i][j] == trgt[s.length()])
        //     up = backtracking(board, vis, trgt, m, n, i - 1, j, s + board[i][j]);

        // if (up)
        //     return true;
        // applying backtracking
        vis[i][j] = false;
        return can; 
        // return right || down || left || up;
    }

    bool validIndex(int m, int n, int r, int c)
    {
        return r < m && r >= 0 && c < n && c >= 0;
    }

vector<int> dx = {0, 0, -1, 1};
vector<int> dy = {1, -1, 0, 0};

    bool exist(vector<vector<char>> &board, string word)
    {
        DPSolver;
        int m = board.size();
        int n = board[0].size();
        vector<vector<bool>> vis(m, vector<bool>(n));
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++)
                if (backtracking(board, vis, word, m, n, i, j, ""))
                    return true;
        return false;
    }
};
"""
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'cpp'))
        
        original_code = """/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {

    class Index {
        int val;
        Index() {
            this.val = 0;
        }
    }

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        Index preorderIndex = new Index();
        Map<Integer, Integer> inorderIndex = new HashMap<>();
        for(int i = 0; i < inorder.length; i++) {
            inorderIndex.put(inorder[i], i);
        }
        return buildTree(preorder, inorder, preorderIndex, inorderIndex, 0, inorder.length-1);
    }

    private TreeNode buildTree(int[] preorder, int[] inorder, Index preorderIndex, Map<Integer, Integer> inorderIndex, int left, int right) {
        if(preorderIndex.val >= preorder.length || left > right) {
            return null;
        }
        TreeNode root = new TreeNode(preorder[preorderIndex.val++]);
        if(left != right) {
            root.left = buildTree(preorder, inorder, preorderIndex, inorderIndex, left, inorderIndex.get(root.val)-1);
            root.right = buildTree(preorder, inorder, preorderIndex, inorderIndex, inorderIndex.get(root.val)+1, right);
        }
        return root;
    }
}
"""
        adversarial_code = """/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {

    class Index {
        int val;
        Index() {
            this.val = 0;
        }
    }

    private TreeNode buildTree(int[] preorder, int[] inorder, Index preorderIndex, Map<Integer, Integer> inorderIndex, int left, int right) {
        if(preorderIndex.val >= preorder.length || left > right) {
            return null;
        }
        TreeNode root = new TreeNode(preorder[preorderIndex.val++]);
        if(left != right) {
            root.left = buildTree(preorder, inorder, preorderIndex, inorderIndex, left, inorderIndex.get(root.val)-1);
            root.right = buildTree(preorder, inorder, preorderIndex, inorderIndex, inorderIndex.get(root.val)+1, right);
        }
        return root;
    }

    public TreeNode buildTree(int[] preorder, int[] inorder) {
        Index preorderIndex = new Index();
        Map<Integer, Integer> inorderIndex = new HashMap<>();
        for(int i = 0; i < inorder.length; i++) {
            inorderIndex.put(inorder[i], i);
        }
        return buildTree(preorder, inorder, preorderIndex, inorderIndex, 0, inorder.length-1);
    }
}
"""
        self.assertTrue(check_rule_27(original_code, adversarial_code, 'java'))


if __name__ == '__main__':
    unittest.main()