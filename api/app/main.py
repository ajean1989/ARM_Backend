from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated

from app.maria import Maria
from app.config import API_KEYS
from app.log import Logg

#  Log

log = Logg()
log_debug = log.set_log_api_backend_debug()


# API KEY

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# Fonction de validation de l'API key

async def validate_api_key(api_key = Depends(api_key_header)):
    if api_key in API_KEYS:
        return api_key
    # code 403 automatiquement retourné par APIKeyHeader 


app = FastAPI(
    title="API ARMarket - OpenAPI 3.0",
    description="API ARMarket for VPS - Link with dataset and datawarehouse - E1 Project.",
    servers=[{"name" : "5.195.7.246"}],
    openapi_tags=[{"name" : "dataset"},
                  {"name", "datawarehouse"}],
    dependencies=[Depends(validate_api_key)],
    root_path="/api-backend"   # Pour gérer le sous chemin de traefik
)

# CORS

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connexion Maria DB
def maria_connect():        # Permet d'overwrite pour les tests d'api (voir tests/main.py app.dependency_overrides[maria_connect] = override_maria) 
    return Maria(False)



# Routes

@app.get("/")
async def read_root():
    try : 
        return {"Hello": "World"}
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")


## application authentification 

@app.post("/authenticate/")
async def auth( mr : Annotated[Maria, Depends(maria_connect)], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    try : 

        result = mr.authenticate(email)
        if result == None :
            return {
                "success": False,
                "message": "Invalid username or password"
            }
        if email == result["email"] and password == result["password"] :
            return {"success": True,
                    "message": "Authentication successful",
                    "token": "azdazad",
                    "user": {
                        "id": result["id_user"],
                        "email": result["email"],
                        "first_name" : result["first_name"],
                        "last_name" : result["last_name"],
                        "role" : result["id_role"]
                        }
            }
        else : 
            return {
                "success": False,
                "message": "Something wrong ..."
            }
            

    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e, email, password}")

## Item

class Item(BaseModel):
    id_code : str
    name: str
    brand : str
    ingredient : str
    allergen: str
    nutriment : str
    nutriscore : str
    ecoscore : str
    packaging: str
    image : str
    url_openfoodfact : str

@app.post("/items/")
async def record_item(mr : Annotated[Maria, Depends(maria_connect)], item: Item):
    try :
        item = item.model_dump()
        mr.create_item(id_code=item["id_code"], name=item["name"], brand=item["brand"], ingredient=item["ingredient"], allergen=item["allergen"], nutriment=item["nutriment"], nutriscore=item["nutriscore"], ecoscore=item["ecoscore"] , packaging=item["packaging"], image=item["image"], url_openfoodfact=item["url_openfoodfact"])
        log_debug.debug(f'Item {item["id_code"], item["brand"], item["name"]} enregistré.')
        return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")
    
@app.get("/items/")
async def get_items(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_item()
        res = [dict(row) for row in res]
        log_debug.debug(f"GET /items/")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e} - {res} - {type(res)}")

@app.get("/items/{id}")
async def get_item(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.get_item(id)
        res = [dict(row) for row in res]
        log_debug.debug(f"GET /items/{id}")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e} - {res} - {type(res)}")


@app.put("/items/")
async def update_item(mr : Annotated[Maria, Depends(maria_connect)], item: Item):
    try : 
        item = item.model_dump()
        res = mr.update_item(id_code=item["id_code"], name=item["name"], brand=item["brand"], ingredient=item["ingredient"], allergen=item["allergen"], nutriment=item["nutriment"], nutriscore=item["nutriscore"], ecoscore=item["ecoscore"] , packaging=item["packaging"], image=item["image"], url_openfoodfact=item["url_openfoodfact"])
        log_debug.debug(f'UPDATE /items/ {item["id_code"]}')
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")

@app.delete("/items/{id}")
async def delete_item(mr : Annotated[Maria, Depends(maria_connect)], id: int | None):
    try : 
        res = mr.delete_item(id)
        log_debug.debug(f"DELETE /items/{id}")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")




## User
    
class User(BaseModel):
    username: str
    last_name : str
    first_name : str
    age: int
    gender : int


@app.post("/users/")
async def record_user(mr : Annotated[Maria, Depends(maria_connect)], user: User):
    try :
        user = user.model_dump()
        username = user["username"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        age = user["age"]
        gender = user["gender"]
        res = mr.create_user(username=username, last_name=last_name, first_name=first_name, age=age, gender=gender)
        log_debug.debug(f"POST /users/ : {username}")
        return JSONResponse(content={"message": "User ajouté avec succès", "result" : str(res)}, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")

@app.get("/users/")
async def get_users(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_user()
        res = [dict(row) for row in res]
        log_debug.debug(f"GET /users/")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")  

@app.get("/users/{id}")
async def get_user(mr : Annotated[Maria, Depends(maria_connect)], id : int):
    try : 
        res = mr.get_user(id)
        res = [dict(row) for row in res]
        log_debug.debug(f"GET /users/{id}")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")
    
@app.put("/users/{id}")
async def update_user(mr : Annotated[Maria, Depends(maria_connect)], id : int, user : User):
    try : 
        user = user.model_dump()
        username = user["username"]
        first_name = user["first_name"]
        last_name = user["first_name"]
        age = user["age"]
        gender = user["gender"]
        res = mr.update_user(id_user=id, username=username, last_name=last_name, first_name=first_name, age=age, gender=gender)
        log_debug.debug(f"PUT /users/{id}")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")

@app.delete("/users/{id}")
async def delete_user(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_user(id)
        log_debug.debug(f"DELETE /users/{id}")
        return JSONResponse(content=res, status_code=200)
    except Exception as e :
        log_debug.info(f"erreur : {e}")
        raise HTTPException(status_code=422, detail=f"Erreur API : {e}")






## Place

class Place(BaseModel):
    name: str
    adresse : str
    postcode : str
    city: str

@app.post("/places/")
async def record_place(mr : Annotated[Maria, Depends(maria_connect)], place: Place):
    try :
        place = place.model_dump()
        name = place["name"]
        adresse = place["adresse"]
        postcode = place["postcode"]
        city = place["city"]
        res = mr.create_place(name=name, adresse=adresse, postcode=postcode, city=city)
        return JSONResponse(content={"message": "Place ajoutée avec succès", "result" : str(res)}, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.get("/places/")
async def get_place(mr : Annotated[Maria, Depends(maria_connect)]):
    try : 
        res = mr.get_place()
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} ")   
    
@app.get("/places/{id}")
async def get_place(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.get_place(id)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message} ")   

@app.put("/places/{id}")
async def update_place(mr : Annotated[Maria, Depends(maria_connect)], id: int, place : Place):
    try : 
        place = place.model_dump()
        name = place["name"]
        adresse = place["adresse"]
        postcode = place["postcode"]
        city = place["city"]
        res = mr.update_place(id_place = id, name=name, adresse=adresse, postcode=postcode, city=city)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/places/{id}")
async def delete_place(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_place(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")







## Scan
    
class Scan(BaseModel):
    id_user: int | None
    id_code : str | None
    id_place : int | None

@app.post("/scan/")
async def record_scan(mr : Annotated[Maria, Depends(maria_connect)], scan: Scan):
    try :
        scan = scan.model_dump()
        mr.create_scan(scan["id_user"], scan["id_code"], scan["id_place"], )
        return JSONResponse(content={"message": "Scan ajoutée avec succès"}, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")


@app.get("/scan/")
async def get_scan(mr : Annotated[Maria, Depends(maria_connect)], id_user : int | None = None):
    try :
        if id_user == None :
            res = mr.get_scan()
        else : 
            res = mr.get_scan(id_user)
        res = [dict(row) for row in res]
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")

@app.delete("/scan/")
async def delete_scan(mr : Annotated[Maria, Depends(maria_connect)], id: int):
    try : 
        res = mr.delete_scan(id)
        return JSONResponse(content=res, status_code=200)
    except Exception as e:
        erreur_message = e
        raise HTTPException(status_code=418, detail=f"Erreur API : {erreur_message}")