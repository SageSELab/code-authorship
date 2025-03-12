import pandas as pd 
# Load datasets
train = pd.read_csv('./LeetCode/data/fold_0_train.csv')
test = pd.read_csv('./LeetCode/data/fold_0_test.csv')

# Combine datasets
dataset_df = pd.concat([train, test], axis=0)

dataset_df['language'].value_counts()/len(dataset_df)

language_wise_results = []

# Load datasets
train = pd.read_csv('./LeetCode/data/fold_0_train.csv')
test = pd.read_csv('./LeetCode/data/fold_0_test.csv')

# Combine datasets
dataset_df = pd.concat([train, test], axis=0)

# Count total samples per language
total_counts = dataset_df['language'].value_counts()

# Load correctly attributed samples
leetcode_all_correct_df = pd.read_csv('./all_models_correct_samples.csv')

# Compute length of code samples
dataset_df['length'] = dataset_df['code'].apply(lambda x: len(x))
leetcode_all_correct_df['length'] = leetcode_all_correct_df['code'].apply(lambda x: len(x))

# List of models
models = ['CodeBERT', 'ContraBERT_C', 'ContraBERT_G' , 'GraphCodeBERT', 'UniXcoder', 'DeepSeek', 'CodeLlama']


# Generate plots for each model
for i, model in enumerate(models):
    # Filter correctly attributed samples for the specific model
    model_correct_df = leetcode_all_correct_df[leetcode_all_correct_df[model]]

    # Count correctly attributed samples per language
    correct_counts = model_correct_df['language'].value_counts()

    language_result = (correct_counts/total_counts).sort_index().to_dict()
    
    
    language_result['average'] = sum(language_result.values())/len(language_result)
    language_result['model'] = model
    language_wise_results.append(language_result)



language_results_df = pd.DataFrame(language_wise_results)

language_results_df.to_csv('./leetcode-language_wise_results.csv', index=False)