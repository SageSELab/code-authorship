class Solution {
public:
    
    // sort the engineeres on the basis of efficiency in decreasing order
    
    static bool compare(vector<int>& a, vector<int>& b)
    {
        return a[0] > b[0];
    }
    
    int maxPerformance(int n, vector<int>& speed, vector<int>& efficiency, int k) {
        
        long long mod = 1e9 + 7;
        
        vector<vector<int>> engineers(n);
        
        for(int i = 0; i < n; i++)
        {
            engineers[i] = {efficiency[i], speed[i]};
        }
        
        // sort the engineeres on the basis of efficiency in decreasing order
        
        sort(engineers.begin(), engineers.end(), compare);
        
        // declare a min. heap, which will store the speeds
        
        priority_queue<long long, vector<long long>, greater<long long>> pq;
        
        long long total_speed = 0;
        
        long long max_performance = INT_MIN;
        
        for(int i = 0; i < n; i++)
        {
            if(i < k)
            {
                long long curr_speed = engineers[i][1];
                
                total_speed += curr_speed;
                
                long long min_efficiency = engineers[i][0];
                
                long long curr_performance = total_speed * min_efficiency;
                
                max_performance = max(max_performance, curr_performance);
                
                pq.push(curr_speed);
            }
            else
            {
                long long curr_speed = engineers[i][1];
                
                if(curr_speed > pq.top())
                {
                    total_speed -= pq.top();
                    
                    total_speed += curr_speed;
                    
                    pq.pop();
                    
                    pq.push(curr_speed);
                    
                    long long min_efficiency = engineers[i][0];
                    
                    long long curr_performance = total_speed * min_efficiency;
                    
                    max_performance = max(max_performance, curr_performance);
                }
            }
        }
        
        return (max_performance % mod);
    }
};