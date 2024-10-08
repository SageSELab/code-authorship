import openai
openai.api_key = ''
client = openai.OpenAI()

import os

def get_text_filenames_without_extension(directory):
    text_filenames = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Filter for text files
            text_filenames.append(os.path.splitext(filename)[0])  # Get filename without extension
    return text_filenames

# Example usage
directory_path = './Samples (Id-ProblemId-Lang-Author)'
text_files_without_extension = get_text_filenames_without_extension(directory_path)

for text_file in text_files_without_extension:

  with open(f'./Samples (Id-ProblemId-Lang-Author)/{text_file}.txt', 'r') as file:
      code = file.read()

  for i in range(0,1):
    with open(f'./Prompts/{i}.txt', 'r') as file:
      prompt = file.read()
    
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      
      messages=[
      {"role": "system", "content": "You are a helpful assistant designed to change code snippets based on prompts."},
        {"role": "user", "content": prompt +'\n\n' + code}
      ]
    )
    print(text_file)
    with open(f'./AdversarialSamples/{text_file}/{i}.txt', 'w') as file:
      file.write(response.choices[0].message.content)
    
    print(f'Prompt {i} completed')
