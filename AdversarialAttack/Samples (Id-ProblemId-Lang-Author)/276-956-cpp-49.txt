class Solution {
public:
    int numMusicPlaylists(int n, int goal, int k) {
        const int mod=1e9+7;
        vector<int> dp(n+1, 0), prev(n+1, 0);
        prev[0]=1;// dp[0][0]=1
        for (int i=1; i<=goal; i++){
            for(int j=1; j<=n; j++){
                long long ans=(long long)prev[j-1]*(n-j+1)%mod;//new song
                if (j>k)
                    ans+=(long long)prev[j]*(j-k)%mod;//old song
                dp[j]=ans%mod;
            }
            prev=dp;
        }
        return dp[n];
    }
};