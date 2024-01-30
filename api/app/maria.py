import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *

from datetime import datetime

from sqlalchemy import create_engine, text


class Maria :

    def __init__(self, test : bool) -> None:
        if test : 
            self.engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
        else : 
            self.engine = create_engine(SQLALCHEMY_DATABASE_URL)

    def reset_db(self, table) : 
        with self.engine.connect() as connection:
            query = text(f"DELETE FROM {table}")
            connection.execute(query) 
            connection.commit()

    # Item

    def create_item(self, id_code : str, brand: str, name: str, ingredient: str, allergen: str, nutriment: str, nutriscore: str, ecoscore: str, packaging: str, image: str, url_openfoodfact: str):
        with self.engine.connect() as connection:
            query = text("INSERT INTO item (id_code, brand, name, ingredient, allergen, nutriment, nutriscore, ecoscore, packaging, image, url_openfoodfact)"
                         " VALUES (:id_code, :brand, :name, :ingredient, :allergen, :nutriment, :nutriscore, :ecoscore, :packaging, :image, :url_openfoodfact)")
            connection.execute(query, {"id_code" : id_code, "brand": brand ,"name": name, "ingredient": ingredient,"allergen" : allergen, "nutriment" : nutriment, "nutriscore" : nutriscore, "ecoscore" : ecoscore, "packaging" : packaging, "image" : image, "url_openfoodfact" : url_openfoodfact}) 
            connection.commit()

    def get_item(self, id_code : str | None = None) : 
        with self.engine.connect() as connection:
            if id_code == None :
                with self.engine.connect() as connection:
                    query = text("SELECT * FROM item")
                    result = connection.execute(query, {"id_code" : id_code}) 
            else :
                    query = text(f"SELECT * FROM item WHERE id_code = :id_code")
                    result = connection.execute(query, {"id_code" : id_code}) 
        result = result.mappings().all()
        return result
    
    def update_item(self, id_code : str, brand: str, name: str, ingredient: str, allergen: str, nutriment: str, nutriscore: str, ecoscore: str, packaging: str, image: str, url_openfoodfact: str):
        with self.engine.connect() as connection:
            query = text("UPDATE item SET id_code=:id_code, brand=:brand, name=:name, ingredient=:ingredient, allergen=:allergen, nutriment=:nutriment, nutriscore=:nutriscore, ecoscore=:ecoscore, packaging=:packaging, image=:image, url_openfoodfact=:url_openfoodfact WHERE id_code=:id_code")
            connection.execute(query, {"id_code" : id_code, "brand": brand ,"name": name, "ingredient": ingredient,"allergen" : allergen, "nutriment" : nutriment, "nutriscore" : nutriscore, "ecoscore" : ecoscore, "packaging" : packaging, "image" : image, "url_openfoodfact" : url_openfoodfact}) 
            connection.commit()

    def delete_item(self, id_code : str | None = None):
        with self.engine.connect() as connection:
            if id_code == None :
                query = text("DELETE FROM item")
                connection.execute(query)
            else : 
                query = text("DELETE FROM item WHERE id_code=:id_code")
                connection.execute(query, {"id_code" : id_code})
            connection.commit()


    # User
           
    def create_user(self, username: str, last_name: str, first_name: str, age: int, gender: int):
        with self.engine.connect() as connection:
            query = text("INSERT INTO user (username, last_name, first_name, age, gender)"
                         " VALUES (:username, :last_name, :first_name, :age, :gender)")
            result = connection.execute(query, {"username": username ,"last_name": last_name, "first_name": first_name,"age" : age, "gender" : gender})
            connection.commit()
        return result

    def get_user(self, id_user : str | None = None):
        with self.engine.connect() as connection:
            if id_user == None :
                query = text("SELECT * FROM user")
                result = connection.execute(query)
            else :
                query = text(f"SELECT * FROM user WHERE id_user = :id_user")
                result = connection.execute(query, {"id_user" : id_user})

        result = result.mappings().all()
        return result


    def update_user(self, id_user : str, username: str, last_name: str, first_name: str, age: str, gender: str):
        with self.engine.connect() as connection:
            query = text("UPDATE user SET username=:username, last_name=:last_name, first_name=:first_name, age=:age, gender=:gender WHERE id_user = :id_user")
            connection.execute(query, {"username" : username, "last_name" : last_name, "first_name" : first_name, "age" : age, "gender" : gender, "id_user" :id_user})
            connection.commit()

    def delete_user(self, id_user : str | None = None):
        with self.engine.connect() as connection:
            if id_user == None :
                query = text("DELETE FROM user")
                connection.execute(query)
            else :
                query = text("DELETE FROM user WHERE id_user = :id_user")
                connection.execute(query, {"id_user" : id_user})
            connection.commit()

    
    # Place
            
    def create_place(self, name: str, adresse: str, postcode: str, city: str):
        with self.engine.connect() as connection:
            query = text("INSERT INTO place (name, adresse, postcode, city)"
                         " VALUES (:name, :adresse, :postcode, :city)")
            connection.execute(query, {"name": name ,"adresse": adresse, "postcode": postcode, "city" : city})
            connection.commit()

    def get_place(self, id_place : str | None = None):
        with self.engine.connect() as connection:
            if id_place == None :
                query = text("SELECT * FROM place")
                result = connection.execute(query) 
            else :
                query = text(f"SELECT * FROM place WHERE id_place = :id_place")
                result = connection.execute(query, {"id_place" : id_place}) 
            result = result.mappings().all()
            return result

    def update_place(self, id_place : str, name: str, adresse: str, postcode: str, city: str):
        with self.engine.connect() as connection:
            query = text("UPDATE place SET name = :name, adresse = :adresse, postcode =:postcode, city = :city WHERE id_place=:id_place")
            connection.execute(query, {"name" : name, "adresse" : adresse, "postcode" : postcode, "city" : city, "id_place" : id_place})
            connection.commit()

    def delete_place(self, id_place : str):
        with self.engine.connect() as connection:
            if id_place == None :
                query = text("DELETE FROM place")
                connection.execute(query)
            else :
                query = text("DELETE FROM place WHERE id_place = :id_place")
                connection.execute(query, {"id_place" : id_place})
            connection.commit()


    # Scan

    def create_scan(self, id_user : int, id_code : str, id_place : int ):
            date = datetime.now()
            year = date.year
            month = date.month
            day = date.day
            hour = date.hour
            minute = date.minute
            with self.engine.connect() as connection:
                query = text("INSERT INTO scan (id_user, id_code, id_place, date, year, month, day, hour, minute)"
                         "VALUES (:id_user, :id_code, :id_place, :date, :year, :month, :day, :hour, :minute)")
                connection.execute(query, {"id_user" : id_user, "id_code" : id_code, "id_place" : id_place, "date" : date, "year" : year, "month" : month, "day" : day, "hour" : hour, "minute" : minute})
                connection.commit()

    def get_scan(self, id_user : int | None = None):
        with self.engine.connect() as connection:
            if id_user == None :
                query = text("SELECT id_user, id_code, id_place, year, month, day, hour, minute FROM scan")
                result = connection.execute(query) 
            else :
                query = text(f"SELECT id_user, id_code, id_place, year, month, day, hour, minute FROM scan WHERE id_user = :id_user")
                result = connection.execute(query, {"id_user" : id_user}) 
            
            result = result.mappings().all()
            return result
            
    def delete_scan(self, id_user : str):
        with self.engine.connect() as connection:
            query = text("DELETE FROM scan WHERE id_user = :id_user")
            connection.execute(query, {"id_user" : id_user})
            connection.commit()