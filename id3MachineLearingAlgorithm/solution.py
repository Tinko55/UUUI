import csv
import sys
import decisiontree
from collections import Counter

#https://www.geeksforgeeks.org/reading-csv-files-in-python/

def input(trainingSetFile, testSetFile):

    with open(trainingSetFile, 'r') as trainingFile:


        trainingCsv=csv.DictReader(trainingFile)

        dataSet=list(trainingCsv)

    with open(testSetFile, 'r') as testFile:

        testCsv = csv.DictReader(testFile)

        testSet =list(testCsv)

    features = list(dataSet[0].keys())

    label=features[-1]

    features.remove(features[-1])

    return dataSet, testSet, features, label

def main():

    depthLimitation=''

    data=sys.argv

    dataSet, testSet, features, label = input(data[1], data[2])

    if len(data) == 4:
        depthLimitation = data[3]

    if depthLimitation != '':
        model = decisiontree.ID3(int(depthLimitation))
        model.fit(dataSet, dataSet, features, label, int(depthLimitation))
    else:
        model = decisiontree.ID3()
        model.fit(dataSet, dataSet, features, label)

    tree = ''
    print('[BRANCHES]:')
    model.createTree(model.root, tree)

    predictions = model.predict(testSet, dataSet, label)


    print('[PREDICTIONS]: ', ' '.join(predictions))

    accuracy = model.accuracy(predictions, testSet, label)
    print('[ACCURACY]: {0}'.format(accuracy))

    print('[CONFUSION_MATRIX]:')
    model.confusionMatrix(predictions, testSet, label)

if __name__ == '__main__':
    main()
