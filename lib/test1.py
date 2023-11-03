import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

try:
    # Open file
    fileName = "matrix_12"
    dataMatrix = np.load("assets/data/1/"+fileName+".npy")
    
    # Initial Variable
    ## Original Matrix
    totalValue = 0
    totalData = 0
    totalValueMainDiagonal = 0
    totalDataMainDiagonal = 0
    totalValueSecondDiagonal = 0
    totalDataSecondDiagonal = 0
    maximumValue = dataMatrix.max()
    minimumValue = dataMatrix.min()
    
    normalizeDataMatrix = (dataMatrix - minimumValue) / (maximumValue - minimumValue)
    
    ## Normalize Matrix
    normalizeTotalValue = 0
    normalizeTotalData = 0
    normalizeTotalValueMainDiagonal = 0
    normalizeTotalDataMainDiagonal = 0
    normalizeTotalValueSecondDiagonal = 0
    normalizeTotalDataSecondDiagonal = 0
    normalizeMaximumValue = normalizeDataMatrix.max()
    normalizeMinimumValue = normalizeDataMatrix.min()
    
    
    for i in range(len(dataMatrix)):
        dataRow = dataMatrix[i]
        normalizeDataRow = normalizeDataMatrix[i]
        for j in range(len(dataRow)):
            # Original
            totalValue += dataRow[j]
            totalData += 1
            # Normalize
            normalizeTotalValue += normalizeDataRow[j]
            normalizeTotalData += 1
            if(i == j):
                # Original
                totalValueMainDiagonal += dataRow[j]
                totalDataMainDiagonal += 1
                # Normalize
                normalizeTotalValueMainDiagonal += normalizeDataRow[j]
                normalizeTotalDataMainDiagonal += 1
            if(j == ((len(dataRow) - 1) - i)):
                # Original
                totalValueSecondDiagonal += dataRow[j]
                totalDataSecondDiagonal += 1
                # Normalize
                normalizeTotalValueSecondDiagonal += normalizeDataRow[j]
                normalizeTotalDataSecondDiagonal += 1
                
    # Original          
    average = totalValue/totalData
    averageMainDiagonal = totalValueMainDiagonal/totalDataMainDiagonal
    averageSecondDiagonal = totalValueSecondDiagonal/totalDataSecondDiagonal
    # Normalize
    normalizeAverage = normalizeTotalValue/normalizeTotalData
    normalizeAverageMainDiagonal = normalizeTotalValueMainDiagonal/normalizeTotalDataMainDiagonal
    normalizeAverageSecondDiagonal = normalizeTotalValueSecondDiagonal/normalizeTotalDataSecondDiagonal
    
    # Data to be written
    originalMatrix = {
        "sum": totalValue,
        "avr": average,
        "sumMD": totalValueMainDiagonal,
        "avrMD": averageMainDiagonal,
        "sumSD": totalValueSecondDiagonal,
        "avrSD": averageSecondDiagonal,
        "max": maximumValue,
        "min": minimumValue
    }
    normalizeMatrix = {
        "sum": normalizeTotalValue,
        "avr": normalizeAverage,
        "sumMD": normalizeTotalValueMainDiagonal,
        "avrMD": normalizeAverageMainDiagonal,
        "sumSD": normalizeTotalValueSecondDiagonal,
        "avrSD": normalizeAverageSecondDiagonal,
        "max": normalizeMaximumValue,
        "min": normalizeMinimumValue
    }
    
    # Serializing json
    json_object_original = json.dumps(originalMatrix, indent=4, cls=NpEncoder)
    json_object_normalize = json.dumps(normalizeMatrix, indent=4, cls=NpEncoder)
    
    # Writing to json
    with open("assets/output/1/"+fileName+"_original_output.json", "w") as outfile:
        outfile.write(json_object_original)
    with open("assets/output/1/"+fileName+"_normalize_output.json", "w") as outfile:
        outfile.write(json_object_normalize)
    
    # Save normalize matrix to npy
    np.save("assets/output/1/"+fileName+"_normalize.npy", normalizeDataMatrix)
        
        
except Exception as e:
    print(e)