class Solution {
    public int findLongestChain(int[][] pairs) {
        Arrays.sort(pairs, (a,b)-> a[1]-b[1]);
        int len=0, prev=-1001;
        for(int[] pair: pairs) {
            if(prev<pair[0]) {
                len++;
                prev=pair[1];
            }
        }
        return len;
    }
}