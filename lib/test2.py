import numpy as np
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
    fileName = "matrix_12_2"
    dataMatrix = np.load("assets/data/2/"+fileName+".npy")
    
    # Initial Variable
    x = []
    y = []
    z = []
    
    for i in range(len(dataMatrix)):
        dataRow = dataMatrix[i]
        for j in range(len(dataRow)):
            if(dataRow[j] > (500 + 12)):
                x.append(i)
                y.append(j)
                z.append(dataRow[j])
                
    data = np.array([x,y,z])
    
    # Save with np.savez()
    np.savez("assets/output/2/"+fileName+".npz", data)
    # Save with np.savez_compressed()
    np.savez_compressed("assets/output/2/"+fileName+"_compressed.npz", data)
    
    # Get file size
    file_size_savez = os.path.getsize("assets/output/2/"+fileName+".npz")
    print("File Size using (savez) is :", file_size_savez, "bytes")
    file_size_savez_compressed = os.path.getsize("assets/output/2/"+fileName+"_compressed.npz")
    print("File Size using (savez_compressed) is :", file_size_savez_compressed, "bytes")
    
    # Data output
    output = {
        "fileSizeSavez": str(file_size_savez) + " bytes",
        "fileSizeSavezCompressed": str(file_size_savez_compressed) + " bytes",
    }
    
    # Serializing json
    json_object_original = json.dumps(output, indent=4, cls=NpEncoder)
    
    # Export the result to json
    with open("assets/output/2/"+fileName+"_output.json", "w") as outfile:
        outfile.write(json_object_original)
        
except Exception as e:
    print(e)