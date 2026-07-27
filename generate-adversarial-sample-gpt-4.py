"""
Generate adversarial samples by asking GPT-4o to apply each of the 28
semantics-preserving transformation rules (Prompts/0.txt .. Prompts/27.txt) to
every code snippet that all models attributed correctly.

Requires an OpenAI API key in the OPENAI_API_KEY environment variable:

    export OPENAI_API_KEY=sk-...
    python generate-adversarial-sample-gpt-4.py

Output is one .txt file per (sample, rule) pair under
./Adversarial-Samples-GPT4/. Existing files are skipped, so the script can be
interrupted and resumed.
"""

import pandas as pd
import os
import time
import openai

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit(
        "OPENAI_API_KEY is not set.\n"
        "Export it before running, e.g.:  export OPENAI_API_KEY=sk-...\n"
        "In Docker, put it in .env (see .env.example) and it is passed through "
        "automatically."
    )

client = openai.OpenAI(api_key=api_key)

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
        