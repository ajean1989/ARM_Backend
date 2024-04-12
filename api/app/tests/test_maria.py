from datetime import datetime

from app.maria import Maria

def test_create_item(item):
    mr = Maria(test=True)

    # test rest
    mr.reset_db("scan") #  reset scan avant car contrainte de clé étrangère
    mr.reset_db("item")
    result = mr.get_item()
    assert len(result) == 0 





    # Item
    mr.create_item(
        item["id_code"],
        item["brand"], 
        item["name"], 
        str(item["ingredient"]), 
        str(item["allergen"]), 
        str(item["nutriment"]), 
        str(item["nutriscore"]),
        str(item["ecoscore"]),
        str(item["packaging"]),
        item["image"],
        item["url_openfoodfact"])
    
    # Test get    
    result = mr.get_item(item["id_code"])
    assert len(result) == 1 

    # Clean de la base
    mr.reset_db("item")
    result = mr.get_item()
    assert len(result) == 0 

def test_update_item(item, item2) :
    mr = Maria(test=True)

    # test rest
    mr.reset_db("item")
    result = mr.get_item()
    assert len(result) == 0

    # Test create
    mr.create_item(
        item["id_code"],
        item["brand"], 
        item["name"], 
        str(item["ingredient"]), 
        str(item["allergen"]), 
        str(item["nutriment"]), 
        str(item["nutriscore"]),
        str(item["ecoscore"]),
        str(item["packaging"]),
        item["image"],
        item["url_openfoodfact"])
    
    mr.update_item(
        item2["id_code"],
        item2["brand"], 
        item2["name"], 
        str(item2["ingredient"]), 
        str(item2["allergen"]), 
        str(item2["nutriment"]), 
        str(item2["nutriscore"]),
        str(item2["ecoscore"]),
        str(item2["packaging"]),
        item2["image"],
        item2["url_openfoodfact"])
    
    # Test get    
    result = mr.get_item(item["id_code"])
    assert len(result) == 1 

    
    assert dict(result[0])["brand"] == "Barilla"
    assert dict(result[0])["id_code"] == "3017620422003"

    # Test delete
    mr.delete_item(dict(result[0])["id_code"])

    result = mr.get_item()
    assert len(result) == 0





# user

def test_create_user(user):
    mr = Maria(test=True)

    # test rest
    mr.reset_db("scan") #  reset scan avant car contrainte de clé étrangère
    mr.reset_db("user")
    result = mr.get_item()
    assert len(result) == 0 

    # Test create
    mr.create_user(
        user["username"],
        user["last_name"], 
        user["first_name"], 
        user["age"], 
        user["gender"])

    # Test get    
    result = mr.get_user()
    assert len(result) == 1 

    # Clean de la base
    mr.reset_db("user")
    result = mr.get_user()
    assert len(result) == 0 


def test_update_user(user, user2) :
    mr = Maria(test=True)

    # test rest
    mr.reset_db("user")
    result = mr.get_user()
    assert len(result) == 0

    # Test create
    mr.create_user(
        user["username"],
        user["last_name"], 
        user["first_name"], 
        user["age"], 
        user["gender"])
    
    result = mr.get_user()
    assert len(result) == 1
    id_user = dict(result[0])["id_user"]
    
    mr.update_user(
        id_user,
        user2["username"],
        user2["last_name"], 
        user2["first_name"], 
        user2["age"], 
        user2["gender"])
    
    # Test get    
    result = mr.get_user()
    assert len(result) == 1 
    
    assert dict(result[0])["username"] == "juju"

    # Test delete
    mr.delete_user(dict(result[0])["id_user"])

    result = mr.get_user()
    assert len(result) == 0


# place
    
def test_create_place(place):
    mr = Maria(test=True)

    # test rest
    mr.reset_db("scan") #  reset scan avant car contrainte de clé étrangère
    mr.reset_db("place")
    result = mr.get_item()
    assert len(result) == 0 

    # Test create
    mr.create_place(
        place["name"],
        place["adresse"], 
        place["postcode"], 
        place["city"])

    # Test get    
    result = mr.get_place()
    assert len(result) == 1 

    # Clean de la base
    mr.reset_db("place")
    result = mr.get_place()
    assert len(result) == 0 


def test_update_place(place, place2) :
    mr = Maria(test=True)

    # test rest
    mr.reset_db("scan") #  reset scan avant car contrainte de clé étrangère
    mr.reset_db("place")
    result = mr.get_place()
    assert len(result) == 0

    # Test create
    mr.create_place(
        place["name"],
        place["adresse"], 
        place["postcode"], 
        place["city"])
    
    result = mr.get_place()
    assert len(result) == 1
    id_place = dict(result[0])["id_place"]
    
    mr.update_place(
        id_place,
        place2["name"],
        place2["adresse"], 
        place2["postcode"], 
        place2["city"])
    
    # Test get    
    res = mr.get_place()
    assert len(res) == 1 
    
    assert dict(res[0])["city"] == "Lyon"

    # Test delete
    mr.delete_place(dict(res[0])["id_place"])

    result = mr.get_place()
    assert len(result) == 0



# Scan
    
def test_scan(place, item, user):
    mr = Maria(test=True)

    # reset
    mr.reset_db("scan")
    result = mr.get_scan()
    assert len(result) == 0

    # create primary keys

    mr.reset_db("place")
    mr.reset_db("item")
    mr.reset_db("user")

    mr.create_place(
        place["name"],
        place["adresse"], 
        place["postcode"], 
        place["city"])
    
    mr.create_user(
        user["username"],
        user["last_name"], 
        user["first_name"], 
        user["age"], 
        user["gender"])
    
    mr.create_item(
        item["id_code"],
        item["brand"], 
        item["name"], 
        str(item["ingredient"]), 
        str(item["allergen"]), 
        str(item["nutriment"]), 
        str(item["nutriscore"]),
        str(item["ecoscore"]),
        str(item["packaging"]),
        item["image"],
        item["url_openfoodfact"])

    user_res = mr.get_user()
    id_user = dict(user_res[0])["id_user"]

    place_res = mr.get_place()
    id_place = dict(place_res[0])["id_place"]

    # create
    mr.create_scan(
        id_user,
        item["id_code"], 
        id_place)
    
    result = mr.get_scan()
    assert len(result) == 1

    # tests
    day = dict(result[0])["day"] 
    month = dict(result[0])["month"] 
    year = dict(result[0])["year"] 

    date = datetime.now()

    assert day == date.day 
    assert month == date.month 
    assert year == date.year 

    # delete
    mr.delete_scan(
        id_user)

    result = mr.get_scan()
    assert len(result) == 0

    mr.reset_db("place")
    mr.reset_db("item")
    mr.reset_db("user")

def test_authenticate():
    mr = Maria(test=True)

    res = mr.authenticate("ad@min.fr")
    print(res)
    assert res["email"] == "ad@min.fr"

