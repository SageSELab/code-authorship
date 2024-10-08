class Solution {
public:
    vector<int> constructArray(int n, int k) {
        vector<int> res;
        int i = 1, j = n;
        
        while (i <= j) {
            if (k > 1)
                k-- % 2 ? res.push_back(i++) : res.push_back(j--);
            
            else 
                res.push_back(i++);
        }
        return res;
    }
};