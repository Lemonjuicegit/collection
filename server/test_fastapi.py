from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_getUser():
    response = client.get("/get_user")
    assert response.text == {
        "code": 200,
        "data": {
            "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpcCI6IjE5Mi4xNjguMi41MSIsImV4cCI6MTcyNjcyOTIyOX0.EeJagbPdvtW-rvrnVSgyQQhuw6t74T_y1TXQmVD5XCo",
            "device": {
                "ip": "192.168.2.51",
                "title": "戴佳宏",
                "name": "0c3605cae19c48c299a14f608b9ba54b",
                "id": 68
                }
        },
        "msg": ""
    }