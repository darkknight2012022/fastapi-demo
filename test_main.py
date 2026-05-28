from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["healthy"] == True

def test_create_trade():
    res = client.post("/trades", json={
        "symbol": "btc", "side": "buy",
        "price": 67000, "quantity": 0.01
    })
    assert res.status_code == 201
    assert res.json()["symbol"] == "BTC"
    assert res.json()["total_value"] == 670.0

def test_create_trade_invalid():
    res = client.post("/trades", json={
        "symbol": "BTC", "side": "hold",
        "price": -100, "quantity": 0.01
    })
    assert res.status_code == 422

def test_get_trade_not_found():
    res = client.get("/trades/99999")
    assert res.status_code == 404

def test_login_success():
    res = client.post("/login", data={
        "username": "liuyu", "password": "password123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_fail():
    res = client.post("/login", data={
        "username": "liuyu", "password": "wrongpassword"
    })
    assert res.status_code == 401

def test_me_without_token():
    res = client.get("/me")
    assert res.status_code == 401
