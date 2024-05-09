import os
import json

from fastapi.testclient import TestClient

from app.main import app, maria_connect
from app.maria import Maria
from config import API_KEYS

from app.logger import log


client = TestClient(app)

def override_maria():
    return Maria(True)


app.dependency_overrides[maria_connect] = override_maria


headers = {'X-API-Key': list(API_KEYS.keys())[0]}



def test_api_key():

    response = client.get("/")
    assert response.status_code == 403

    response = client.get("/", headers=headers)
    assert response.status_code == 200

    assert response.json() == {"Hello": "World"}
    




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

def test_auth() :

    data = {"email" : "ad@min.fr",
            "password" : "pass"}
    
    res = client.post(f"/authenticate/", data=data, headers=headers)
    res = res.json()
    assert res["success"] == True

def test_log() :
    res = client.get(f"/logs/api-ia", headers=headers)
    log.debug(res)
    assert res.status_code == 200
    res = res.json()
    log.debug(res)

