from pymongo import MongoClient
from bson.objectid import ObjectId
from PIL import Image

import io
import logging
import datetime
import random
import re
import json
import shutil
import sys
import os

from app.config import *


class Mongo :

    log = logging.getLogger("log-auto")
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)   
    log.addHandler(file_handler)   

    def __init__(self, test : bool = True) -> None:
        self.client = MongoClient(f'mongodb://{user_mongo}:{pass_mongo}@{adresse_mongo}:{port_mongo}')
        self.db = self.client.ARMarket
        self.test = test
        if self.test :
            self.dataset_collection = self.db.dataset_test
        else :
            self.dataset_collection = self.db.dataset




    def img_to_byte(self, img):
        """ Convertion d'une image PIL en BYTES """
        imgbyte = io.BytesIO()
        img.save(imgbyte, format="png")
        image_file_size = imgbyte.tell()
        imgbyte = imgbyte.getvalue()

        return [imgbyte, image_file_size]
    

    
    def byte_to_img(self, imgbyte):
        """ Conversion des BYTES en image PIL"""
        imgbyte_io = io.BytesIO(imgbyte)
        image_pil = Image.open(imgbyte_io)
        return image_pil

    
    
    # API

    def get_dataset(self, id : int) : 
        """Compile les images et annotations au format yolo d'un dataset dans un dossier zipé."""
        # Réquête
        documents = self.dataset_collection.find({"dataset" : {"$elemMatch": {"$eq": id}}})

        if self.dataset_collection.count_documents({"dataset" : {"$elemMatch": {"$eq": id}}}) == 0 :
            # mauvais id
            return False

        # Création d'un dossier structuré
        current_datetime = datetime.datetime.now()
        folder_name = f"dataset_{id}_{current_datetime.strftime('%Y%m%d_%H%M%S')}"
        saving_path = os.path.join("app","temp",folder_name)
        os.makedirs(saving_path, exist_ok=True)
        for doc in documents:
            # Enregistrement de l'image
            img = self.byte_to_img(doc["img"])
            img.save(os.path.join(saving_path,f"{doc['name']}.png"))
            
            # Enregistrement du fichier d'annotation
            training_data = doc["training_data"]
            #labels = [i for i in doc.keys() if re.search("^label" , i)]
            with open(os.path.join(saving_path,f"{doc['name']}.txt"), "w") as txt :
                for i in training_data :
                    txt.write(f"{i['label_int']} {i['bounding_box'][0]} {i['bounding_box'][1]} {i['bounding_box'][2]} {i['bounding_box'][3]} \n")
        
        # Transformation en zip
        shutil.make_archive(os.path.join(saving_path), 'zip', saving_path)
        self.log.info(f"API : download dataset with dataset_id : {id}")
        path_zip_file = os.path.join("app","temp",f"{folder_name}.zip")
        return path_zip_file

    def remove_temp_get_dataset(self) :
        temp_path = os.path.join("app","temp") 
        files = os.listdir(temp_path)
        for i in files :
            path = os.path.join(temp_path,i)
            if os.path.isdir(path) : 
                shutil.rmtree(path)
            else : 
                os.remove(path)


       

    def set_img(self,img : bytes, annotation : bytes, dataset_id : list, dataset_extraction : str, pretreatment : bool, data_augmentation: bool):
        """ 
        post /dataset/frame
        Enregistre les images qui on eu une détection et les métadonnées :
        "date" : "[date JJMMYYYY] Date de l'insertion du document",
        "id" : "[int] Id de l'image / collection",
        "img" : "[bin] Image",
        "name" : "[str] Nom de l'image format [from(dataset)_rand(10).jpg]",
        "size" : "[int] Taille de l'image en Mo",
        "pre-treatment" : "[bool] Si l'image a été pré-traitée",
        "data_augmentation" : "[bool] Si l'image est issue d'une data augmentation",
        "dataset" : "[list] Liste des datasets auquel l'image appartient",
        "training_data" :
            [
                {
                    "label" : "[str] Label associé à l'image",
                    "label_int" : "[int] Label associé à l'image sous forme d'integer unique avec table de correspondance dans label.json",
                    "bounding box" : "[list] Liste des bounding box au format xywhn"
                },
                {
                    "label" : "[str] Label associé à l'image",
                    "label_int" : "[int] Label associé à l'image sous forme d'integer unique avec table de correspondance dans label.json",
                    "bounding box" : "[list] Liste des bounding box au format xywhn"
                }
            ]
        """

        # Création du document
        new_document = {}

        # "date" : "[date YYYYMMDD] Date de l'insertion du document"
        new_document["date"] = datetime.datetime.today().strftime('%Y-%m-%d')

        # "id" : "[int] Id de l'image / collection"
        # Créé automatiquement "_id"

        # "img" : "[bin] Image"
        #imgbyte = self.img_to_byte(img)
        new_document["img"] = img
        # "size" : "[int] Taille de l'image en Mo"
        new_document["size"] = sys.getsizeof(img)

        # "name" : "[str] Nom de l'image format [from(dataset d'extraction)_rand(10).jpg]"
        new_document["name"] = f"{dataset_extraction}_{random.randint(1000000000,9999999999)}"


        # "pre-treatment" : "[bool] Si l'image a été pré-traitée",
        new_document["pre_treatment"] = pretreatment

        # "data_augmentation" : "[bool] Si l'image est issue d'une data augmentation",
        new_document["data_augmentation"] = data_augmentation

        # "dataset" : "[list] Liste des datasets auquel l'image appartient"
        new_document["dataset"] = dataset_id

        # "training_data" : list de dict contenant label, label int, bb de chaque détection de l'image
        # input est un une list contenant un json pré formaté avant l'envoie à l'API pour correspondre au format attendu par yolo. 
        annotation = annotation.decode("utf-8")
        annotation = json.loads(annotation)
        
        new_document["training_data"] = annotation

        
        # Insertion en base
        self.dataset_collection.insert_one(new_document)
        self.log.info(f"API : frame set in dataset{'_test' if self.test else ''} collection - dataset_id : {dataset_id}")
        

    def update_frame(self, id : str, query : dict):
        """
        Met à jour une frame via son id.
        query = "key premier niveau" : value
        "key premier niveau = date, img, name, size, pre-trement, data_aumentation, dataset, training_data.
        """


        self.dataset_collection.update_one(
            {"_id" :  ObjectId(id)},
            {"$set" : query}
        )
        self.dataset_collection.update_one(
            {"_id" :  ObjectId(id)},
            {"$set" : {"update_date" : datetime.datetime.today().strftime('%Y-%m-%d')}}
            )
        self.log.info(f"API : frame {id} updated in dataset{'_test' if self.test else ''} collection with {query}")
        



    def delete_frame(self, id : str) : 
        query = {"_id" :  ObjectId(id)}
        nb_response = self.dataset_collection.count_documents(query)
        if nb_response > 0 :
            document = self.dataset_collection.find_one(query)
            self.dataset_collection.delete_one(query)
            self.log.info(f"API : frame {id} deleted from dataset{'_test' if self.test else ''} collection. Dataset : {document['_id']}.")

        return nb_response


    def reset_db(self):
        """Efface la base de donnée sélectionnée (dataset ou dataset_test)"""

        self.dataset_collection.delete_many({})
        logging.info(f"La collection dataset{'_test' if self.test else ''} a été vidée de ses documents")
        

        

        

if __name__ == "__main__" : 
    Mongo_test = Mongo()
    # Mongo_test.test()
    Mongo_test.reset_db(test=False)


