import numpy as np
import msgpack
import os
import json
import statistics

def getFileSize(file):
    return os.path.getsize(file)

def saveToMsgpack(name, data):
    with open("assets/output/3/resolved/"+name, "wb") as jsonFile:
        packed = msgpack.packb(data)
        jsonFile.write(packed)
        
def saveToJson(name, data):
    with open("assets/output/3/resolved/"+name, 'w') as jsonFile:
        jsonFile.write(data)

def getDataFile(name, ext):
    data = None
    with open("assets/data/3/"+name+ext, 'r') as jsonFile:
        data = json.load(jsonFile)
    return data

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

fileName = "products_12"
ext = ".json"

# Get data from file json
data = getDataFile(fileName, ext)

results = []
processedProducts = set()

for product in data:
    if product['name'] in processedProducts:
        continue

    prices = [processProduct['price'] for processProduct in data if processProduct['name'] == product['name']]
            
    avgPrice = statistics.mean(prices)
    maxPrice = max(prices)
    minPrice = min(prices)
    
    results.append({
        'name': product['name'],
        'avgPrice': avgPrice,
        'maxPrice': maxPrice,
        'minPrice': minPrice
    })

    processedProducts.add(product['name'])

jsonResult = json.dumps(results, indent=4, cls=NpEncoder)

# Save data to json
saveToJson(fileName + "_output.json", jsonResult)

# Save data to msgpack
saveToMsgpack(fileName + "_output.msgpack", jsonResult)

# Get file size
jsonSize = getFileSize("assets/output/3/resolved/"+fileName+"_output.json")
msgpackSize = getFileSize("assets/output/3/resolved/"+fileName+"_output.msgpack")

print(f'File json: {jsonSize} bytes')
print(f'File msgpack: {msgpackSize} bytes')