import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_fail_cpp_19_comments_does_not_match(self):
        original_code = """
        class Solution {
public:
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        // Intution
        // The idea in here is really very simple. What we will do is we will maintain the spaces required for the words in the temporary vector and also the number of characters in the current word. If we found that the total lenght is greater than or equal to maximum length then we will perform the operation.

        int spacesReq;
        int currLen = 0;

        vector<string> temp;
        vector<string> result;

        for(auto &word : words){
            int wordLen = word.size();
            spacesReq = temp.size();
            if(currLen + wordLen + spacesReq > maxWidth){
                string answer = "";
                int spaces = maxWidth - currLen;
                if(temp.size() == 1){
                    answer = temp[0];
                    while(spaces --> 0) answer += " ";
                    result.push_back(answer);
                }
                else{
                    int spaceBetween = spaces / (temp.size() - 1);
                    int extraSpaces = maxWidth - currLen - spaceBetween * (temp.size() - 1);
                    answer = temp[0];
                    string bet = "";
                    while(spaceBetween --> 0) bet += " ";
                    for(int i = 1 ; i < temp.size() ; i++){
                        answer += bet;
                        if(extraSpaces > 0){
                            answer += " ";
                            extraSpaces -= 1;
                        }
                        answer += temp[i];
                    }
                    result.push_back(answer);
                }
                temp.clear();
                currLen = wordLen;
                temp.push_back(word);
            }
            else{
                currLen += wordLen;
                temp.push_back(word);
            }
        }

        if(temp.size() >= 1){
            string answer = temp[0];
            for(int i = 1 ; i < temp.size() ; i++){
                answer += " " + temp[i];
            }
            while(answer.size() < maxWidth) answer += " ";
            result.push_back(answer);
        }

        return result;

    }
};
        """
        adversarial_code = """
        class Solution {
public:
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        int spacesReq;
        int currLen = 0;

        vector<string> temp;
        vector<string> result;

        for(auto &word : words){
            int wordLen = word.size();
            spacesReq = temp.size();
            if(currLen + wordLen + spacesReq > maxWidth){
                string answer = "";
                int spaces = maxWidth - currLen;
                switch(temp.size()) {
                    case 1:
                        answer = temp[0];
                        while(spaces --> 0) answer += " ";
                        result.push_back(answer);
                        break;
                    default:
                        int spaceBetween = spaces / (temp.size() - 1);
                        int extraSpaces = maxWidth - currLen - spaceBetween * (temp.size() - 1);
                        answer = temp[0];
                        string bet = "";
                        while(spaceBetween --> 0) bet += " ";
                        for(int i = 1 ; i < temp.size() ; i++){
                            answer += bet;
                            if(extraSpaces > 0){
                                answer += " ";
                                extraSpaces -= 1;
                            }
                            answer += temp[i];
                        }
                        result.push_back(answer);
                        break;
                }
                temp.clear();
                currLen = wordLen;
                temp.push_back(word);
            }
            else{
                currLen += wordLen;
                temp.push_back(word);
            }
        }

        if(temp.size() >= 1){
            string answer = temp[0];
            for(int i = 1 ; i < temp.size() ; i++){
                answer += " " + temp[i];
            }
            while(answer.size() < maxWidth) answer += " ";
            result.push_back(answer);
        }

        return result;
    }
};
"""
        self.assertFalse(check_rule_19_and_20(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))    
    def test_pass_ruby_19(self):
        original_code = """
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
        adversarial_code = """
        
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
            case
            when findMST(i) > mstw
                c << e.last
            when mstw == findMST(nil, i)
                pc << e.last
            end
        }
    end
end

def find_critical_and_pseudo_critical_edges(n, edges)
    Graph.new(n, edges).solve
end
"""
        self.assertTrue(check_rule_19_and_20(original_code, adversarial_code, 'ruby') and are_comments_equal(original_code, adversarial_code, 'ruby'))        
    def test_pass_csharp_19(self):
        original_code = """
        public class Solution {
    public void SortColors(int[] nums) {
        int r=0,w=0,b=0;
        foreach(int n in nums){
            if(n==0)r++;
            else if(n==1)w++;
            else b++;
        }
        for(int i=0;i0){
                nums[i]=0;
                r--;
            } else if(w>0){
                nums[i]=1;
                w--;
            }
            else
                nums[i]=2;
        }
    }
}
"""
        adversarial_code = """
        public class Solution {
    public void SortColors(int[] nums) {
        int r=0,w=0,b=0;
        foreach(int n in nums){
            switch(n) {
                case 0:
                    r++;
                    break;
                case 1:
                    w++;
                    break;
                default:
                    b++;
                    break;
            }
        }
        for(int i=0;i0){
                nums[i]=0;
                r--;
            } else if(w>0){
                nums[i]=1;
                w--;
            }
            else
                nums[i]=2;
        }
    }
}
"""
        self.assertTrue(check_rule_19_and_20(original_code, adversarial_code, 'csharp') and are_comments_equal(original_code, adversarial_code, 'csharp'))
    def test_pass_cpp_19(self):
        original_code = """
        class Solution {
public:
    vector>>dp;
    int findMaxForm(vector& arr, int m, int n) 
   {
    dp.resize(arr.size()+1,vector>(m+1,vector(n+1,-1))); 
    vector>v;  //pair
    
	for(int i=0;iif(str[j]=='0')
			{
				zero++;
			}
			else if(str[j]=='1')
			{
				one++;
			}
		}
	    v.push_back(make_pair(zero,one));
	}
	int idx=0;
	return fun(arr,v,idx,m,n);        
}
int fun(vector&arr,vector>&v,int idx,int m,int n)
{
	//base 
	if(idx>=arr.size())
	{
		return 0;
	}
	if(dp[idx][m][n]!=-1)
    {
        // cout<<"hello"<=0 and n-v[idx].second >=0)
    {
    	choise1=1+fun(arr,v,idx+1,m-v[idx].first,n-v[idx].second);
	}
   
    //or i cannot take that element
    choise2=0+fun(arr,v,idx+1,m,n);
   
    return dp[idx][m][n] = max(choise1,choise2);
}
};
"""
        adversarial_code = """
        class Solution {
public:
    vector>>dp;
    int findMaxForm(vector& arr, int m, int n) 
   {
    dp.resize(arr.size()+1,vector>(m+1,vector(n+1,-1))); 
    vector>v;  //pair
    
	for(int i=0;iswitch(str[j])
			{
				case '0':
					zero++;
					break;
				case '1':
					one++;
					break;
			}
		}
	    v.push_back(make_pair(zero,one));
	}
	int idx=0;
	return fun(arr,v,idx,m,n);        
}
int fun(vector&arr,vector>&v,int idx,int m,int n)
{
	//base 
	if(idx>=arr.size())
	{
		return 0;
	}
	if(dp[idx][m][n]!=-1)
    {
        // cout<<"hello"<=0 and n-v[idx].second >=0)
    {
    	choise1=1+fun(arr,v,idx+1,m-v[idx].first,n-v[idx].second);
	}
   
    //or i cannot take that element
    choise2=0+fun(arr,v,idx+1,m,n);
   
    return dp[idx][m][n] = max(choise1,choise2);
}
};
"""
        self.assertTrue(check_rule_19_and_20(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_java_19(self):
        original_code = """
        class Solution {

    // taken help as for my code TLE T.C = (n^2);

/*    static boolean check(String s){
        int n = s.length();

        int arr[] = new int[26];

        for(int i=0; i<n; i++){
            int a = s.charAt(i)-97;
            arr[a]++;
        }

        if(arr[0]%2!=0 || arr[4]%2!=0 || arr[8]%2!=0 || arr[14]%2!=0 ||arr[20]%2!=0) return false;
        else return true; 
    }

    static int helper(String str){
        int ans = 0;
        int n = str.length();
        StringBuilder s = new StringBuilder(str);

        for(int k=1; k<=n; k++){
            for(int i=0; i<=n-k; i++){
                String x = s.substring(i,i+k);
                if(check(x)){
                    ans = Math.max(ans,k);
                    break;
                }
            }
        }
        return ans;
    }

    */
    public int findTheLongestSubstring(String s) {

        int[] map = new int[32];
        Arrays.fill(map, -2);
        map[0] = -1;
        int n = s.length(), mask = 0, len = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') mask ^= 1 << (4 -
                    (ch == 'a' ? 0 : ch == 'e' ? 1 : ch == 'i' ? 2 : ch == 'o' ? 3 : 4));
            if (map[mask] == -2) map[mask] = i;
            else len = Math.max(len, i - map[mask]);
        }
        return len;
    }
}
"""
        adversarial_code = """
        class Solution {

    public int findTheLongestSubstring(String s) {

        int[] map = new int[32];
        Arrays.fill(map, -2);
        map[0] = -1;
        int n = s.length(), mask = 0, len = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            switch (ch) {
                case 'a':
                    mask ^= 1 << 4;
                    break;
                case 'e':
                    mask ^= 1 << 3;
                    break;
                case 'i':
                    mask ^= 1 << 2;
                    break;
                case 'o':
                    mask ^= 1 << 1;
                    break;
                case 'u':
                    mask ^= 1 << 0;
                    break;
            }
            if (map[mask] == -2) map[mask] = i;
            else len = Math.max(len, i - map[mask]);
        }
        return len;
    }
}
"""
        self.assertFalse(check_rule_19_and_20(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_pass_java_20(self):
        original_code = """
        class Solution {
    public boolean judgeCircle(String moves) {
        int UpDown = 0;
        int LeftRight = 0;

        for (char c : moves.toCharArray() )
        {
            switch (c){
                case 'U':
                    UpDown++;
                    break;
                case 'D':
                    UpDown--;
                    break;
                case 'L':
                    LeftRight++;
                    break;
                case 'R':
                    LeftRight--;
                    break;
            }
        }



        return (LeftRight == 0 && UpDown == 0); 
    }
}
"""
        adversarial_code = """
        class Solution {
    public boolean judgeCircle(String moves) {
        int UpDown = 0;
        int LeftRight = 0;

        for (char c : moves.toCharArray() )
        {
            if (c == 'U') {
                UpDown++;
            } else if (c == 'D') {
                UpDown--;
            } else if (c == 'L') {
                LeftRight++;
            } else if (c == 'R') {
                LeftRight--;
            }
        }

        return (LeftRight == 0 && UpDown == 0); 
    }
}
"""
        self.assertTrue(check_rule_19_and_20(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
    
    def test_fail_cpp_20(self):
        """
        Original code does not contain any switch statement.
        """
        original_code = """
        class Solution {
public:
    bool buddyStrings(string s, string goal) {
        int i,j,k,c=0,a=0;
        unordered_map<char,int>map;
        for(auto x:s)
        map[x]++;

        if(map.size()<s.size())
        a=1;

        for(auto x:goal){                    //comparing that both strings have same number of alphabets
            if(map.find(x)==map.end())        //if different alphabets 
            return 0;                            //return 0;
            if(map[x]==1)
            map.erase(x);                       //else erase from map
            else
            map[x]--;
        }

        if(map.size()>0)                        //if map not empty return 0
        return 0;

        for(i=0;i<s.size();i++){                  //comparing alphabets at all indexes
            if(s[i]!=goal[i])
            c++;
        }

    if(c==2)                                     //if c==2 only 2 alphabets are displaced return 1;
    return 1;
    if(a==1 and c==0)                            //if any 2 characters are repeating then if c==0 return 1;
    return 1;                               //return 0
    
    return 0;
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    bool buddyStrings(string s, string goal) {
        int i,j,k,c=0,a=0;
        unordered_map<char,int>map;
        for(auto x:s)
        map[x]++;

        if(map.size()<s.size())
        a=1;

        for(auto x:goal){                    //comparing that both strings have same number of alphabets
            if(map.find(x)==map.end())        //if different alphabets 
            return 0;                            //return 0;
            if(map[x]==1)
            map.erase(x);                       //else erase from map
            else
            map[x]--;
        }

        if(map.size()>0)                        //if map not empty return 0
        return 0;

        for(i=0;i<s.size();i++){                  //comparing alphabets at all indexes
            if(s[i]!=goal[i])
            c++;
        }

        if(c==2)                                     //if c==2 only 2 alphabets are displaced return 1;
        return 1;
        if(a==1 and c==0)                            //if any 2 characters are repeating then if c==0 return 1;
        return 1;                               //return 0
        
        return 0;
    }
};
"""
        self.assertFalse(check_rule_19_and_20(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    def test_fail_java_20(self):
        """
        Transformations are valid. But extra comments are added in adversarial code.
        """
        original_code = """
        class Solution {
    public int minOperations(String[] logs) {
        int count = 0;
        for (String move : logs) {
            switch (move) {
                case "../": {
                    if (count > 0)
                        count--;
                    break;
                }
                case "./": {
                    break;
                }
                default: {
                    count++;
                }
            }
        }
        return count;
    }
}
"""
        adversarial_code = """
        
class Solution {
    public int minOperations(String[] logs) {
        int count = 0;
        for (String move : logs) {
            if (move.equals("../")) {
                if (count > 0)
                    count--;
            } else if (move.equals("./")) {
                // Do nothing
            } else {
                count++;
            }
        }
        return count;
    }
}
"""
        self.assertFalse(check_rule_19_and_20(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()