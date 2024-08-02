
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import confusion_matrix
import json
import pandas as pd

all_corrects = []

for fold in range(8):
    X_train, X_test = np.load(f'./gemini_fold_{fold}_X_train.npy', allow_pickle=True), np.load(f'./gemini_fold_{fold}_X_test.npy', allow_pickle=True)
    y_train, y_test = np.load(f'./gemini_fold_{fold}_Y_train.npy', allow_pickle=True), np.load(f'./gemini_fold_{fold}_Y_test.npy', allow_pickle=True)


    unique_Y = np.unique(y_train).tolist()

    y_train = np.array([unique_Y.index(y) for y in y_train])
    y_test = np.array([unique_Y.index(y) for y in y_test])
    
    svm_classifier = SVC(kernel='linear')

    svm_classifier.fit(X_train, y_train)
    predictions = svm_classifier.predict(X_test)
    
    # Comparing true labels and predicted labels
    cm = confusion_matrix(y_test, predictions)
    
    # Store or process the confusion matrix / predictions as needed
    print((y_test.tolist(), predictions.tolist()))
    
    results = {
        'Actual': y_test.tolist(),
        'Predicted': predictions.tolist(),
    }
    
    df = pd.DataFrame(results)
    df['Id'] = df.index
    
    
    df['IsCorrect'] = df['Actual'] == df['Predicted']
    
    print(len(df[df['IsCorrect'] == True]) / len(df))
    
    df = df[df['IsCorrect'] == True]
    
    all_corrects.extend([f'1-{fold}-{id}' for id in df['Id']])

with open(f'all_corrects_gpt.json', 'w') as f:
    json.dump(all_corrects, f)






