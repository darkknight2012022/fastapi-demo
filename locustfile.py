from locust import HttpUser, task, between

class TradingAPIUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def get_root(self):
        self.client.get("/")

    @task(2)
    def get_health(self):
        self.client.get("/health")

    @task(1)
    def create_trade(self):
        self.client.post("/trades", json={
            "symbol": "BTC",
            "side": "buy",
            "price": 67000,
            "quantity": 0.01
        })
