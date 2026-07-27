import json
import glob
import os
import pandas as pd
import re


df = pd.read_csv('./all_models_correct_samples.csv')

results = []

for index, row in df.iterrows():
    code = row['code']
    location = row['location']
    
    for rule in range(28):
        if not os.path.exists(f'./Adversarial-Samples-GPT4/{location}-{rule}.txt'):
            continue
        with open(f'./Adversarial-Samples-GPT4/{location}-{rule}.txt', 'r') as f:
            adversarial_code = f.read()
            if "NA" in adversarial_code or code in adversarial_code:
                results.append({"location": location, 'rule': rule, 'is_applied': False})
            else:
                results.append({"location": location, 'rule': rule, 'is_applied': True})


results_df = pd.DataFrame(results)

sorted(results_df[results_df['is_applied'] == True]['rule'].value_counts().to_dict().keys())


results_df = results_df[results_df['is_applied'] == True]

all_models_correct_samples = pd.read_csv('./all_models_correct_samples.csv')


def get_problem(location):
   filtered_df = all_models_correct_samples[all_models_correct_samples['location'] == location]
   if len(filtered_df) != 1:
       print(f"Error: {location} not found or multiple entries found.")
       raise Exception(f"Error: {location} not found or multiple entries found.")
   
   else:
        return filtered_df['problem_url'].values[0], int(filtered_df['problem_id'].values[0]), filtered_df['language'].values[0]


results_df['problem_url'], results_df['problem_id'], results_df['language'] = zip(*results_df['location'].apply(get_problem))


all_models_correct_samples[all_models_correct_samples['problem_id'].isna()]['problem_url'].values


results_df.to_csv('./adversarial-samples-GPT4.csv', index=False)


file_path = 'Submissions/*.json'
files = glob.glob(file_path)


all_submissions = []


for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        all_submissions.append(data)


df = pd.DataFrame(all_submissions)


all_models_correct_samples_df = pd.read_csv("all_models_correct_samples.csv")


adversarial_samples_GPT4_df = pd.read_csv("adversarial-samples-GPT4.csv")


def get_leetcode_submission_status(row):
    location = row['location']
    rule_id = row['rule']
    
    if not os.path.exists(f"./Submissions/{location}-{rule_id}.json"):
        return "NA"
    with open(f"./Submissions/{location}-{rule_id}.json", 'r') as f:
        data = json.load(f)
        if 'status_msg' in data:
            return data['status_msg']
        else:
            return "NA"
    


adversarial_samples_GPT4_df['submission_status'] = adversarial_samples_GPT4_df.apply(get_leetcode_submission_status, axis=1)


def get_models(location):
    filter_df = all_models_correct_samples_df[all_models_correct_samples_df['location'] == location]
    if len(filter_df) > 1:
        raise ValueError(f"Multiple models found for location {location}")
    return filter_df['PbNN'].values[0], filter_df['CodeBERT'].values[0],filter_df['GraphCodeBERT'].values[0], filter_df['ContraBERT_C'].values[0],filter_df['ContraBERT_G'].values[0], filter_df['UniXcoder'].values[0], filter_df['DeepSeek'].values[0], filter_df['CodeLlama'].values[0]


adversarial_samples_GPT4_df['PbNN'], adversarial_samples_GPT4_df['CodeBERT'], adversarial_samples_GPT4_df['GraphCodeBERT'], adversarial_samples_GPT4_df['ContraBERT_C'], adversarial_samples_GPT4_df['ContraBERT_G'], adversarial_samples_GPT4_df['UniXcoder'], adversarial_samples_GPT4_df['DeepSeek'], adversarial_samples_GPT4_df['CodeLlama'] = zip(*adversarial_samples_GPT4_df['location'].apply(get_models))


adversarial_samples_GPT4_df = adversarial_samples_GPT4_df[adversarial_samples_GPT4_df["submission_status"] == "Accepted"]


def remove_backticks_with_regex(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    if '```cpp' in content:
        regex = r'^```cpp|```$'
    elif '```python' in content:
        regex = r'^```python|```$'
    elif '```java' in content:
        regex = r'^```java|```$'
    elif '```javascript' in content:
        regex = r'^```javascript|```$'
    elif '```c' in content:
        regex = r'^```c|```$'
    elif '```csharp' in content:
        regex = r'^```csharp|```$'
    elif '```ruby' in content:
        regex = r'^```ruby|```$'
    elif '```' in content:
        regex = r'^```|```$'
    else:
        return 'NA'
    
    # Regex to remove leading and trailing lines starting with ```
    cleaned_content = re.sub(regex, '', content, flags=re.MULTILINE)
    
    return cleaned_content


def get_adeversarial_code(row):
    location = row['location']
    rule_id = row['rule']
    
    code = remove_backticks_with_regex(f"./Adversarial-Samples-GPT4/{location}-{rule_id}.txt")
    return code


adversarial_samples_GPT4_df['adversarial_code'] = adversarial_samples_GPT4_df.apply(get_adeversarial_code, axis=1)


adversarial_samples_GPT4_df.to_csv("adversarial_samples_GPT4_accepted.csv", index=False)





