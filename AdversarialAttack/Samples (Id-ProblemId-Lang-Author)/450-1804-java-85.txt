class Solution {

    // taken some help


    // First i get the index of  first "0", if it is not present then we will return the string itself
    // otherwise we will count the number of "0" after that index;
    // now we will shift that "0" by count number of times and fill all the place with "1"
    // this is because we can always make the string that contains only one "0";
    
    public String maximumBinaryString(String s){

        int n = s.length();

        int a = s.indexOf("0");
        if(a==-1) return s;

        int zero = 0;

        for(int i=a+1; i<n; i++){
            if(s.charAt(i)=='0') zero++;
        } 

        StringBuilder ans = new StringBuilder();
        ans.append("1".repeat(n));

        int x = a+zero;

        ans.replace(x,x+1,"0");
        return ans.toString();
    }
}