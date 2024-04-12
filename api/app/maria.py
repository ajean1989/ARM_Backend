import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

from app.config import *
from app.log import Logg


class Maria :

    def __init__(self, test : bool) -> None:
        self.test = test
        if test : 
            self.engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
        else : 
            self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        
        self.engine_app = create_engine(SQLALCHEMY_DATABASE_APP)
        
        log = Logg()
        self.log_debug = log.set_log_api_backend_debug()

    def reset_db(self, table) : 
        try : 
            with self.engine.connect() as connection:
                query = text(f"DELETE FROM {table}")
                connection.execute(query) 
                connection.commit()
            self.log_debug.info(f"Reset de la base de données {'test' if self.test else 'de production'}")
        except Exception as e : 
            self.log_debug.debug(e)
    

    # Item

    def create_item(self, id_code : str, brand: str, name: str, ingredient: str, allergen: str, nutriment: str, nutriscore: str, ecoscore: str, packaging: str, image: str, url_openfoodfact: str):
        try : 
            with self.engine.connect() as connection:
                query = text("INSERT INTO item (id_code, brand, name, ingredient, allergen, nutriment, nutriscore, ecoscore, packaging, image, url_openfoodfact)"
                            " VALUES (:id_code, :brand, :name, :ingredient, :allergen, :nutriment, :nutriscore, :ecoscore, :packaging, :image, :url_openfoodfact)")
                connection.execute(query, {"id_code" : id_code, "brand": brand ,"name": name, "ingredient": ingredient,"allergen" : allergen, "nutriment" : nutriment, "nutriscore" : nutriscore, "ecoscore" : ecoscore, "packaging" : packaging, "image" : image, "url_openfoodfact" : url_openfoodfact}) 
                connection.commit()

                self.log_debug.info(f"Item {id_code, brand, name} ajouté à la base de données {'test' if self.test else 'de production'}.")
            
        except Exception as e : 
            self.log_debug.debug(e)

    def get_item(self, id_code : str | None = None) :
        try :  
            with self.engine.connect() as connection:
                if id_code == None :
                    # with self.engine.connect() as connection:
                        query = text("SELECT * FROM item")
                        result = connection.execute(query, {"id_code" : id_code}) 
                else :
                        query = text(f"SELECT * FROM item WHERE id_code = :id_code")
                        result = connection.execute(query, {"id_code" : id_code}) 
            result = result.mappings().all()
            self.log_debug.info(f"retrieve item {id_code}")
            return result
        
        except Exception as e : 
            self.log_debug.debug(e)
    
    def update_item(self, id_code : str, brand: str, name: str, ingredient: str, allergen: str, nutriment: str, nutriscore: str, ecoscore: str, packaging: str, image: str, url_openfoodfact: str):
        try : 
            with self.engine.connect() as connection:
                query = text("UPDATE item SET id_code=:id_code, brand=:brand, name=:name, ingredient=:ingredient, allergen=:allergen, nutriment=:nutriment, nutriscore=:nutriscore, ecoscore=:ecoscore, packaging=:packaging, image=:image, url_openfoodfact=:url_openfoodfact WHERE id_code=:id_code")
                connection.execute(query, {"id_code" : id_code, "brand": brand ,"name": name, "ingredient": ingredient,"allergen" : allergen, "nutriment" : nutriment, "nutriscore" : nutriscore, "ecoscore" : ecoscore, "packaging" : packaging, "image" : image, "url_openfoodfact" : url_openfoodfact}) 
                connection.commit()

            self.log_debug.info(f"Update item {id_code}")

        except Exception as e : 
            self.log_debug.debug(e)

    def delete_item(self, id_code : str | None = None):
        try :
            with self.engine.connect() as connection:
                if id_code == None :
                    query = text("DELETE FROM item")
                    connection.execute(query)
                else : 
                    query = text("DELETE FROM item WHERE id_code=:id_code")
                    connection.execute(query, {"id_code" : id_code})
                connection.commit()
            self.log_debug.info(f"Delete item {id_code}")

        except Exception as e : 
            self.log_debug.debug(e)


    # User
           
    def create_user(self, username: str, last_name: str, first_name: str, age: int, gender: int):
        try :
            with self.engine.connect() as connection:
                query = text("INSERT INTO user (username, last_name, first_name, age, gender)"
                            " VALUES (:username, :last_name, :first_name, :age, :gender)")
                result = connection.execute(query, {"username": username ,"last_name": last_name, "first_name": first_name,"age" : age, "gender" : gender})
                connection.commit()

            self.log_debug.info(f"Create user {username}")
            return result
        
        except Exception as e : 
            self.log_debug.debug(e)

    def get_user(self, id_user : str | None = None):
        try: 
            with self.engine.connect() as connection:
                if id_user == None :
                    query = text("SELECT * FROM user")
                    result = connection.execute(query)
                else :
                    query = text(f"SELECT * FROM user WHERE id_user = :id_user")
                    result = connection.execute(query, {"id_user" : id_user})

            result = result.mappings().all()
            self.log_debug.info(f"retrieve user {id_user}")
            return result
        
        except Exception as e : 
            self.log_debug.debug(e)


    def update_user(self, id_user : str, username: str, last_name: str, first_name: str, age: str, gender: str):
        try : 
            with self.engine.connect() as connection:
                query = text("UPDATE user SET username=:username, last_name=:last_name, first_name=:first_name, age=:age, gender=:gender WHERE id_user = :id_user")
                connection.execute(query, {"username" : username, "last_name" : last_name, "first_name" : first_name, "age" : age, "gender" : gender, "id_user" :id_user})
                connection.commit()
            self.log_debug.info(f"Update user {id_user}")

        except Exception as e : 
            self.log_debug.debug(e)

    def delete_user(self, id_user : str | None = None):
        try : 
            with self.engine.connect() as connection:
                if id_user == None :
                    query = text("DELETE FROM user")
                    connection.execute(query)
                else :
                    query = text("DELETE FROM user WHERE id_user = :id_user")
                    connection.execute(query, {"id_user" : id_user})
                connection.commit()
            self.log_debug.info(f"Delete user {id_user}")

        except Exception as e : 
            self.log_debug.debug(e)

    
    # Place
            
    def create_place(self, name: str, adresse: str, postcode: str, city: str):
        try : 
            with self.engine.connect() as connection:
                query = text("INSERT INTO place (name, adresse, postcode, city)"
                            " VALUES (:name, :adresse, :postcode, :city)")
                connection.execute(query, {"name": name ,"adresse": adresse, "postcode": postcode, "city" : city})
                connection.commit()

                self.log_debug.info(f"create place {name}")

        except Exception as e : 
            self.log_debug.debug(e)

    def get_place(self, id_place : str | None = None):
        try : 
            with self.engine.connect() as connection:
                if id_place == None :
                    query = text("SELECT * FROM place")
                    result = connection.execute(query) 
                else :
                    query = text(f"SELECT * FROM place WHERE id_place = :id_place")
                    result = connection.execute(query, {"id_place" : id_place}) 
                result = result.mappings().all()
                return result
        except Exception as e : 
            self.log_debug.debug(e)

    def update_place(self, id_place : str, name: str, adresse: str, postcode: str, city: str):
        try : 
            with self.engine.connect() as connection:
                query = text("UPDATE place SET name = :name, adresse = :adresse, postcode =:postcode, city = :city WHERE id_place=:id_place")
                connection.execute(query, {"name" : name, "adresse" : adresse, "postcode" : postcode, "city" : city, "id_place" : id_place})
                connection.commit()

        except Exception as e : 
            self.log_debug.debug(e)

    def delete_place(self, id_place : str):
        try : 
            with self.engine.connect() as connection:
                if id_place == None :
                    query = text("DELETE FROM place")
                    connection.execute(query)
                else :
                    query = text("DELETE FROM place WHERE id_place = :id_place")
                    connection.execute(query, {"id_place" : id_place})
                connection.commit()

        except Exception as e : 
            self.log_debug.debug(e)


    # Scan

    def create_scan(self, id_user : int, id_code : str, id_place : int ):
        try: 
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
            self.log_debug.info(f"Create scan {id_code} from {id_user}.")
        
        except Exception as e : 
            self.log_debug.debug(e)

    def get_scan(self, id_user : int | None = None):
        try : 
            with self.engine.connect() as connection:
                if id_user == None :
                    query = text("SELECT id_user, id_code, id_place, year, month, day, hour, minute FROM scan")
                    result = connection.execute(query) 
                else :
                    query = text(f"SELECT id_user, id_code, id_place, year, month, day, hour, minute FROM scan WHERE id_user = :id_user")
                    result = connection.execute(query, {"id_user" : id_user}) 
                
                result = result.mappings().all()
                return result
        
        except Exception as e : 
            self.log_debug.debug(e)
            
    def delete_scan(self, id_user : str):
        try : 
            with self.engine.connect() as connection:
                query = text("DELETE FROM scan WHERE id_user = :id_user")
                connection.execute(query, {"id_user" : id_user})
                connection.commit()
        
        except Exception as e : 
            self.log_debug.debug(e)
    
    def authenticate(self, email) : 
        try : 
            with self.engine_app.connect() as connection:
                query = text(f"SELECT * FROM user WHERE email = '{email}'")
                result = connection.execute(query)

            result = result.mappings().all()
            result = result[0]

            return result
        
        except Exception as e : 
            self.log_debug.debug(e)
    
    
