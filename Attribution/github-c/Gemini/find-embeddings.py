
import pandas as pd


import numpy as np


df_train = pd.read_csv(f'../data/fold_0_train.csv')
df_test = pd.read_csv(f'../data/fold_0_test.csv')
df = pd.concat([df_train, df_test])


X = np.load('./gemini_X.npy', allow_pickle=True)
Y = np.load('./gemini_Y.npy', allow_pickle=True)

df['X'] = X.tolist()
df['Y'] = Y.tolist()

for fold in range(8):
    df_train = pd.read_csv(f'../data/fold_{fold}_train.csv')
    df_test = pd.read_csv(f'../data/fold_{fold}_test.csv')
    
    df_train['X'] = df_train['code'].apply(lambda x: df[df['code']== x]['X'].values[0])
    df_train['Y'] = df_train['code'].apply(lambda x: df[df['code']== x]['Y'].values[0])
    
    train_X = np.vstack(df_train['X'].values)
    train_Y = df_train['Y'].values
    
    np.save(f'./gemini_fold_{fold}_X_train.npy', train_X)
    np.save(f'./gemini_fold_{fold}_Y_train.npy', train_Y)
    
    #test
    
    df_test['X'] = df_test['code'].apply(lambda x: df[df['code']== x]['X'].values[0])
    df_test['Y'] = df_test['code'].apply(lambda x: df[df['code']== x]['Y'].values[0])
    
    test_X = np.vstack(df_test['X'].values)
    test_Y = df_test['Y'].values
    
    np.save(f'./gemini_fold_{fold}_X_test.npy', test_X)
    np.save(f'./gemini_fold_{fold}_Y_test.npy', test_Y)




