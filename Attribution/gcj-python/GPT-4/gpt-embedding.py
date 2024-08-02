import pandas as pd
import openai
import numpy as np
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # 
import sys
import time

start_time = time.time()

client = openai.OpenAI(api_key='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')

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
# def get_embeddings(text):
#     response = openai.Embedding.create(input=text, engine='text-embedding-ada-002')['data']
#     print(response)
#     return [x["embedding"] for x in response]

#Load Data
df_train = pd.read_csv(f'../data/fold_0_train.csv')
df_test = pd.read_csv(f'../data/fold_0_test.csv')
df = pd.concat([df_train, df_test])

#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(text, model="text-embedding-3-large"):
   embedding = client.embeddings.create(input = [text], model=model).data[0].embedding
   print(embedding)
   return embedding

df['encoding'] = df['code'].apply(get_embedding)

X = np.vstack(df['encoding'].values)
Y = df['author'].values

np.save(f'./gpt_X.npy', X)
np.save(f'./gpt_Y.npy', Y)

end_time = time.time()

duration = end_time - start_time