"""
ANN + Cross Validation 

@author: YiHan
"""

import pickle
import pandas as pd
import numpy as np
import os
import re
from keras.models import Sequential
from keras.layers import Dropout, Dense
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# ----------------------------------------------------- Preping Data and Model ----------------------------------------------------- 
inputFile = os.path.join(__location__, 'NNset_all.p')
inputFile = pd.read_pickle(inputFile)
X = np.array([value[-2] for key, value in inputFile.items()])
Y = np.array([value[-1] for key, value in inputFile.items()])

# -------------------------------------------------------- function tanimoto  ---------------------------------------------------------- 
def tanimoto(candi, predi):
    predi = list(map(lambda x: round(x), predi))

    bothAB = 0
    onlyA = 0
    onlyB = 0
    for i in range(0,len(candi)):
        if candi[i] == 1 and predi[i] == 1:
            bothAB += 1
        elif candi[i] == 1 and predi[i] == 0:
            onlyB += 1
        elif predi[i] == 1 and candi[i] == 0:
            onlyA += 1
    div = onlyA + onlyB + bothAB
    return 0 if div == 0 else bothAB / div

#-------remove 0s for train and test-------
def remove0(X_train, X_test):
    # Removes bins from the vectors  that have little significance 
    col_num = len(X_train[0])
    row_num = len(X_train)
    allzero_index = [0]*col_num
    for i in range(col_num):#each column
        for j in range(row_num):#check in each compound
            all_zero=True
            if X_train[j][i]!=0:
                all_zero=False
                break
        if all_zero==True:
            allzero_index[i]=1
    keep_index = [i for i in range(len(allzero_index)) if allzero_index[i]==0]
    X_train = X_train[:,keep_index]
    X_test = X_test[:,keep_index]
    return(X_train, X_test)

# --------------------------------------------------------  5 folder cross-validation procedure  ---------------------------------------------------------- 
kfold = KFold(n_splits=5, shuffle=True)
f1_score_5 = []
tanimoto_5 = []
accuracy_5 = []
fold_no = 1
for train, test in kfold.split(X, Y):

  # Remove 0s
    X_train, X_test = remove0(X[train], X[test])
    input_len = len(X_train[0])

  # Define the model architecture
    model = Sequential()
    model.add(Dense(528, input_dim=input_len, activation='sigmoid'))
    

  # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])


  # Generate a print
    print('------------------------------------------------------------------------')
    print(f'Training for fold {fold_no} ...')

    # Fit data to model
    model_fit = model.fit(X_train, Y[train],
                batch_size=100,
                epochs=10,
                verbose=1)

    # Generate generalization metrics
    accuracy = model.evaluate(X_test, Y[test], verbose=0)
    accuracy_5.append(accuracy[1])
    print(f'Accuracy for fold {fold_no}: {model.metrics_names[0]} of {accuracy[0]}; {model.metrics_names[1]} of {accuracy[1]*100}%')
    y_pred = model.predict(X_test, verbose=0)
    # calculate tanimoto and f1_score
    tanimoto_arr = []
    f1_arr = []
    for i in range(len(y_pred)):
        y1 = np.array(Y[test][i])
        y2 = np.array(list(map(lambda x: round(x), y_pred[i])))
        tanimoto_score = tanimoto(y1, y2)
        tanimoto_arr.append(tanimoto_score)
        f1Score = f1_score(y1, y2)
        f1_arr.append(f1Score)
    print(f'tanimoto for fold {fold_no}: {np.mean(tanimoto_arr) * 100}%')
    print(f'f1_score for fold {fold_no}: {np.mean(f1_arr) * 100}%')
    
    tanimoto_5.append(np.mean(tanimoto_arr))
    f1_score_5.append(np.mean(f1_arr))
    

    # Increase fold number
    fold_no = fold_no + 1


# print(accuracy_5)
# print(tanimoto_5)
# print(f1_score_5)

# --------------------------------------------------------  Average accuracy  ---------------------------------------------------------- 

print(f'Average accuracy for 5 folder: {np.mean(accuracy_5) * 100}%')
print(f'Average tanimoto for 5 folder: {np.mean(tanimoto_5) * 100}%')
print(f'Average f1_score for 5 folder: {np.mean(f1_score_5) * 100}%')

