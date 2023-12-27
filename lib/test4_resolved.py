import numpy as np
import json
import pickle

def saveToPkl(name, data):
    with open("assets/output/4/resolved/"+name+"_new_price.pkl", "wb") as pklFile:
        pickle.dump(data, pklFile, protocol=pickle.HIGHEST_PROTOCOL)

def getDataPklFile(name, ext):
    data = None
    with open("assets/data/4/"+name+ext, 'rb') as pklFile:
        data = pickle.load(pklFile)
    return data

def getDataJsonFile(name, ext):
    data = None
    with open("assets/data/4/"+name+ext, 'r') as jsonFile:
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

jsonFileName = "price_info_12"
pklFileName = "products_12"

dataJson = getDataJsonFile(jsonFileName, ".json")
dataPkl = getDataPklFile(pklFileName, ".pkl")

productsDictionary = {product['name']: product for product in dataPkl}

# Only for test product "Siding" -> original product
# print(next(filter(lambda obj: obj.get('name') == 'Siding', dataPkl), None))

for item in dataJson:
    itemName = item['name']
    method = item['method']
    param = item['param']
    
    # Only for test product "Siding" -> change parameter
    # if(itemName == "Siding"):
    #     print(item)
    
    if itemName in productsDictionary:
        product = productsDictionary[itemName]
        
        if method == 'add':
            product['price'] += param
        elif method == 'sub':
            product['price'] -= param
        elif method == 'percent+':
            product['price'] *= (1 + param)
        elif method == 'percent-':
            product['price'] *= (1 - param)

# Only for test product "Siding" -> updated product
# print(next(filter(lambda obj: obj.get('name') == 'Siding', dataPkl), None))

saveToPkl(pklFileName, dataPkl)