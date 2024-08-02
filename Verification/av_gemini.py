import google.generativeai as genai
import os
import pandas as pd
import sys
import json
import time
from google.generativeai.types import generation_types

config = generation_types.GenerationConfig(
                temperature=0.9
            )

with open('av_prompt.txt', 'r') as file:
    prompt_template = file.read()

genai.configure(api_key='GEMINI_API_KEY')

model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json", "temperature": 0.9})

dataset = sys.argv[1]
sample = sys.argv[2]

dataset_df = pd.read_csv(f'./{dataset}/{dataset.lower()}.csv')

code_snippets = dataset_df['code'].values

sample_df = pd.read_csv(f'./Samples/{dataset.lower()}_{sample}.csv')

for index, row in sample_df.iterrows():
    c1_index = row['c1']
    c2_index = row['c2']
    
    if os.path.exists(f'./av_response_gemini/{dataset.lower()}/{sample}/{c1_index}_{c2_index}.json'):
        continue
    code1 = code_snippets[c1_index-1]
    code2 = code_snippets[c2_index-1]
    
    prompt = prompt_template.format(code1, code2)
    
    response = model.generate_content(prompt, generation_config=config)
    
    print(response.text)
    try:
        response_text = response.text
        response_object = json.loads(response_text)
        response_object['final_confidence_score'] = float(response_object['final_confidence_score'])
        response_object['ground_truth'] = float(row['same'])
        response_object['predicted'] = 1.0 if response_object['final_confidence_score'] >= 0.5 else 0.0
        response_object['is_correct'] = 1.0 if response_object['ground_truth'] == response_object['predicted'] else 0.0
        with open(f'./av_response_gemini/{dataset.lower()}/{sample}/{c1_index}_{c2_index}.json', 'w') as file:
            file.write(json.dumps(response_object))
        print(c1_index, c2_index, 'done')
    except Exception as e:
        print(c1_index, c2_index, 'error', e)
    time.sleep(3)