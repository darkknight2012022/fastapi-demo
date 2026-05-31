import urllib.request
import json

BASE_URL = "http://localhost:8000"

def api_get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def api_post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body,
          headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def test_root_endpoint():
    res = api_get("/")
    assert res["status"] == "ok"
    assert "time" in res
    print("✅ GET / 通过")

def test_health_endpoint():
    res = api_get("/health")
    assert res["healthy"] == True
    print("✅ GET /health 通过")

def test_create_and_get_trade():
    trade = api_post("/trades", {
        "symbol": "eth", "side": "buy",
        "price": 3200, "quantity": 0.5
    })
    assert trade["symbol"] == "ETH"
    assert trade["total_value"] == 1600.0
    assert "id" in trade
    trade_id = trade["id"]
    fetched = api_get(f"/trades/{trade_id}")
    assert fetched["id"] == trade_id
    print(f"✅ POST /trades + GET /trades/{trade_id} 通过")

def test_docs_accessible():
    req = urllib.request.Request(f"{BASE_URL}/docs")
    with urllib.request.urlopen(req) as r:
        html = r.read().decode()
    assert "swagger" in html.lower() or "openapi" in html.lower()
    print("✅ GET /docs Swagger UI 可访问")
