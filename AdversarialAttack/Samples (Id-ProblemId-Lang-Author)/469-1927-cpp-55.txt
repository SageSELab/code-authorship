class Solution {
public:
    int maxAscendingSum(vector<int>& nums) {
        int i, j, k, sum=0, max=0;
        for(i=0 ; i<nums.size() ; i++)
        {
            sum=nums[i];
            k = i;
            for(j=i+1 ; j<nums.size() ; j++)
            {
                if(nums[j]>nums[k])
                {
                    sum += nums[j];
                    k = j;
                }
                else
                {
                    break;
                }
            }
            if(sum>max)
            {
                max = sum;
            }
        }
        return max;
    }
};