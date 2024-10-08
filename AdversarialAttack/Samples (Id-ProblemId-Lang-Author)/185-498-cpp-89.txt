class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& mat) {
        // Intution
        // The idea in here is really very simple. We know that by maintains two straps details i.e., First row + Last column and First column + Last row we can get the required elements but only the starting location changes in both the cases.
        vector<int> answer;

        vector<pair<int, int>> strap1;
        vector<pair<int, int>> strap2;

        int m = mat.size();
        int n = mat[0].size();

        for(int i = 0 ; i < n ; i++) strap1.push_back({0, i});
        for(int i = 1 ; i < m ; i++) strap1.push_back({i, n - 1});

        for(int i = 0 ; i < m ; i++) strap2.push_back({i, 0});
        for(int i = 1 ; i < n ; i++) strap2.push_back({m - 1, i});

        bool toggler = false;

        int total = strap1.size();

        int ind = 0;

        while(total --> 0){
            if(!toggler){
                int r = strap2[ind].first;
                int c = strap2[ind].second;
                while(r >= 0 and c < n){
                    answer.push_back(mat[r][c]);
                    r -= 1;
                    c += 1;
                }
            }
            else{
                int r = strap1[ind].first;
                int c = strap1[ind].second;
                while(c >= 0 and r < m){
                    answer.push_back(mat[r][c]);
                    c -= 1;
                    r += 1;
                }
            }
            if(toggler) toggler = false;
            else toggler = true;
            ind += 1;
        }

        return answer;

    }
};