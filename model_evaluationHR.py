
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Dense
import numpy as np
import pickle
import sys
import random

# ------------------------------------------------------------- File Handling ------------------------------------------------------------- 

input_file = "NIST_HR_fp.p"

with open(input_file, 'rb') as handle:
    DATA = pickle.load(handle)

#    for key,value in DATA.items():
#        print (key)
#        print(value)
    	#print (value,'\n',  value[-1], '\n')

# ----------------------------------------------------- Preping Data and Model ----------------------------------------------------- 

# Fix random seed for reproducibility

np.random.seed(7)


#creat random train and test list
samplelist=[i for i in range(0,25550)]

ttlist=[]
testlist = random.sample(samplelist, 4533)
for i in range(0,25550):
    if i in testlist:
        ttlist.append(1)
    else:
        ttlist.append(0)
#train:0,test:1

# Split the dict into train_dict and test_dict
i=0
train_dict={}
test_dict={}
for key,value in DATA.items():
    if ttlist[i] == 0:
        train_dict[key]=value
    else:
        test_dict[key]=value
    i = i + 1

# Split into input (X) and output (Y) variables
train_XY=[]
test_XY=[]
for key,value in train_dict.items():
	train_XY.append([value[-2],value[-1]])
for key,value in test_dict.items():
	test_XY.append([value[-2],value[-1]])

train_X = np.array([i[0] for i in train_XY])
train_Y = np.array([i[1] for i in train_XY])
test_X  = np.array([i[0] for i in test_XY])
test_Y  = np.array([i[1] for i in test_XY])


#for i in range(len(train_X)):
#	#print(train_X[i])
#	print("length of X: ", len(train_X[i]))
#	#print(train_Y[i])
#	print("length of Y: ", len(train_Y[i]))
#	print("xxxxxxxxxxxxxx")

# --------------------------------------------------------- Create Model ---------------------------------------------------------- 

model = Sequential()
#833
model.add(Dense(800, input_dim=986, activation='relu'))
#model.add(Dropout(0.25))

model.add(Dense(600, activation='relu'))
model.add(Dense(400, activation='relu'))
# model.add(Dropout(0.25))

model.add(Dense(200, activation='relu'))
model.add(Dense(528, activation='sigmoid'))#那我们的话，应该是就是把output的node的个数改一下。下面compile里的参数应该是不用改的。
#185
# -------------------------------------------------------- Compile Model ---------------------------------------------------------- 

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])

# ---------------------------------------------------------- Fit Model ------------------------------------------------------------ 

model.fit(train_X, train_Y, epochs=20, batch_size=100)

# -------------------------------------------------------- Evaluate Model --------------------------------------------------------- 

scores = model.evaluate(test_X, test_Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# Variable 'a' represents 'accuracy'

a = model.predict(test_X)
a[a>=0.5] = 1
a[a<0.5] = 0
#print(a)
# -----------save inchikey+predict fingerprint into predic_dict--------------
predic_dict = {}
s = 0
for key,value in test_dict.items():
    ms = np.array(value[-2])
    ms.shape=(1,986)
    a = model.predict(ms)
    a[a>=0.5] = 1
    a[a<0.5] = 0
    a = a.astype(np.int32).tolist()
    a = a[0]
    #predic_dict[key]=[value[0],value[1],value[2],value[8],value[-2],value[9],a]
    value.append(a)
    predic_dict[key]=value
    s = s + 1
# -----------output file---------
pickle_out = open("NIST20_HR_predic_dict_foromics.p", "wb")
pickle.dump(predic_dict, pickle_out)
pickle_out.close()

#save = []
#for key,value in predic_dict.items():
#    same = 0
#    for i in range(527):
#        if value[6][0][i]==value[7][i]:
#            same = same + 1
#    save.append(same/528)
#m = np.mean(save)
#print(m)
    