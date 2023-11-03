# Need to install msgpack (if you don't have yet)
# >> pip install msgpack
# or
# >> python3 -m pip install msgpack

import numpy as np
import msgpack
import os
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
    fileName = "products_12"
    openfile = open("assets/data/3/"+fileName+".json")
    
    allProducts = np.array(json.load(openfile))
    
    uniqueProductNameList = []
    
    for product in allProducts:
        if (product["name"] not in uniqueProductNameList):
            uniqueProductNameList.append(product["name"])
    
    data = []
    
    for productName in uniqueProductNameList:
        totalData = 0
        totalPrice = 0
        
        tempData = {
            "name": productName,
            "averagePrice": 0
        }
        
        for product in allProducts:
            if(productName == product["name"]):
                totalData += 1
                totalPrice += product["price"]
                
        tempData["averagePrice"] = totalPrice / totalData
        data.append(tempData)
    
    # print(data)
    
    # Serializing json
    json_object_original = json.dumps(data, indent=4, cls=NpEncoder)
    
    # Export the result to json
    with open("assets/output/3/"+fileName+"_output.json", "w") as outfile:
        outfile.write(json_object_original)
    
    # Export the result to msgpack
    with open("assets/output/3/"+fileName+"_output.msgpack", "wb") as outfile:
        packed = msgpack.packb(data)
        outfile.write(packed)
    
    # Get file size
    file_size_json = os.path.getsize("assets/output/3/"+fileName+"_output.json")
    print("File Size using (json) is :", file_size_json, "bytes")
    file_size_msgpack = os.path.getsize("assets/output/3/"+fileName+"_output.msgpack")
    print("File Size using (msgpack) is :", file_size_msgpack, "bytes")
    
    # Data output
    output = {
        "fileSizeJson": str(file_size_json) + " bytes",
        "fileSizeMsgpack": str(file_size_msgpack) + " bytes",
    }
    
    # Serializing json
    json_object_original = json.dumps(output, indent=4, cls=NpEncoder)
    
    # Export the result to json
    with open("assets/output/3/"+fileName+"_output_size.json", "w") as outfile:
        outfile.write(json_object_original)
except Exception as e:
    print(e)