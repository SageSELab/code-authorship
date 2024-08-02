import openai
import pandas as pd
import sys
import time
import os
import json

with open('av_prompt.txt', 'r') as file:
    prompt_template = file.read()

dataset = sys.argv[1]
sample = sys.argv[2]

client = openai.OpenAI(api_key='OPENAI_API')

dataset_df = pd.read_csv(f'./{dataset}/{dataset.lower()}.csv')

code_snippets = dataset_df['code'].values

sample_df = pd.read_csv(f'./Samples/{dataset.lower()}_{sample}.csv')

for index, row in sample_df.iterrows():
    c1_index = row['c1']
    c2_index = row['c2']
    
    if os.path.exists(f'./av_response_gpt-4/{dataset.lower()}/{sample}/{c1_index}_{c2_index}.json'):
        print(c1_index, c2_index, 'already done')
        continue
    code1 = code_snippets[c1_index-1]
    code2 = code_snippets[c2_index-1]
    
    prompt = prompt_template.format(code1, code2)
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      response_format={ "type": "json_object" },
      temperature = 0.2,
      messages=[
      {"role": "system", "content": "Let’s consider you as an expert in code authorship verification."},
        {"role": "user", "content": prompt}
      ]
    )
    response_object = json.loads(response.choices[0].message.content)
    response_object['ground_truth'] = float(row['same'])
    response_object['predicted'] = 1.0 if response_object['final_confidence_score'] >= 0.5 else 0.0
    response_object['is_correct'] = 1.0 if response_object['ground_truth'] == response_object['predicted'] else 0.0
    with open(f'./av_response_gpt-4/{dataset.lower()}/{sample}/{c1_index}_{c2_index}.json', 'w') as file:
        file.write(json.dumps(response_object))
    print(c1_index, c2_index, 'done')
    time.sleep(3)
    
    
    