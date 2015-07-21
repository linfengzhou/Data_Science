#import os
#os.chdir('E:\Code\machinelearninginaction code\ch02')
#E:\Code\machinelearninginaction\Ch02
from numpy import *
import numpy as np 
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels



def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    ##Distance calculation
    diffMat = tile(inX, (dataSetSize,1)) - dataSet #tile() function = repeat
    sqDiffMat =  diffMat ** 2 
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    
    classCount = {}   
    
    ### Voting with lowest k distance
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 
    
    ### Sort Dictionary
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)

    return sortedClassCount[0][0]

##Paring data from a text file
def file2matrix(filename):
    ### Get number of lines in file
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    ### Create NumPy matrix to return 
        #### hard-coded in the sieze of this to be numberOfLines x 3
        #### but you could add some conde to make 
        #### this adaptable to the various input
    returnMat = np.zeros((numberOfLines,3))
    
    classLabelVector = [] 
    fr = open(filename)
    index = 0

    ### Parse line to a list

    for line in arrayOLines:

        #### strip off the return line character with line.strip()

        line = line.strip()

        #### split the line into list of elements delimited by the tab 
        #### character '\t'

        listFromLine = line.split('\t')
   
        returnMat[index,:] = listFromLine[0:3]
        
        #### using negative indexing to get the last item from the list
        #### you have to explicitly tell the interpreter that you'd like
        #### the integer version of the last item
        classLabelVector.append(int(listFromLine[-1]))
        
        index += 1 
    return returnMat, classLabelVector
#code: datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')  
    
# Analyze: creating scatter plots with Matplotlib
def createScatter(datingDataMat,datingLabels):
    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,1], datingDataMat[:,2],15.0*np.array(datingLabels),
           15.0*np.array(datingLabels))
    plt.show()

## Prepaer: normalizing numeric values
def autoNorm(dataSet):
    #### The 0 in dataSet.min(0) allows you to make the minimums from
    #### the columns, not the rows
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges, (m,1)) ##element wise divide
    return normDataSet, ranges, minVals
# code: normMat, ranges, minVals = kNN.autoNorm(datingDataMat)

## Test:tesing the classifier as a whole program
### classifier testing code for dating site
def datingClassTest():
    hoRatio = 0.10

    ####get the data into a form you can use
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]

    ####decide which vector from normMat will be used for testing
    numTestVecs = int(m * hoRatio)
    
    #### calculated and displayed the error rate    
    errorCount = 0.0 
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],
                                     datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d"\
        %(classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]) :
            errorCount += 1.0 
    print "the total error rate is: %f" %(errorCount/float(numTestVecs))
        
### Dating site predictor function
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input(
    "percentage of time spent playing video game? "))
    ffmiles = float(raw_input("frequent flier miles earned per year? "))
    iceCream = float(raw_input("liters of ice cream consumed per year? "))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffmiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals) / ranges,normMat,
                                 datingLabels, 3)
    print "You will probably like this person:", resultList[classifierResult
    - 1]
