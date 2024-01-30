import os

from fastapi.testclient import TestClient
from bson.objectid import ObjectId

from app.main import app, mongo_connect, maria_connect
from app.mongo import Mongo
from app.maria import Maria
from config import API_KEYS


client = TestClient(app)

def override_maria():
    return Maria(True)


def override_mongo():
    return Mongo(True)


app.dependency_overrides[mongo_connect] = override_mongo
app.dependency_overrides[maria_connect] = override_maria


headers = {'X-API-Key': list(API_KEYS.keys())[0]}



def test_api_key():

    response = client.get("/")
    assert response.status_code == 403

    response = client.get("/", headers=headers)
    assert response.status_code == 200

    assert response.json() == {"Hello": "World"}
    



def test_get_dataset(binary_annotation, binary_metadata, binary_annotation_1):

    mongo = Mongo(test = True)

    # Ajout de 2 frames
    
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response1 = client.post("/dataset/frames/", files = files, headers=headers)

    assert response1.status_code == 200

    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation_1), ("files" , binary_metadata)]
    response2 = client.post("/dataset/frames/", files = files, headers=headers)

    assert response2.status_code == 200

    # Téléchargement
    response = client.get("/dataset/0", headers=headers)
    assert response.status_code == 200

    # Récupérer le zip
    print(response)
    with open(os.path.join("app","dataset_0.zip"), "wb") as zip:
        zip.write(response.content)

    assert "dataset_0.zip" in os.listdir("app")

    # Supprimer le zip
    os.remove(os.path.join("app","dataset_0.zip"))
    assert "dataset_0.zip" not in os.listdir("app")

    # Supprimer le contenu de temp
    mongo.remove_temp_get_dataset()

    mongo.client.close()



def test_add_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 200

    # Image n'est pas un jpg, png, etc. 
    mongo.reset_db()
    img = open("app/tests/sample/test.txt","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 405

    # Array n'a pas 3 éléments
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 405
    assert response.json() == {"error": "array must have 3 binaries elements"}

    mongo.client.close()


def test_update_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]


    response = client.post("/dataset/frames/", files = files, headers=headers)
    assert response.status_code == 200

    res = mongo.dataset_collection.find_one({})
    assert res["data_augmentation"] == False 

    # Modification de data_augmentation
    id_init = (res["_id"]) 
    id = str(res["_id"]) 
    pp = ObjectId(id)
    assert id_init == pp 

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 200

    res_updated = mongo.dataset_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 

    # Multi modification

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True,
                   "pre_treatment" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 200

    res_updated = mongo.dataset_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 
    assert res_updated["pre_treatment"] == True 


    # Cas où le champ de query n'existe pas

    update = {
        "id" : id,
        "query" : {"data_augment" : True},
        "test" : True
    }

    response = client.put("/dataset/frames/", json = update, headers=headers)
    assert response.status_code == 405

    mongo.client.close()


def test_delete_frame(binary_annotation, binary_metadata):

    mongo = Mongo(test = True)

    # Ajout d'un frame
    mongo.reset_db()
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frames/", files = files, headers=headers)

    assert response.status_code == 200

    # Suprression 
    res = mongo.dataset_collection.find_one({})

    nb =  mongo.dataset_collection.count_documents({})
    assert nb == 1

    id = res["_id"]
    response = client.delete(f"/dataset/frames/{id}", headers=headers)

    nb =  mongo.dataset_collection.count_documents({})

    assert nb == 0
    assert response.status_code == 200


    # Bad id 

    response = client.delete(f"/dataset/frames/000111125478541154555255", headers=headers)
    assert response.status_code == 405

    response = client.delete(f"/dataset/frames/00011", headers=headers)
    assert response.status_code == 405

    mongo.client.close()




def test_record_item(item):
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("item")

    # Transormation type
    item["ingredient"] = str(item["ingredient"])
    item["allergen"] = str(item["allergen"])
    item["nutriment"] = str(item["nutriment"])
    item["nutriscore"] = str(item["nutriscore"])
    item["ecoscore"] = str(item["ecoscore"])
    item["packaging"] = str(item["packaging"])

    response = client.post(f"/items/", json=item, headers=headers)
    print(response.json())
    assert response.status_code == 200

def test_delete_item(item) : 

    # Create item
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("item")

    # Transormation type
    item["ingredient"] = str(item["ingredient"])
    item["allergen"] = str(item["allergen"])
    item["nutriment"] = str(item["nutriment"])
    item["nutriscore"] = str(item["nutriscore"])
    item["ecoscore"] = str(item["ecoscore"])
    item["packaging"] = str(item["packaging"])

    response = client.post(f"/items/", json=item, headers=headers)
    assert response.status_code == 200

    response = client.get(f"/items/{item['id_code']}", headers=headers)
    print(response.json())
    print(type(response.json()))
    assert response.status_code == 200

    response = client.delete(f"/items/{item['id_code']}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/items/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

    
def test_update_item(item, item2) : 

    # Create item
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("item")

    # Transormation type
    item["ingredient"] = str(item["ingredient"])
    item["allergen"] = str(item["allergen"])
    item["nutriment"] = str(item["nutriment"])
    item["nutriscore"] = str(item["nutriscore"])
    item["ecoscore"] = str(item["ecoscore"])
    item["packaging"] = str(item["packaging"])

    item2["ingredient"] = str(item2["ingredient"])
    item2["allergen"] = str(item2["allergen"])
    item2["nutriment"] = str(item2["nutriment"])
    item2["nutriscore"] = str(item2["nutriscore"])
    item2["ecoscore"] = str(item2["ecoscore"])
    item2["packaging"] = str(item2["packaging"])

    response = client.post(f"/items/", json=item, headers=headers)
    assert response.status_code == 200

    response = client.get(f"/items/{item['id_code']}", headers=headers)
    assert response.status_code == 200
    res = response.json()
    assert res[0]["brand"] == "Ferero"

    response = client.put(f"/items/", json=item2, headers=headers)
    assert response.status_code == 200

    response = client.get(f"/items/{item['id_code']}", headers=headers)
    assert response.status_code == 200
    res = response.json()
    assert res[0]["brand"] == "Barilla"

    response = client.delete(f"/items/{item['id_code']}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/items/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_users(user, user2):
     # Create item
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("user")

    # Transormation type
    user["age"] = str(user["age"])
    user["gender"] = str(user["gender"])


    user2["age"] = str(user2["age"])
    user2["gender"] = str(user2["gender"])
 
 
    response = client.post(f"/users/", json=user, headers=headers)
    assert response.status_code == 200
    response = client.post(f"/users/", json=user2, headers=headers)
    assert response.status_code == 200

    response = client.get(f"/users/", headers=headers)
    print(response.json())
    assert response.status_code == 200
    res = response.json()
    assert len(res) == 2

    print(res)


def test_user(user, user2) : 

    # Create item
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("user")

    # Transormation type
    user["age"] = str(user["age"])
    user["gender"] = str(user["gender"])


    user2["age"] = str(user2["age"])
    user2["gender"] = str(user2["gender"])
 
 
    response = client.post(f"/users/", json=user, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/users/", headers=headers)
    assert response.status_code == 200
    print(response.json())
    res = response.json()
    assert res[0]["username"] == "raiden"
    id = res[0]["id_user"]
    print(id)

    response = client.put(f"/users/{id}", json=user2, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/users/{id}", headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert res[0]["username"] == "juju"

    response = client.get(f"/users/", headers=headers)
    assert response.status_code == 200
    print(response.json())

    response = client.delete(f"/users/{id}", headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/users/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_place(place, place2) : 

    # Create item
    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("place")

    response = client.post(f"/places/", json=place, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/places/", headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert res[0]["city"] == "Dijon"
    id = res[0]["id_place"]
    print(id)

    response = client.put(f"/places/{id}", json=place2, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/places/{id}", headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert res[0]["city"] == "Lyon"

    response = client.get(f"/places/", headers=headers)
    assert response.status_code == 200
    print(response.json())

    response = client.delete(f"/places/{id}", headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/places/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_scan(place, item, user) : 

    mr = Maria(test=True)
    mr.reset_db("scan")
    mr.reset_db("user")
    mr.reset_db("item")
    mr.reset_db("place")


    # create primary keys

    item["ingredient"] = str(item["ingredient"])
    item["allergen"] = str(item["allergen"])
    item["nutriment"] = str(item["nutriment"])
    item["nutriscore"] = str(item["nutriscore"])
    item["ecoscore"] = str(item["ecoscore"])
    item["packaging"] = str(item["packaging"])

    response = client.post(f"/items/", json=item, headers=headers)
    assert response.status_code == 200

    user["age"] = str(user["age"])
    user["gender"] = str(user["gender"])
 
    response = client.post(f"/users/", json=user, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.post(f"/places/", json=place, headers=headers)
    print(response.json())
    assert response.status_code == 200


    # retrieve id 

    id_code = item["id_code"]

    response = client.get(f"/users/", headers=headers)
    assert response.status_code == 200
    print(response.json())
    res = response.json()
    id_user = res[0]["id_user"]
    print("user_id : ", id_user, " type : " , type(id_user))

    response = client.get(f"/places/", headers=headers)
    res = response.json()
    assert response.status_code == 200
    id_place = res[0]["id_place"]
    print("id_place : ", id_place, " type : " , type(id_place))

    scan = {}
    scan["id_code"] = id_code
    scan["id_place"] = id_place
    scan["id_user"] = id_user
    scan["test"] = True

    scan2 = {}
    scan2["id_user"] = id_user
    scan2["test"] = True




    # scan

    response = client.post(f"/scan/", json=scan, headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/scan/", params=scan2, headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert res[0]["id_user"] == id_user
    assert res[0]["id_code"] == id_code
    assert res[0]["id_place"] == id_place

    response = client.get(f"/scan/", headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert res[0]["id_user"] == id_user
    assert res[0]["id_code"] == id_code
    assert res[0]["id_place"] == id_place

    response = client.delete(f"/scan/?id={id_user}", headers=headers)
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/scan/", headers=headers)
    print(response.json())
    res = response.json()
    assert response.status_code == 200
    assert len(res) == 0

    response = client.delete(f"/items/{id_code}", headers=headers)
    assert response.status_code == 200

    response = client.delete(f"/users/{id_user}", headers=headers)
    assert response.status_code == 200

    response = client.delete(f"/places/{id_place}", headers=headers)
    assert response.status_code == 200