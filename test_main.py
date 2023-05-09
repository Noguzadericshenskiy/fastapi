from fastapi.testclient import TestClient
from typing import Dict
from main import app


client = TestClient(app)


def test_main_dishes():
    response = client.get("/dishes/")
    assert response.status_code == 200
    assert  response.json()[0] == Dict
    # assert .isinstance(dict)
# {"id":2,"name_of_dish":"Шашлык","preparation_time":30,"number_of_views":5}
