from fastapi import Depends
from prometheus_fastapi_instrumentator import Instrumentator
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

app = FastAPI(title="Trading API", version="1.0.0")

trades_db = []


class TradeCreate(BaseModel):
    symbol: str = Field(..., min_length=2, max_length=10, example="BTC")
    side: str = Field(..., example="buy")
    price: float = Field(..., gt=0)
    quantity: float = Field(..., gt=0)

    @validator('side')
    def side_must_be_valid(cls, v):
        if v not in ['buy', 'sell']:
            raise ValueError('side 只能是 buy 或 sell')
        return v

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: str
    price: float
    quantity: float
    total_value: float
    created_at: str


@app.get("/")
def root():
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.get("/health")
def health():
    return {"healthy": True, "trades_count": len(trades_db)}


@app.post("/trades", response_model=TradeResponse, status_code=201)
def create_trade(trade: TradeCreate):
    trade_id = len(trades_db) + 1
    new_trade = {
        "id": trade_id,
        "symbol": trade.symbol,
        "side": trade.side,
        "price": trade.price,
        "quantity": trade.quantity,
        "total_value": trade.price * trade.quantity,
        "created_at": datetime.now().isoformat()
    }
    trades_db.append(new_trade)
    return new_trade


@app.get("/trades", response_model=List[TradeResponse])
def get_trades(symbol: Optional[str] = None):
    if symbol:
        return [t for t in trades_db if t["symbol"] == symbol.upper()]
    return trades_db


@app.get("/trades/{trade_id}", response_model=TradeResponse)
def get_trade(trade_id: int):
    for trade in trades_db:
        if trade["id"] == trade_id:
            return trade
    raise HTTPException(status_code=404, detail=f"交易 {trade_id} 不存在")


SECRET_KEY = "dev-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

fake_users = {
    "liuyu": {"username": "liuyu", "password": "password123"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(data: dict):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or username not in fake_users:
            raise HTTPException(status_code=401, detail="无效的 token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="token 已过期或无效")


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user, "message": "鉴权成功！"}


# ── 监控指标 ──
Instrumentator().instrument(app).expose(app)
