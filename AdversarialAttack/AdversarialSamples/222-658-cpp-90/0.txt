class Solution {
public:
    vector<int> findClosestElements(vector<int>& arr, int k, int x) {
        int n = arr.size();

        priority_queue<pair<int,int>> maxHeap;

        for(int i=0;i<n;i++) {
            int diff = abs(arr[i]-x);

            maxHeap.push({diff,arr[i]});

            if(maxHeap.size() > k) {
                maxHeap.pop();
            }
        }

        vector<int> result;

        while(!maxHeap.empty()) {
            auto p = maxHeap.top();
            result.push_back(p.second);
            maxHeap.pop();
        }

        sort(result.begin(),result.end());

        return result;
    }
};