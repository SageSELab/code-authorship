# Install python dependencies
pip install tree-sitter
pip install pandas

# Clone tree-sitter grammars
git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-ruby.git
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-c.git
git clone https://github.com/tree-sitter/tree-sitter-python.git
git clone https://github.com/tree-sitter/tree-sitter-c-sharp.git
git clone https://github.com/tree-sitter/tree-sitter-javascript.git

# Generate tree-sitter grammars
npm install tree-sitter-cli
npx

cd tree-sitter-java
tree-sitter generate
gcc -shared -o tree-sitter-java.so -fPIC src/parser.c

cd tree-sitter-c
tree-sitter generate
gcc -shared -o tree-sitter-c.so -fPIC src/parser.c

cd ../tree-sitter-ruby
gcc -shared -o tree-sitter-ruby.so -fPIC src/parser.c src/scanner.c

cd ../tree-sitter-cpp
gcc -shared -o tree-sitter-cpp.so -fPIC src/parser.c src/scanner.c

cd ../tree-sitter-python
gcc -shared -o tree-sitter-python.so -fPIC src/parser.c src/scanner.c

cd ../tree-sitter-c-sharp
gcc -shared -o tree-sitter-c-sharp.so -fPIC src/parser.c src/scanner.c

cd ../tree-sitter-javascript
gcc -shared -o tree-sitter-javascript.so -fPIC src/parser.c src/scanner.c

cd ..

# Generate path contexts for gcj-cpp dataset

for i in {0..7}
do
  python generate_path_contexts_cpp.py --input_csv=./gcj-cpp/data/fold_${i}_train.csv --output_json=./gcj-cpp/data/fold_${i}_train.json
  python generate_path_contexts_cpp.py --input_csv=./gcj-cpp/data/fold_${i}_test.csv --output_json=./gcj-cpp/data/fold_${i}_test.json
done

# Generate path contexts for gcj-python dataset

for i in {0..9}
do
  python generate_path_contexts_python.py --input_csv=./gcj-python/data/fold_${i}_train.csv --output_json=./gcj-python/data/fold_${i}_train.json
  python generate_path_contexts_python.py --input_csv=./gcj-python/data/fold_${i}_test.csv --output_json=./gcj-python/data/fold_${i}_test.json
done

# Generate path contexts for LeetCode dataset

for i in {0..9}
do
  python generate_path_contexts_leetcode.py --input_csv=./LeetCode/data/fold_${i}_train.csv --output_json=./leetcode/data/fold_${i}_train.json
  python generate_path_contexts_leetcode.py --input_csv=./LeetCode/data/fold_${i}_test.csv --output_json=./leetcode/data/fold_${i}_test.json
done