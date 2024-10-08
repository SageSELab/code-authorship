class Solution:
    def canReorderDoubled(self, arr):
        cnt = Counter(arr)
        for num in sorted(arr, key = lambda x: abs(x)):
            if cnt[num] == 0: continue
            if cnt[2*num] == 0: return False
            cnt[num] -= 1
            cnt[2*num] -= 1
        
        return True