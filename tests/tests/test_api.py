import httpx
from config import *
# Tests des différentes ressources


# API KEY

headers = {'X-API-Key': list(API_KEYS.keys())[0]}


def test_helloworld_raw() :
    response = httpx.get(f"http://api-backend:6001/", headers = headers)
    assert response.status_code == 200

def test_adminer_traefik() :
    response = httpx.get(f"http://traefik/adminer/", headers = headers)
    assert response.status_code == 200

def test_helloworld_traefik() :
    response = httpx.get(f"http://traefik/api-backend/", headers = headers)
    assert response.status_code == 200
