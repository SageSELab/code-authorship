class Solution {
public:
    int longestValidParentheses(string s) {
        int n=s.size();
        if (n<2) return 0;
        stack<int> st;
        vector<int> dp(n, 0);
       
        int ans=0;
        for(int i=0; i<n; i++){
            if (s[i]=='(') {
                st.push(i);
            }
            else{ //s[i]=')'
                if (!st.empty()){
                    int x=st.top();
                    dp[i]=i-x+1;//substring s[x:i+1] is valid
                    if (x>=1) dp[i]+=dp[x-1];//concatenate with substring
                //    cout<<i<<"->"<<x<<":"<<dp[i]<<endl;
                    st.pop();
                }
            }
            ans=max(ans, dp[i]);
        }
        return ans;
    }
};