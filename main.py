from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OK"}
# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_dummy_depth_data():
    return [
        {"emir": 243, "adet": 432771, "alis": 33.66, "satis": 0},
        {"emir": 61, "adet": 61, "alis": 33.58, "satis": 0},
        {"emir": 1, "adet": 10, "alis": 33.56, "satis": 0},
    ]

@app.get("/api/depth")
async def get_depth(symbol: str):
    return get_dummy_depth_data()

@app.get("/api/chart")
async def get_chart(symbol: str):
    ticker = yf.Ticker(symbol + ".IS")
    hist = ticker.history(period="5d", interval="15m")
    chart_data = [
        {"time": str(index), "price": row["Close"]}
        for index, row in hist.iterrows()
    ]
    return chart_data

class AlertRequest(BaseModel):
    symbol: str
    price: float

alerts = []

@app.post("/api/alert")
async def create_alert(alert: AlertRequest):
    alerts.append(alert.dict())
    return {"status": "created", "alert": alert}

@app.get("/api/alerts")
async def get_alerts():
    return alerts
