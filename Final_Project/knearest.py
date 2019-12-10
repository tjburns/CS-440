import util
import numpy
PRINT = True

class kNearestClassifier:
  
    def __init__( self, legalLabels, neighbors):
        self.legalLabels = legalLabels
        self.type = "knearest"
        self.neighbors = neighbors

    def classify(self, data, trainingData, trainingLabels):

        trainingMatrix = []
        for datum in trainingData:
            # convert each element of training data into matrix of pixels 
            datumMatrix = numpy.zeros((70,70))
            for pixel in datum.keys():
                datumMatrix[pixel] = datum[pixel]
            trainingMatrix.append(datumMatrix)

        guesses = []
        for element in data:
            # convert current data element to matrix
            elementMatrix = numpy.zeros((70,70))
            for pixel in element.keys():
                elementMatrix[pixel] = element[pixel]
            # calculate euclidean distance with each element of trainingMatrix
            # could be done with the manhattan distance method in util alternatively
            distances = []
            for sample in trainingMatrix:
                d = numpy.linalg.norm(elementMatrix - sample)
                distances.append(d)
            # find k values to track
            sortedDistances = sorted(distances)
            ksorted = sortedDistances[0:self.neighbors]
            closestLabels = []
            for dist in ksorted:
                closestLabels.append(trainingLabels[distances.index(dist)])
            label = max(set(closestLabels), key=closestLabels.count)
            # empty if k=0, implement something to catch that and either random guess or default guess

            # 'label' here is the most common label
            # append it to guesses
            guesses.append(label)
        
        return guesses