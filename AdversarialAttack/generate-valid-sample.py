
from transformers import (AutoTokenizer)
import os
import pandas as pd


tokenizer = AutoTokenizer.from_pretrained('./unixcoder_fine_tuned', problem_type="multi_label_classification")

def added(arr1, arr2):
    added_elements = []
    for element in arr2:
        if element not in arr1:
            added_elements.append(element)
    return len(added_elements)/len(arr1)

def removed(arr1, arr2):
    removed_elements = []
    for element in arr1:
        if element not in arr2:
            removed_elements.append(element)
    return len(removed_elements)/len(arr1)


def reordered(arr1, arr2):
    changed_position = 0
    for i in range(min(len(arr1), len(arr2))):
        if arr1[i] != arr2[i] and arr1[i] in arr2:
            changed_position += 1
    return changed_position/len(arr1)

adversarial_samples = []

def get_text_filenames_without_extension(directory):
    text_filenames = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  
            text_filenames.append(os.path.splitext(filename)[0])
    return text_filenames

directory_path = './Samples (Id-ProblemId-Lang-Author)'
text_files_without_extension = get_text_filenames_without_extension(directory_path)
change_dict = {}
for text_file in text_files_without_extension:
    with open(f'{directory_path}/{text_file}.txt', 'r') as file:
        main_code = file.read()
    main_code_tokens = tokenizer(main_code)['input_ids']
    for i in range(0, 28):
        with open(f'./AdversarialSamples/{text_file}/{i}.txt', 'r') as file:
            adv_code = file.read()
            if adv_code == 'NA':
                continue
        adv_code_tokens = tokenizer(adv_code)['input_ids']
        total_change = (added(main_code_tokens, adv_code_tokens) + removed(main_code_tokens, adv_code_tokens) + reordered(main_code_tokens, adv_code_tokens))
        if total_change > 0.5 or total_change == 0:
            continue
        id, problem_id, lang, author = text_file.split('-')
        adversarial_samples.append({
            'id': id,
            'sample_id': f'{text_file}_{i}',
            'total_change': total_change,
            'main_code': main_code,
            'adv_code': adv_code,
            'problem_id': int(problem_id),
            'lang': lang,
            'author': int(author)
        })

pd.DataFrame(adversarial_samples).to_csv('adversarial_samples_v1.csv', index=False)


