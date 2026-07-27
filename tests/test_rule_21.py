import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    
    def test_fail_python(self):
        """
        No transformation is done.
        """
        original_code = """
       class Solution(object):
    def lemonadeChange(self, bills):
        fives, tens = 0, 0
        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False
        return True
        """
        adversarial_code = """
        class Solution(object):
    def lemonadeChange(self, bills):
        fives, tens = 0, 0
        for bill in bills:
            if bill == 5:
                fives += 1
            elif bill == 10:
                if fives == 0:
                    return False
                fives -= 1
                tens += 1
            else:
                if tens > 0 and fives > 0:
                    tens -= 1
                    fives -= 1
                elif fives >= 3:
                    fives -= 3
                else:
                    return False
        return True
        """
        self.assertFalse(check_rule_21(original_code, adversarial_code, 'python'))
    
    def test_fail_java(self):
        """
        Transformations are done correctly. But comments are not equal.
        """
        original_code = """
        class Solution {
    public double myPow(double x, int n) {
        
        // Base condition: If n is 0, x^0 is 1
        if (n == 0) {
            return 1;
        }

        // Convert n to a long integer to handle the edge case with Integer.MIN_VALUE
        long N = n;

        // If n is negative, take the reciprocal of x and make N positive
        if (N < 0) {
            N = -N;
            x = 1 / x;
        }

        // If N is even, recursively compute the square of x^(N/2)
        if (N % 2 == 0) {
            return myPow(x * x, (int) (N / 2));
        } 
    
        // If N is odd, recursively compute x^(N-1) and multiply it by x
        else {
            return x * myPow(x, (int) (N - 1));
        }
    }
}
"""
        adversarial_code = """  
        
class Solution {
    public double myPow(double x, int n) {
        
        // Base condition: If n is 0, x^0 is 1
        if (n == 0) {
            return 1;
        }

        // Convert n to a long integer to handle the edge case with Integer.MIN_VALUE
        long N = n;

        // If n is negative, take the reciprocal of x and make N positive
        if (N < 0) {
            N = -N;
            x = 1 / x;
        }

        // Use ternary operator for even/odd check
        return (N % 2 == 0) ? myPow(x * x, (int) (N / 2)) : x * myPow(x, (int) (N - 1));
    }
}
"""
        self.assertFalse(check_rule_21(original_code, adversarial_code, 'java') and are_comments_equal(original_code, adversarial_code, 'java'))    

    def test_pass_cpp(self):
        """
        Transformations are done correctly.
        """
        original_code = """
        class Solution {
public:
    int largestSubmatrix(vector>& matrix) {
        int m = matrix.size(); // Number of rows in the matrix
        int n = matrix[0].size(); // Number of columns in the matrix
        int ans = 0; // Initialize the maximum area of the largest submatrix
        
        // Traverse through each row in the matrix
        for (int row = 0; row < m; row++) {
            // For each non-zero element in the matrix (except the first row),
            // accumulate its value with the element directly above it
            for (int col = 0; col < n; col++) {
                if (matrix[row][col] != 0 && row > 0) {
                    matrix[row][col] += matrix[row - 1][col];
                }
            }
            
            // Create a copy of the current row to work with
            vector currRow = matrix[row];
            
            // Sort the elements in the current row in descending order
            sort(currRow.begin(), currRow.end(), greater());
            
            // Calculate the maximum area of the largest submatrix with consecutive ones
            for (int i = 0; i < n; i++) {
                ans = max(ans, currRow[i] * (i + 1));
            }
        }
        
        return ans; // Return the maximum area of the largest submatrix
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    int largestSubmatrix(vector>& matrix) {
        int m = matrix.size(); // Number of rows in the matrix
        int n = matrix[0].size(); // Number of columns in the matrix
        int ans = 0; // Initialize the maximum area of the largest submatrix
        
        // Traverse through each row in the matrix
        for (int row = 0; row < m; row++) {
            // For each non-zero element in the matrix (except the first row),
            // accumulate its value with the element directly above it
            for (int col = 0; col < n; col++) {
                matrix[row][col] = (matrix[row][col] != 0 && row > 0) ? matrix[row][col] + matrix[row - 1][col] : matrix[row][col];
            }
            
            // Create a copy of the current row to work with
            vector currRow = matrix[row];
            
            // Sort the elements in the current row in descending order
            sort(currRow.begin(), currRow.end(), greater());
            
            // Calculate the maximum area of the largest submatrix with consecutive ones
            for (int i = 0; i < n; i++) {
                ans = max(ans, currRow[i] * (i + 1));
            }
        }
        
        return ans; // Return the maximum area of the largest submatrix
    }
};
"""
        self.assertTrue(check_rule_21(original_code, adversarial_code, 'cpp'))
    
    def test_pass_java(self):
        """
        Transformations are done correctly.
        """
        original_code = """
        class Solution {
    static class Triple{
        int id;
        int rate;

        Triple(int id, int rate){
            this.id = id;
            this.rate = rate;
        }
    }

    

    
    public List<Integer> filterRestaurants(int[][] rest, int vegan, int maxP, int maxD) {

        ArrayList<Triple> arr = new ArrayList<>();

        int n = rest.length;

        if(vegan==1){
            for(int i=0; i<n; i++){
                if(rest[i][2]==1 && rest[i][3]<=maxP && rest[i][4]<=maxD){
                    arr.add(new Triple(rest[i][0],rest[i][1]));
                }
            }
        }else{
            for(int i=0; i<n; i++){
                if(rest[i][3]<=maxP && rest[i][4]<=maxD){
                    arr.add(new Triple(rest[i][0],rest[i][1]));
                }
            }
        }

        Collections.sort(arr,(a,b)->b.rate==a.rate ? b.id-a.id : b.rate-a.rate);

        List<Integer> ans = new ArrayList<>();

        for(int i=0; i<arr.size(); i++){
            ans.add(arr.get(i).id);
        }

        return ans;
    }
}
"""
        adversarial_code = """
        class Solution {
    static class Triple{
        int id;
        int rate;

        Triple(int id, int rate){
            this.id = id;
            this.rate = rate;
        }
    }

    public List<Integer> filterRestaurants(int[][] rest, int vegan, int maxP, int maxD) {

        ArrayList<Triple> arr = new ArrayList<>();

        int n = rest.length;

        for(int i=0; i<n; i++){
            if((vegan == 1 ? rest[i][2] == 1 : true) && rest[i][3] <= maxP && rest[i][4] <= maxD){
                arr.add(new Triple(rest[i][0], rest[i][1]));
            }
        }

        Collections.sort(arr,(a,b)->b.rate==a.rate ? b.id-a.id : b.rate-a.rate);

        List<Integer> ans = new ArrayList<>();

        for(int i=0; i<arr.size(); i++){
            ans.add(arr.get(i).id);
        }

        return ans;
    }
}
"""
        self.assertTrue(check_rule_21(original_code, adversarial_code, 'java'))
if __name__ == '__main__':
    unittest.main()