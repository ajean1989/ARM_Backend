import httpx
from config import *
# Tests des différentes ressources

api = "api-backend"

# API KEY

headers = {'X-API-Key': list(API_KEYS.keys())[0]}


def test_helloworld() :
    response = httpx.get(f"http://{api}/:6001", headers = headers)
    assert response.status_code == 200

    response = httpx.get(f"http://{api}/api-backend/", headers = headers)
    assert response.status_code == 200
