class Solution {
    public List<String> fizzBuzz(int n) {
        List<String> res = new ArrayList<>();
        int i = 1, fizz = 0, buzz = 0;
        while (i <= n){
            fizz++; buzz++;
            if (fizz == 3 && buzz == 5) {
                res.add("FizzBuzz");
                fizz = buzz = 0;
            } else if (fizz == 3) {
                res.add("Fizz");
                fizz = 0;
            } else if (buzz == 5) {
                res.add("Buzz");
                buzz = 0;
            } else {
                res.add(String.valueOf(i));
            }
            i++;
        }

        return res;
    }
}