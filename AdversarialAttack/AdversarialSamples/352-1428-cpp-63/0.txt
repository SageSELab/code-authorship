class Solution {
public:
    bool canReach(vector<int>& A, int cur) {
        return cur >= 0 && cur < size(A) && A[cur] >= 0 && (!(A[cur] *= -1) || canReach(A, cur + A[cur]) || canReach(A, cur - A[cur]));
    }
};