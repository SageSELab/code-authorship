class Solution {
public:
    int change(int amt, vector<int>& coins) {
        int sz = coins.size(); 
        vector<int> combCnt(amt+1, 0);
        combCnt[0] = 1;
        for(int cIndx = 0; cIndx < sz; cIndx++){
          for(int curAmt = coins[cIndx]; curAmt<=amt; curAmt++){
             int contri = curAmt - coins[cIndx];
                    combCnt[curAmt] += combCnt[contri];
          }
        }
        return combCnt[amt];
    }
};