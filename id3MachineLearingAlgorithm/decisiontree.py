import math
from collections import Counter


# https://www.geeksforgeeks.org/counters-in-python-set-1/

class Feature:

    def __init__(self, feature, subtree=[]):
        self.feature = feature
        self.subtree = subtree

    def __repr__(self):
        return self.feature

    def __str__(self):
        return str(self.feature)


class Leaf:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ID3:

    def __init__(self, depth=None):
        self.root = None
        self.depth = depth

    def createTree(self, node, tree):

        if type(node) is Leaf:
            tree += ' ' + node.name
            temp = list(tree.split())
            i = 0
            num = 1
            while i < len(temp):
                if i % 2 == 0 and i != len(temp) - 1:
                    if i == 0:
                        nodeDescription = str(num) + ':' + temp[i] + '='
                    else:
                        nodeDescription = ' ' + str(num) + ':' + temp[i] + '='

                    temp[i] = nodeDescription
                    num += 1
                if temp[i] == node.name and i == len(temp) - 1:
                    temp[i] = ' ' + node.name
                i += 1
            print(''.join(temp))
            return

        tree += ' ' + node.feature

        for l in node.subtree:
            if type(l) is Leaf:
                tree += ' ' + l.name
                temp = list(tree.split())
                i = 0
                num = 1
                while i < len(temp):
                    if i % 2 == 0 and i != len(temp) - 1:
                        if i == 0:
                            nodeDescription = str(num) + ':' + temp[i] + '='
                        else:
                            nodeDescription = ' ' + str(num) + ':' + temp[i] + '='
                        temp[i] = nodeDescription
                        num += 1
                    if temp[i] == l.name and i == len(temp) - 1:
                        temp[i] = ' ' + l.name
                    i += 1
                print(''.join(temp))
                return
            self.createTree(l, tree)

    def fit(self, dataSet, dataSetP, features, y, depth=None):

        self.root = self.id3(dataSet, dataSetP, features, y, depth)

    def entropy(self, featurelabels):

        length = sum(v for k, v in featurelabels.items() if k is not False)

        entropy = -sum((v / length) * math.log2(v / length) for k, v in featurelabels.items() if k is not False)

        return entropy

    def informationGain(self, dataSet, feature):

        label = list(dataSet[0].keys())[-1]

        informationGain = self.entropy(dict(Counter(row[label] for row in dataSet)))

        lenD = len(dataSet)

        featureCount = dict(Counter(row[feature] for row in dataSet))

        for value, count in featureCount.items():
            informationGain -= (count / lenD) * self.entropy(dict(Counter(row.get(feature) == value
                                                                          and row.get(label) for row in dataSet)))

        return round(informationGain, 4)

    def id3(self, dataSet, dataSetP, features, y, depth=None):

        if depth == 0:
            return Leaf(min(k for k, v in dict(Counter(row.get(y) for row in dataSet)).items()
                            if v == max(dict(Counter(row.get(y) for row in dataSet)).values())))

        if len(dataSet) == 0:
            return Leaf(max(dict(Counter(row.get(y) for row in dataSetP))))

        v = min(k for k, v in dict(Counter(row.get(y) for row in dataSet)).items()
                if v == max(dict(Counter(row.get(y) for row in dataSet)).values()))

        if len(features) == 0 or dataSet == list(row for row in dataSet if row.get(y) == v):
            return Leaf(v)

        x = min(f for f in features if self.informationGain(dataSet, f)
                == max(self.informationGain(dataSet, f) for f in features))

        subtrees = []

        for value in list(dict(Counter(row.get(x) for row in dataSet)).keys()):

            if depth is not None:
                t = self.id3(list(row for row in dataSet if row.get(x) == value), dataSet,
                             list(feature for feature in features if feature != x), y, depth - 1)
            else:
                t = self.id3(list(row for row in dataSet if row.get(x) == value), dataSet,
                             list(feature for feature in features if feature != x), y)
            sub = [t]
            subtrees.append(Feature(value, sub))

        return Feature(x, subtrees)

    def predicting(self, node, features, dataSet, y):

        for feature, value in features.items():

            if type(node) is Leaf:
                label = node.name
                return label

            if feature == node.feature:
                for l in node.subtree:
                    if type(l) is Leaf:
                        label = l.name
                        return label
                    if l.feature == value:
                        for ll in l.subtree:
                            return self.predicting(ll, features, dataSet, y)

        return min(k for k, v in dict(Counter(row.get(y) for row in dataSet)).items()
                   if v == max(dict(Counter(row.get(y) for row in dataSet)).values()))

    def predict(self, testSet, dataSet, label):

        predictions = []

        for row in testSet:
            predictions.append(self.predicting(self.root, row, dataSet, label))

        return predictions

    def accuracy(self, predictions, testSet, label):

        testLabels = list(row.get(label) for row in testSet)

        return '{:.5f}'.format(
            (sum(labelP == labelT for labelP, labelT in zip(predictions, testLabels))) / len(testLabels), 5)

    def confusionMatrix(self, predictions, testSet, label):

        testLabels = list(row.get(label) for row in testSet)
        matrixlist = []

        labels = set(testLabels)
        for e in sorted(labels):
            for k in sorted(labels):
                matrixlist.append(sum(1 for labelP, labelT in zip(predictions, testLabels)
                                      if labelT == e and labelP == k))

        i = 0
        j = 0

        while i < len(matrixlist):
            print(matrixlist[i], end=' ')
            if len(matrixlist) % (j + 1) == 0 and (j + 1) != 1:
                j = -1
                print('')
            j += 1
            i += 1
