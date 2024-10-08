class Solution {
    public String complexNumberMultiply(String num1, String num2) {
        // extract real and img part
        int real1= Integer.parseInt(num1.substring(0,num1.indexOf('+')));
        int img1= Integer.parseInt(num1.substring(num1.indexOf('+')+1, num1.length()-1));
        //similarly extract for second com  number
        int real2= Integer.parseInt(num2.substring(0,num2.indexOf('+')));
        int img2= Integer.parseInt(num2.substring(num2.indexOf('+')+1, num2.length()-1));

        int real= real1*real2-img1*img2;
        int img= real1*img2+real2*img1;

        String res= real+"+"+img+"i";

        return res; 
    }
}