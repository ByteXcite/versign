import classifiers
from sklearn.metrics import accuracy_score

import numpy as np
import os, sys
import scipy.io

from matplotlib import pyplot as plt

def read_train_data(train_dir):
    x_train = []
    for f in os.listdir(train_dir):
        if f.endswith('.mat'):
            mat = scipy.io.loadmat(train_dir + '/' + f)
            feat = np.array(mat['feature_vector'][0][:])
            x_train.append(feat)
    return np.array(x_train)

def read_test_data(test_dir):
    #groundtruth = np.loadtxt(test_dir + '/groundtruth.txt').flatten()

    files = []
    x_test = []
    y_true = []
    for f in os.listdir(test_dir):
        if f.endswith('.mat'):
            files.append(f[:-4])

            # Read feature vector
            mat = scipy.io.loadmat(test_dir + '/' + f)
            feat = np.array(mat['feature_vector'][0][:])
            x_test.append(feat)

            if f.startswith('F'):
                label = -1
            elif f.startswith('G'):
                label = 1
            # Read label
            #if len(f) == 14:
            #    label = -1
            #elif len(f) == 10:
            #    label = 1
            #id = int(f[1:-4]) - 1
            #label = groundtruth[id]
            y_true.append(int(label))
    
    return files, np.array(x_test), y_true

def get_equal_error(far, frr):
    idx = np.argwhere(np.diff(np.sign(far - frr)) != 0).reshape(-1) + 0
    eer = np.mean(far[idx])
    return eer, int(np.mean(idx))

def get_user_classes(train_dir, test_dir):
    c_test = []
    for c in os.listdir(test_dir):
        if os.path.isdir(os.path.join(test_dir, c)):
            c_test.append(c)

    c_train = []
    for c in os.listdir(train_dir):
        if os.path.isdir(os.path.join(train_dir, c)):
            c_train.append(c)

    classes = []
    for c in c_test:
        if c in c_train:
            classes.append(c)

    return classes

# Define globals
data_dir  = 'db/features'
DATASET   = 'our_dataset'

train_dir = data_dir + '/' + DATASET + '/' + 'Ref'
test_dir  = data_dir + '/' + DATASET + '/' + 'Questioned'

NOR_OF_STEPS = 100.0
steps = range(0, int(NOR_OF_STEPS), 1)
classes = get_user_classes(train_dir, test_dir)

print 'Dataset:', DATASET
print 'No. of users:', len(classes)

# Output predictions to a csv file
outfile = open(test_dir + '/predictions.csv', 'w')

# Write header row
outfile.write('U_ID,Q_ID,Pr,Label')
for i in steps:
    outfile.write(',T='+str(i/NOR_OF_STEPS))
outfile.write('\n')

_preds=[]
_Y_true=[]

for c in classes:
    DIR_TRAIN = train_dir + '/' + c
    DIR_TEST = test_dir + '/' + c

    # Load training data
    x_train = read_train_data(DIR_TRAIN)

    # Load test data
    files, x_test, Y_true = read_test_data(DIR_TEST)

    # Get predictions from OneClassSVM
    Y_test, Y_train, n_error_train, Y_prob = classifiers.OneClassSVM(x_train, x_test)

    preds = []
    for i in range(len(Y_prob)):
        tfile = files[i]
        prob = Y_prob[i][0]
        outfile.write(c + ',' + tfile + ',' + str(prob) + ',' + str(Y_true[i]))
        row = []
        for j in steps:
            if prob > j/NOR_OF_STEPS:
                pred = 1
            else:
                pred = -1

            outfile.write(',' + str(pred))
            row.append(pred)

        preds.append(row)
        outfile.write('\n')
    _preds += preds
    _Y_true += Y_true

_preds = np.array(_preds)

# Calculate and write FAR and FRR
FAR = []
FRR = []
for i in steps:
    Y_test = _preds[:, [i]].flatten()
    FA = 0
    FR = 0
    for j in range(len(Y_test)):
        if _Y_true[j] == -1 and Y_test[j] == 1:
            FA += 1
        elif _Y_true[j] == 1 and Y_test[j] == -1:
            FR += 1
    
    FAR.append(100.*FA/len(Y_test))
    FRR.append(100.*FR/len(Y_test))

outfile.write(',,,FAR,' + str(FAR).replace('[', '').replace(']','') + '\n')
FAR = np.array(FAR)

outfile.write(',,,FRR,' + str(FRR).replace('[', '').replace(']','') + '\n')
FRR = np.array(FRR)

EER, idx = get_equal_error(FAR, FRR)
print "EER:", str(round(EER, 3)) + '%\n'
outfile.write(',,,EER,' + str(EER) + '%\n')

x = np.arange(0, NOR_OF_STEPS)

fig = plt.figure()
ax = fig.add_subplot(111, title='Error Rates (Dataset: ' + DATASET + ')')
ax.plot(x, FAR, '-', c='r')
ax.plot(x, FRR, '-', c='g')
ax.plot(idx, EER, 'o', c='b')
ax.legend(('FAR', 'FRR', 'ERR='+str(EER)+'%'))
plt.savefig(test_dir + '/figure.png')