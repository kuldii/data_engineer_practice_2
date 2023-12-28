import numpy as np
import pickle
import msgpack
import csv
import json
import os
import statistics
from collections import Counter

def printSize(name, csvSize, jsonSize, msgpackSize, pklSize):
    print("================================")
    print(f'File {name} (csv): {csvSize} bytes')
    print(f'File {name} (json): {jsonSize} bytes')
    print(f'File {name} (msgpack): {msgpackSize} bytes')
    print(f'File {name} (pickle): {pklSize} bytes')

def getFileSize(file):
    return os.path.getsize(file)

def saveToCsv(name, data):
    with open("assets/output/5/resolved/"+name, mode='w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        header = data.keys()
        csvWriter.writerow(header)
        value = data.values()
        csvWriter.writerow(value)
        
def saveToPickle(name, data):
    with open("assets/output/5/resolved/"+name, "wb") as pklFile:
        pickle.dump(data, pklFile, protocol=pickle.HIGHEST_PROTOCOL)

def saveToPickle(name, data):
    with open("assets/output/5/resolved/"+name, "wb") as pklFile:
        pickle.dump(data, pklFile, protocol=pickle.HIGHEST_PROTOCOL)

def saveToMsgpack(name, data):
    with open("assets/output/5/resolved/"+name, "wb") as msgpackFile:
        packed = msgpack.packb(data)
        msgpackFile.write(packed)
        
def saveToJson(name, data):
    with open("assets/output/5/resolved/"+name, 'w') as jsonFile:
        jsonFile.write(data)
        
def countFrequency(collection):
    return Counter(collection)

def getDataJsonFile(name, ext):
    data = None
    with open("assets/data/5/"+name+ext, 'r') as jsonFile:
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

fileName = "animal-shelter-intakes-and-outcomes"
ext = ".json"

allData = getDataJsonFile(fileName, ext)

# Example data -> All Fields
# {'animal_id': 'A584130','animal_name': None, 'animal_type': 'CAT', 'primary_color': 'BLACK', 'secondary_color': 'WHITE', 'sex': 'Male', 'dob': '2016-12-05', 'age': 6.0, 'intake_date': '2017-01-05', 'intake_cond': 'UNDER AGE/WEIGHT', 'intake_type': 'STRAY', 'intake_subtype': 'OTC', 'reason': None, 'outcome_date': '2017-01-08', 'crossing': '7000 LIME AVE, CA 90805', 'jurisdiction': 'LONG BEACH', 'outcome_type': 'RESCUE', 'outcome_subtype': 'OTHER RESC', 'intake_is_dead': 'Alive on Intake','outcome_is_dead': 'FALSE', 'was_outcome_alive': 1}

# Example data -> Picked only 10 Fields
# {
#     'animal_id': 'A584130',
#     'animal_name': None, 
#     'animal_type': 'CAT', 
#     'primary_color': 'BLACK',
#     'secondary_color': 'WHITE', 
#     'sex': 'Male', 
#     'dob': '2016-12-05', 
#     'age': 6.0, 
#     'outcome_is_dead': 'FALSE', 
#     'was_outcome_alive': 1
# }

ages = [animal['age'] for animal in allData if animal["age"] != None]

statisticsAge = {
    "avgAge": statistics.mean(ages),
    "maxAge" : max(ages),
    "minAge" : min(ages),
    "stdevAge" : statistics.stdev(ages)
}

# Only for check
# print(statisticsAge)

categories = []
gender = []

for animal in allData:
    categories.append(animal["animal_type"])
    gender.append(animal["sex"])

categoryFreq = countFrequency(categories)
genderFreq = countFrequency(gender)

# Only for check
# print(categoryFreq)
# print(genderFreq)

statisticsAgeJsonResult = json.dumps(statisticsAge, indent=4, cls=NpEncoder)
categoryFreqJsonResult = json.dumps(categoryFreq, indent=4, cls=NpEncoder)
genderFreqJsonResult = json.dumps(genderFreq, indent=4, cls=NpEncoder)

# Save data to csv
saveToCsv("statistic_age.csv", statisticsAge)
saveToCsv("categories.csv", dict(categoryFreq))
saveToCsv("gender.csv", dict(genderFreq))

# Save data to json
saveToJson("statistic_age.json", statisticsAgeJsonResult)
saveToJson("categories.json", categoryFreqJsonResult)
saveToJson("gender.json", genderFreqJsonResult)

# Save data to msgpack
saveToMsgpack("statistic_age.msgpack", statisticsAgeJsonResult)
saveToMsgpack("categories.msgpack", categoryFreqJsonResult)
saveToMsgpack("gender.msgpack", genderFreqJsonResult)

# Save data to pkl
saveToPickle("statistic_age.pkl", statisticsAgeJsonResult)
saveToPickle("categories.pkl", categoryFreqJsonResult)
saveToPickle("gender.pkl", genderFreqJsonResult)


# Get file size of Statistic Age
csvSizeStatisticAge = getFileSize("assets/output/5/resolved/statistic_age.csv")
jsonSizeStatisticAge = getFileSize("assets/output/5/resolved/statistic_age.json")
msgpackSizeStatisticAge = getFileSize("assets/output/5/resolved/statistic_age.msgpack")
pklSizeStatisticAge = getFileSize("assets/output/5/resolved/statistic_age.pkl")

printSize("Statistic Age", csvSizeStatisticAge, jsonSizeStatisticAge, msgpackSizeStatisticAge, pklSizeStatisticAge)

# Get file size of Categories
csvSizeCategories = getFileSize("assets/output/5/resolved/categories.csv")
jsonSizeCategories = getFileSize("assets/output/5/resolved/categories.json")
msgpackSizeCategories = getFileSize("assets/output/5/resolved/categories.msgpack")
pklSizeCategories = getFileSize("assets/output/5/resolved/categories.pkl")

printSize("Categories", csvSizeCategories, jsonSizeCategories, msgpackSizeCategories, pklSizeCategories)

# Get file size of Gender
csvSizeGender = getFileSize("assets/output/5/resolved/gender.csv")
jsonSizeGender = getFileSize("assets/output/5/resolved/gender.json")
msgpackSizeGender = getFileSize("assets/output/5/resolved/gender.msgpack")
pklSizeGender = getFileSize("assets/output/5/resolved/gender.pkl")

printSize("Gender", csvSizeGender, jsonSizeGender, msgpackSizeGender, pklSizeGender)