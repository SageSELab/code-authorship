import pandas as pd
import numpy as np
import time
import google.generativeai as genai

start_time = time.time()

#Load Data
df_train = pd.read_csv(f'../data/fold_0_train.csv')
df_test = pd.read_csv(f'../data/fold_0_test.csv')
df = pd.concat([df_train, df_test])

genai.configure(api_key='AIzaSyCWtvnORlOligi7t7usvmyLsjncQTlaeWE')

#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_embedding(text, model="models/embedding-001"):
    result = genai.embed_content(
    model=model,
    content=text,
    task_type="retrieval_document",
    title="Embedding of single string")
    print(result['embedding'])
    return result['embedding']

#print(get_embedding("Hello, World!"))


df['encoding'] = df['code'].apply(get_embedding)

X = np.vstack(df['encoding'].values)
Y = df['author'].values

np.save(f'./gemini_X.npy', X)
np.save(f'./gemini_Y.npy', Y)

end_time = time.time()

duration = end_time - start_time