import pandas as pd
import os
import time
import openai
client = openai.OpenAI(api_key='')

os.makedirs('./Adversarial-Samples-GPT4', exist_ok=True)

df = pd.read_csv("./leetcode-all-models-corrects-intersection.csv")

for index, row in df.iterrows():
    code = row["code"]
    
    for i in range(28):
        
        if os.path.exists(f'./Adversarial-Samples-GPT4/{row["Id"]}-{i}.txt'):
            continue
        
        start_time = time.time()
        
        with open(f'./Prompts/{i}.txt') as f:
            prompt = f.read()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to change code snippets based on prompts."},
                {"role": "user", "content": prompt + '\n\n' + code}
            ],
            temperature=0.1)

        with open(f'./Adversarial-Samples-GPT4/{row["Id"]}-{i}.txt', 'w') as file:
          file.write(response.choices[0].message.content)
        