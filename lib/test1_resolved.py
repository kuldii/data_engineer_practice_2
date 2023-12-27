import numpy as np
import json

def getMinimum(dataMatrix):
    return np.min(dataMatrix)

def getMaximum(dataMatrix):
    return np.max(dataMatrix)

def flipTheMatrix(dataMatrix):
    return np.fliplr(dataMatrix)

def getDiagonalData(dataMatrix):
    return np.diagonal(dataMatrix)

def totalSumDiagonal(dataMatrix):
    return np.trace(dataMatrix)

def totalSumAllData(dataMatrix):
    return np.sum(dataMatrix)

def totalAverageAllData(dataMatrix):
    return np.mean(dataMatrix)

def saveToJson(name, data):
    with open("assets/output/1/resolved/"+name, 'w') as jsonFile:
        jsonFile.write(data)

def saveMatrixToNpy(name, ext, dataMatrix):
    np.save("assets/output/1/resolved/"+name+ext, dataMatrix)
    
def getDataFile(name, ext):
    return np.load("assets/data/1/"+name+ext)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

# ================================================= #

fileName = "matrix_12"
ext = ".npy"

# Original Matrix
dataMatrix = getDataFile(fileName, ext)

# Process the Orgininal Matrix
totalSum = totalSumAllData(dataMatrix)
totalAvg = totalAverageAllData(dataMatrix)
mainDiagonalSum = totalSumDiagonal(dataMatrix)
mainDiagonalAvg = totalAverageAllData(getDiagonalData(dataMatrix))

#Flip the Matrix
flipedMatrix = flipTheMatrix(dataMatrix)

# Process the Fliped Matrix
secDiagonalSum = totalSumDiagonal(flipedMatrix)
secDiagonalAvg = totalAverageAllData(getDiagonalData(flipedMatrix))

# Maximum & Minimum
max = getMaximum(dataMatrix)
min = getMinimum(dataMatrix)

# Normalize the matrix
normalizedMatrix = (dataMatrix - getMinimum(dataMatrix)) / (getMaximum(dataMatrix) - getMinimum(dataMatrix))

# Only for check the result
# print("totalSum", totalSum)
# print("totalAvg", totalAvg)
# print("mainDiagonalSum", mainDiagonalSum)
# print("mainDiagonalAvg", mainDiagonalAvg)
# print("secDiagonalSum", secDiagonalSum)
# print("secDiagonalAvg", secDiagonalAvg)
# print("max", max)
# print("min", min)
# print("Normalized Matrix")
# print(normalizedMatrix)

# Save Normalized Matrix to npy
saveMatrixToNpy(fileName + "_normalized", ext, normalizedMatrix)

# Create a dictionary
dataOutput = {
    'sum': totalSum,
    'avr': totalAvg,
    'sumMD': mainDiagonalSum,
    'avrMD': mainDiagonalAvg,
    'sumSD': secDiagonalSum,
    'avrSD': secDiagonalAvg,
    'max': max,
    'min': min
}

jsonResult = json.dumps(dataOutput, indent=4, cls=NpEncoder)

# Save data to json
saveToJson(fileName + "_output.json", jsonResult)