import os
import re

from app.mongo import Mongo
from bson.objectid import ObjectId

def test_get_dataset(binary_annotation, binary_annotation_1, binary_img, binary_img_1):
    
    mongo = Mongo(test = True)
    
    # Ajout de deux images

    mongo.reset_db()
    mongo.set_img(binary_img, binary_annotation, dataset_id =[0], dataset_extraction = "ARM", pretreatment = False, data_augmentation = False)
    mongo.set_img(binary_img_1, binary_annotation_1, dataset_id = [0], dataset_extraction = "ARM", pretreatment = True, data_augmentation = True)
    res = mongo.dataset_collection.count_documents({})
    assert res == 2

    # export zip
    zip = mongo.get_dataset(0)

    # Il existe à la suite de get_dataset deux fichiers dans temp, un dossier et son archive
    temp_file = os.listdir(os.path.join("app","temp"))

    #Dossier non vide
    assert len(os.listdir(os.path.join("app","temp",temp_file[0]))) > 0
    # Il existe un fichier zip
    assert temp_file[1][-3:] == "zip"
    
    # Suppression du contenu de temp
    mongo.remove_temp_get_dataset()
    assert len(os.listdir(os.path.join("app","temp"))) == 0

    mongo.client.close()


def test_set_img(binary_annotation, binary_img):

    mongo = Mongo(test = True)

    mongo.reset_db()
    mongo.set_img(binary_img, binary_annotation, dataset_id =0, dataset_extraction = "ARM", pretreatment = False, data_augmentation = False)
    res = mongo.dataset_collection.count_documents({})

    assert res == 1 

    mongo.client.close()

    


def test_update_frame():

    mongo = Mongo(test = True)

    res = mongo.dataset_collection.find_one({})
    docs = mongo.dataset_collection.count_documents({})

    assert docs == 1
    assert res["data_augmentation"] == False

    id = str(res["_id"])
    mongo.update_frame(id=id, query={"data_augmentation" : True})

    res_updated = mongo.dataset_collection.find_one({"_id": ObjectId(id)})

    assert res_updated["data_augmentation"] == True 
    
    mongo.client.close()


def test_delete_frame():

    mongo = Mongo(test = True)

    docs = mongo.dataset_collection.count_documents({})
    assert docs == 1

    res = mongo.dataset_collection.find_one({})

    id = str(res["_id"])
    mongo.delete_frame(id=id)

    docs = mongo.dataset_collection.count_documents({})
    assert docs == 0

    mongo.client.close()

