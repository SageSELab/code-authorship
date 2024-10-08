class Solution:
    def suggestedProducts(self, P, W):
        P.sort()
        beg, end, ans = 0, len(P) - 1, []

        for i, c in enumerate(W):
            while beg <= end and (len(P[beg]) <= i or P[beg][i] != c):
                beg += 1
                
            while beg <= end and (len(P[end]) <= i or P[end][i] != c):
                end -= 1
                
            ans.append(P[beg:min(end+1, beg+3)])

        return ans