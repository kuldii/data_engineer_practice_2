from datetime import datetime
import numpy as np
import pickle
import msgpack
import csv
import json
import os

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
    fileName = "animal-shelter-intakes-and-outcomes"
    openfile = open("assets/data/5/"+fileName+".json")
    
    allAnimals = np.array(json.load(openfile))
    
    # print(len(allAnimals)) # 40440 animals
    
    # print(allAnimals[1000]) # Example
    # {
    #     'animal_id': 'A506699',
    #     'animal_name': 'PUMPKIN',
    #     'animal_type': 'CAT',
    #     'primary_color': 'CALICO',
    #     'secondary_color': None,
    #     'sex': 'Female',
    #     'dob': '2009-09-09',
    #     'age': 14.0,
    #     'intake_date': '2017-06-09',
    #     'intake_cond': 'NORMAL',
    #     'intake_type': 'OWNER SURRENDER',
    #     'intake_subtype': 'OTC',
    #     'reason': 'MOVE',
    #     'outcome_date': '2017-06-24',
    #     'crossing': '3500 BLK OLEANDER ST, SEAL BEACH, CA 90740',
    #     'jurisdiction': 'SEAL BEACH',
    #     'outcome_type': 'ADOPTION',
    #     'outcome_subtype': 'REMOTE EVT',
    #     'intake_is_dead': 'Alive on Intake',
    #     'outcome_is_dead': 'FALSE',
    #     'was_outcome_alive': 1
    # }
    
    allCategories = []
    
    for animal in allAnimals:
        if(animal["animal_type"] not in allCategories):
            allCategories.append(animal["animal_type"])
    
    outputCategories = []
    
    for category in allCategories:
        total = 0
        totalFemale = 0
        totalMale = 0
        totalUnknownGender = 0
        totalDataHaveAge = 0
        totalValueAge = 0
        totalUnknownAge = 0
        maxAge = 0
        minAge = 99999
        allAgesNoNone = []
        nameOfAnimals = []
        dataAnimal = []
        
        for animal in allAnimals:
            if(animal["animal_type"] == category):
                total += 1
                if(animal["animal_name"] not in nameOfAnimals):
                    nameOfAnimals.append(animal["animal_name"])
                    totalUnknownAgeAnimal = 0
                    maxAgeAnimal = 0
                    minAgeAnimal = 99999
                    
                    if(animal["age"] == None):
                        totalUnknownAgeAnimal = 1
                    else:
                        
                        if(animal["age"] > maxAgeAnimal):
                            maxAgeAnimal = animal["age"]
                        if(animal["age"] < minAgeAnimal):
                            minAgeAnimal = animal["age"]
                        
                    dataAnimal.append({
                        "name": animal["animal_name"],
                        "totalAnimals": 1,
                        "totalUnknownAge": totalUnknownAgeAnimal,
                        "maximumAge": maxAgeAnimal,
                        "minimumAge": minAgeAnimal,
                    })
                else:
                    for data in dataAnimal:
                        if(data["name"] == animal["animal_name"]):
                            data["totalAnimals"] += 1
                            if(animal["age"] == None):
                                data["totalUnknownAge"] += 1
                            else:
                                if(animal["age"] > data["maximumAge"]):
                                    data["maximumAge"] = animal["age"]
                                if(animal["age"] < data["minimumAge"]):
                                    data["minimumAge"] = animal["age"]
                
                if(animal["sex"] == "Female"):
                    totalFemale += 1
                elif(animal["sex"] == "Male"):
                    totalMale += 1
                else:
                    totalUnknownGender += 1
                        
                if(animal["age"] == None):
                    totalUnknownAge += 1
                else:
                    totalDataHaveAge += 1
                    totalValueAge += animal["age"]
                    allAgesNoNone.append(animal["age"])
                    if(animal["age"] > maxAge):
                        maxAge = animal["age"]
                    if(animal["age"] < minAge):
                        minAge = animal["age"]
        
        averageAge = totalValueAge / totalDataHaveAge
        standartDeviationOfAge = np.std(allAgesNoNone)
        outputCategories.append({
            "category": category,
            "totalAnimals": total,
            "totalMale": totalMale,
            "totalFemale": totalFemale,
            "totalUnknownGender": totalUnknownGender,
            "totalUnknownAge": totalUnknownAge,
            "maximumAge": maxAge,
            "minimumAge": minAge,
            "averageAge": averageAge,
            "standartDeviationOfAge": standartDeviationOfAge,
            "animals": dataAnimal,
        })       
    
    # Export the result to csv
    with open("assets/output/5/output_categories.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(outputCategories)
        
    # Export the result to json
    with open("assets/output/5/output_categories.json", "w") as outfile:
        jsonOutputCategories = json.dumps(outputCategories, indent=4, cls=NpEncoder)
        outfile.write(jsonOutputCategories)
    
    # Export the result to pkl
    with open("assets/output/5/output_categories.pkl", "wb") as outfile:
        pickle.dump(outputCategories, outfile, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Export the result to msgpack
    with open("assets/output/5/output_categories.msgpack", "wb") as outfile:
        packed = msgpack.packb(outputCategories)
        outfile.write(packed)
    
    # Get file size
    file_size_csv = os.path.getsize("assets/output/5/output_categories.csv")
    print("File Size using (csv) is :", file_size_csv, "bytes")
    file_size_json = os.path.getsize("assets/output/5/output_categories.json")
    print("File Size using (json) is :", file_size_json, "bytes")
    file_size_pkl = os.path.getsize("assets/output/5/output_categories.pkl")
    print("File Size using (pkl) is :", file_size_pkl, "bytes")
    file_size_msgpack = os.path.getsize("assets/output/5/output_categories.msgpack")
    print("File Size using (msgpack) is :", file_size_msgpack, "bytes")
except Exception as e:
    print(e)