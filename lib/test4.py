import numpy as np
import json
import pickle

try:
    # Open file
    jsonFileName = "price_info_12"
    pklFileName = "products_12"
    openFileJson = open("assets/data/4/"+jsonFileName+".json")
    
    with open("assets/data/4/"+pklFileName+".pkl", "rb") as openFilePkl:
        allProducts = pickle.load(openFilePkl)
        priceInfo = np.array(json.load(openFileJson))
        
        print(allProducts[0])
        
        for product in allProducts:
            for info in priceInfo:
                if(product["name"] == info["name"]):
                    if(info["method"] == "add"):
                        product["price"] = product["price"] + info["param"]
                    elif(info["method"] == "sub"):
                        product["price"] = product["price"] - info["param"]
                    elif(info["method"] == "percent+"):
                        product["price"] = product["price"] * (1 + info["param"])
                    elif(info["method"] == "percent-"):
                        product["price"] = product["price"] * (1 - info["param"])
        
        with open("assets/output/4/"+pklFileName+"_new_price.pkl", "wb") as writeFilePkl:
            pickle.dump(allProducts, writeFilePkl, protocol=pickle.HIGHEST_PROTOCOL)
            
    with open("assets/output/4/"+pklFileName+"_new_price.pkl", "rb") as openNewFilePkl:
        allProductsNewPrice = pickle.load(openNewFilePkl)
        
        print(allProductsNewPrice[0])
except Exception as e:
    print(e)