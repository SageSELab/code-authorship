class Solution {
public:
    bool canReach(vector<int>& A, int cur) {
        queue<int> q;
        q.push(cur);
        while(size(q)) {
            cur = q.front(); q.pop();
            if(A[cur] == 0) return true;                        // target reached
            if(A[cur] < 0)  continue;                           // already visited - stop further exploration of this path
            if(cur + A[cur] < size(A)) q.push(cur + A[cur]);    // try forward jump
            if(cur - A[cur] >= 0)      q.push(cur - A[cur]);    // try backward jump
            A[cur] *= -1;                                       // mark current index as visited by negating
        }
        return false;             // explored all array without reaching target
    }
};