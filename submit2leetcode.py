import requests
import time
import json
import pandas as pd
import argparse
import os
import re

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

os.makedirs("Submissions", exist_ok=True)
os.makedirs("Submissions-Error", exist_ok=True)
os.makedirs("Picked", exist_ok=True)

parser = argparse.ArgumentParser( description='Submit code to LeetCode')
parser.add_argument('--csrftoken', type=str, help='csrftoken')

parser.add_argument('--LEETCODE_SESSION', type=str, help='LEETCODE_SESSION')

args = parser.parse_args()

df = pd.read_csv("./leetcode-all-models-corrects-intersection.csv")


cookies = {
    'LEETCODE_SESSION': args.LEETCODE_SESSION,
    'csrftoken': args.csrftoken,
}

for index, row in df.iterrows():
    start_time = time.time()
    id = row["Id"]
    problem_url = row["problem_url"]
    problem_id = row["problem_id"]
    language = row["language"]
    
    for i in range(28):
        if os.path.exists(f'./Submissions/{id}-{i}.json'):
                continue
            
        code = remove_backticks_with_regex(f'./Adversarial-Samples-GPT4/{id}-{i}.txt')
            
        if 'NA' in code:
                continue
        try:
            url = f"{problem_url}/submit/"
            
            # Submit code to LeetCode

            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Sec-Fetch-Site": "same-origin",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Sec-Fetch-Mode": "cors",
                "Host": "leetcode.com",
                "Origin": "https://leetcode.com",
                "Content-Length": "577",
                "Referer": f"{problem_url}/",
                "Connection": "keep-alive",
                "x-csrftoken": cookies['csrftoken'],
                "Sec-Fetch-Dest": "empty"
            }

            data = {
                "lang": language,
                "question_id": problem_id,
                "typed_code": code
            }
            
            print("submitting code")

            submit_response = requests.post(url, headers=headers, cookies=cookies,json=data)
            
            if submit_response.status_code != 200:
                raise Exception(f"Error submitting code for {id}-{i}")
            
            submit_response_json = submit_response.json()

            time.sleep(10)
            
            # Check submission status

            headers = {
                'Content-Type': 'application/json',
                'Sec-Fetch-Dest': 'empty',
                'Accept': '*/*',
                'Sec-Fetch-Site': 'same-origin',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'cors',
                'Host': 'leetcode.com',
                'Referer': f"{problem_url}/submissions/{submit_response_json['submission_id']}/",
                'Connection': 'keep-alive',
                'x-csrftoken': cookies['csrftoken'],
            }

            status_response = requests.get(f"https://leetcode.com/submissions/detail/{submit_response_json['submission_id']}/check/", cookies=cookies, headers=headers)


            print(status_response)
            
            if status_response.status_code != 200:
                time.sleep(10)
                status_response = requests.get(f"https://leetcode.com/submissions/detail/{submit_response_json['submission_id']}/check/", cookies=cookies, headers=headers)
                if status_response.status_code != 200:
                    continue
            
            status_response_json = status_response.json()
            
            with open(f'./Submissions/{id}-{i}.json', 'w') as f:
                json.dump(status_response_json, f, indent=4)

            print(f"Time taken: {time.time()-start_time}")
        except Exception as e:
            print(e)
