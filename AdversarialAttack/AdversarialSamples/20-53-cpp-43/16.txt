class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maxi=INT_MIN;
        int temp=0;
        for(int i=0;i<nums.size();i++){
            temp=temp+nums[i];

            maxi=max(maxi,temp);
            if(temp<0){
                temp=0;
            }
            
        }
        return maxi;
    }
};