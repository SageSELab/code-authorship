import unittest
from adversarial_sample_verification import *
class TestRules(unittest.TestCase):
    def test_pass_cpp(self):
        original_code = """
        class Solution {
public:
    string reverseWords(string s) {
        // Trim the input string to remove leading and trailing spaces
        int i = 0, j = s.size() - 1;
        while (i <= j && s[i] == ' ') i++;   // Find the first non-space character
        while (j >= i && s[j] == ' ') j--;   // Find the last non-space character
        s = s.substr(i, j - i + 1);          // Extract the trimmed substring

        // Split the trimmed string into words based on spaces
        vector words;                // Create a vector to store words
        stringstream ss(s);                  // Create a stringstream with the trimmed string
        string word;
        while (ss >> word) {                 // Tokenize the string into words
            words.push_back(word);           // Store each word in the vector
        }

        // Initialize the output string
        string out = "";

        // Iterate through the words in reverse order
        for (int i = words.size() - 1; i > 0; i--) {
            // Append the current word and a space to the output
            out += words[i] + " ";
        }

        // Append the first word to the output (without trailing space)
        return out + words[0];               // Concatenate the reversed words
    }
};
"""
        adversarial_code = """
        class Solution {
public:
    string reverseWords(string s) {
        // Trim the input string to remove leading and trailing spaces
        int i = 0, j = s.size() - 1;
        while (i <= j && s[i] == ' ') i++;   // Find the first non-space character
        while (j >= i && s[j] == ' ') j--;   // Find the last non-space character
        s = s.substr(i, j - i + 1);          // Extract the trimmed substring

        // Split the trimmed string into words based on spaces
        stringstream ss(s);                  // Create a stringstream with the trimmed string
        vector words;                // Create a vector to store words
        string word;
        while (ss >> word) {                 // Tokenize the string into words
            words.push_back(word);           // Store each word in the vector
        }

        // Initialize the output string
        string out = "";

        // Iterate through the words in reverse order
        for (int i = words.size() - 1; i > 0; i--) {
            // Append the current word and a space to the output
            out += words[i] + " ";
        }

        // Append the first word to the output (without trailing space)
        return out + words[0];               // Concatenate the reversed words
    }
};
"""
        self.assertTrue(check_rule_5(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
        
    def test_fail_cpp(self):
        original_code = """
        class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int reader=0, writer=0;
        // reader pointer will move forward in every iteration, writer will stop if nums[writer]==val, and will be overwritten by nums[reader]
        while(reader<nums.size()){
            if(nums[reader]==val){
                reader++;
            }
            else{
                nums[writer++] = nums[reader++];

            }
        }
        return writer;
    }
};
"""
        adversarial_code = """
        
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int reader=0, writer=0;
        // reader pointer will move forward in every iteration, writer will stop if nums[writer]==val, and will be overwritten by nums[reader]
        while(reader<nums.size()){
            if(nums[reader]==val){
                reader++;
            }
            else{
                nums[writer++] = nums[reader++];
            }
        }
        return writer;
    }
};
"""
        self.assertFalse(check_rule_5(original_code, adversarial_code, 'cpp') and are_comments_equal(original_code, adversarial_code, 'cpp'))
    
    def test_pass_csharp(self):
        original_code = """
        public class Solution {
    public int[][] UpdateMatrix(int[][] mat) {
        int m = mat.Length;
        int n = mat[0].Length;
        
        int[][] result = new int[m][];
        for (int i = 0; i < m; i++) {
            result[i] = new int[n];
            for (int j = 0; j < n; j++) {
                result[i][j] = int.MaxValue - 1; // Initialize to a large value
                
                if (mat[i][j] == 0) {
                    result[i][j] = 0; // If it's 0, distance is 0
                }
                else {
                    // Check left and top neighbors
                    if (i > 0) result[i][j] = Math.Min(result[i][j], result[i - 1][j] + 1);
                    if (j > 0) result[i][j] = Math.Min(result[i][j], result[i][j - 1] + 1);
                }
            }
        }
        
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                // Check right and bottom neighbors
                if (i < m - 1) result[i][j] = Math.Min(result[i][j], result[i + 1][j] + 1);
                if (j < n - 1) result[i][j] = Math.Min(result[i][j], result[i][j + 1] + 1);
            }
        }
        
        return result;
    }
}
"""
        adversarial_code = """
        public class Solution {
    public int[][] UpdateMatrix(int[][] mat) {
        int m = mat.Length;
        int n = mat[0].Length;
        
        int[][] result = new int[m][];
        for (int i = 0; i < m; i++) {
            result[i] = new int[n];
            for (int j = 0; j < n; j++) {
                result[i][j] = int.MaxValue - 1; // Initialize to a large value
                
                if (mat[i][j] == 0) {
                    result[i][j] = 0; // If it's 0, distance is 0
                }
                else {
                    // Check left and top neighbors
                    if (j > 0) result[i][j] = Math.Min(result[i][j], result[i][j - 1] + 1);
                    if (i > 0) result[i][j] = Math.Min(result[i][j], result[i - 1][j] + 1);
                }
            }
        }
        
        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                // Check right and bottom neighbors
                if (j < n - 1) result[i][j] = Math.Min(result[i][j], result[i][j + 1] + 1);
                if (i < m - 1) result[i][j] = Math.Min(result[i][j], result[i + 1][j] + 1);
            }
        }
        
        return result;
    }
}
"""
        self.assertTrue(check_rule_5(original_code, adversarial_code, 'csharp') and are_comments_equal(original_code, adversarial_code, 'csharp'))

    
if __name__ == '__main__':
    unittest.main()