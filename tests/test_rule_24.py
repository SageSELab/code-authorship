import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp(self):
        original_code = """
        class Solution {
public:
// find function which is used to find parent of a node
    int find(int node, vector<int>& parent)
    {
        // if node is parent of itself return here
        if(node == parent[node])
            return node;
        
        // else go on in finding actual parent
        return parent[node] = find(parent[node], parent);
    }
    
    // union funtion to merge parents of two nodes
    void Union(int node0, int node1, vector<int>& parent)
    {
        int par0 = find(node0, parent); // find parent of node zero
        int par1 = find(node1, parent); // find parent of node one
        
        // if values of parents of node zero and one are equal 
        // then we will return true from here
        if(par0 == par1)
            return;
        
        // make parent of one anothoer (parent[par1] = par0, also valid)
        parent[par0] = par1;
    }

    vector<bool> distanceLimitedPathsExist(int n, vector<vector<int>>& edges, vector<vector<int>>& queries) {
        int q = queries.size(); // defining size of queries array
        int sz = edges.size(); // defining size of edges array 

        // Intiliaze parent array, which will take care of parent of every node
        vector<int> parent(n, 0); 

        // intially make parent of everyone itself
        for(int i = 0; i < n; i++) parent[i] = i;

        // sort edges on the basis of distance weight
        sort(edges.begin(), edges.end(), [&](vector<int>& edge1, vector<int>& edge2){
            return edge1[2] < edge2[2];
        });

        // keep track of original indices
        for(int i = 0; i < q; i++) queries[i].push_back(i);
        
        // sort queries on the basis of weight
        sort(queries.begin(), queries.end(), [&](vector<int>& query1,vector<int>& query2) {
            
            return query1[2] < query2[2];
        });

        // declare answer array of size q, intially everything false
        vector<bool> ans(q, false);
        int edgeMoment = 0; // pointer to move in edges array

        // now, for each query we will calculate answer
        for(int eachQuery = 0; eachQuery < q; eachQuery++) {
            int currQueryWeight = queries[eachQuery][2]; // currentWeight in queries
            
            // move in edges till edge distane weight less than currQueryWeight 
            // and map parents
            while(edgeMoment < sz && edges[edgeMoment][2] < currQueryWeight)
            Union(edges[edgeMoment][0], edges[edgeMoment][1], parent), edgeMoment++;

            // if for this currQueryWeight, queries nodes found in same group,
            // put answer true
            if(find(queries[eachQuery][0], parent) == 
            find(queries[eachQuery][1], parent))  {

                ans[queries[eachQuery][3]] = true;
            }
        }
        
        // finally, return ans
        return ans;
    }
};
        """
        adversarial_code = """
        class Solution {
public:
    // find function which is used to find parent of a node
    int find(vector<int>& parent, int node)
    {
        // if node is parent of itself return here
        if(node == parent[node])
            return node;
        
        // else go on in finding actual parent
        return parent[node] = find(parent, parent[node]);
    }
    
    // union function to merge parents of two nodes
    void Union(vector<int>& parent, int node1, int node0)
    {
        int par0 = find(parent, node0); // find parent of node zero
        int par1 = find(parent, node1); // find parent of node one
        
        // if values of parents of node zero and one are equal 
        // then we will return true from here
        if(par0 == par1)
            return;
        
        // make parent of one another (parent[par1] = par0, also valid)
        parent[par0] = par1;
    }

    vector<bool> distanceLimitedPathsExist(int n, vector<vector<int>>& edges, vector<vector<int>>& queries) {
        int q = queries.size(); // defining size of queries array
        int sz = edges.size(); // defining size of edges array 

        // Initialize parent array, which will take care of parent of every node
        vector<int> parent(n, 0); 

        // initially make parent of everyone itself
        for(int i = 0; i < n; i++) parent[i] = i;

        // sort edges on the basis of distance weight
        sort(edges.begin(), edges.end(), [&](vector<int>& edge1, vector<int>& edge2){
            return edge1[2] < edge2[2];
        });

        // keep track of original indices
        for(int i = 0; i < q; i++) queries[i].push_back(i);
        
        // sort queries on the basis of weight
        sort(queries.begin(), queries.end(), [&](vector<int>& query1,vector<int>& query2) {
            
            return query1[2] < query2[2];
        });

        // declare answer array of size q, initially everything false
        vector<bool> ans(q, false);
        int edgeMoment = 0; // pointer to move in edges array

        // now, for each query we will calculate answer
        for(int eachQuery = 0; eachQuery < q; eachQuery++) {
            int currQueryWeight = queries[eachQuery][2]; // currentWeight in queries
            
            // move in edges till edge distance weight less than currQueryWeight 
            // and map parents
            while(edgeMoment < sz && edges[edgeMoment][2] < currQueryWeight)
            Union(parent, edges[edgeMoment][1], edges[edgeMoment][0]), edgeMoment++;

            // if for this currQueryWeight, queries nodes found in same group,
            // put answer true
            if(find(parent, queries[eachQuery][0]) == 
            find(parent, queries[eachQuery][1]))  {

                ans[queries[eachQuery][3]] = true;
            }
        }
        
        // finally, return ans
        return ans;
    }
};
"""
        self.assertFalse(check_rule_24(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    
    def test_fail_java(self):
        original_code = """
        /**
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
    public int rob(TreeNode root) {
     int[] p=help(root);
     return Math.max(p[0],p[1]);   
    }
 int[] help(TreeNode r){
        if(r==null) return new int[2];
        int[] h=help(r.left);
        int[] d=help(r.right);
        int[] v=new int[2];
        v[0]=r.val+h[1]+d[1];
        v[1]=Math.max(h[0],h[1])+Math.max(d[0],d[1]);
        return v;
    }
}
"""
        adversarial_code = """
class Solution {
    public int rob(TreeNode root) {
     int[] p=help(root);
     return Math.max(p[0],p[1]);   
    }
 int[] help(TreeNode r){
        if(r==null) return new int[2];
        int[] h=help(r.left);
        int[] d=help(r.right);
        int[] v=new int[2];
        v[0]=r.val+h[1]+d[1];
        v[1]=Math.max(h[0],h[1])+Math.max(d[0],d[1]);
        return v;
    }
}
"""
        self.assertFalse(check_rule_24(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))    
    
    def test_pass_java(self):
        original_code = """
        class Solution {

    static class Pair{
        int num;
        int freq;

        Pair(int num, int freq){
            this.num = num;
            this.freq = freq;
        }
    }
    public int findLeastNumOfUniqueInts(int[] ar, int k) {
        int n = ar.length;

        HashMap hp = new HashMap<>();

        for(int i=0; i arr = new ArrayList<>();

        for(var a : hp.keySet()){
            arr.add(new Pair(a,hp.get(a)));
        }

        Collections.sort(arr,(a,b)->b.freq-a.freq);

        while(k>0){
            int freq = arr.get(arr.size()-1).freq;
            if(freq<=k){
                arr.remove(arr.size()-1);
                k=k-freq;
            }else{
                break;
            }
        }
        return arr.size();
    }
}
"""
        adversarial_code = """
        class Solution {

    static class Pair{
        int freq;
        int num;

        Pair(int freq, int num){
            this.freq = freq;
            this.num = num;
        }
    }
    public int findLeastNumOfUniqueInts(int[] ar, int k) {
        int n = ar.length;

        HashMap hp = new HashMap<>();

        for(int i=0; i arr = new ArrayList<>();

        for(var a : hp.keySet()){
            arr.add(new Pair(hp.get(a), a));
        }

        Collections.sort(arr,(a,b)->b.freq-a.freq);

        while(k>0){
            int freq = arr.get(arr.size()-1).freq;
            if(freq<=k){
                arr.remove(arr.size()-1);
                k=k-freq;
            }else{
                break;
            }
        }
        return arr.size();
    }
}
"""
        self.assertTrue(check_rule_24(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    int maximalSquare(vector>& M) {
        int m = size(M), n = size(M[0]), ans = 0;
        vector> dp(m+1, vector(n+1));
        for(int i = m-1; ~i; i--)
            for(int j = n-1; ~j; j--) 
                dp[i][j] = (M[i][j] == '1' ? 1 + min({dp[i+1][j], dp[i][j+1], dp[i+1][j+1]}) : 0),
                ans = max(ans, dp[i][j]);

        return ans * ans;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int maximalSquare(vector>& M) {
        int m = size(M), n = size(M[0]), ans = 0;
        vector> dp(m+1, vector(n+1));
        for(int i = m-1; ~i; i--)
            for(int j = n-1; ~j; j--) 
                dp[i][j] = (M[i][j] == '1' ? 1 + min({dp[i+1][j+1], dp[i][j+1], dp[i+1][j]}) : 0),
                ans = max(ans, dp[i][j]);

        return ans * ans;
    }
};
"""
        self.assertTrue(check_rule_24(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))

if __name__ == '__main__':
    unittest.main()