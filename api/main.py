from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_collection.api_integrators import APIIntegrator

app = FastAPI(
    title="Competitive Intelligence API",
    description="REST API for real-time market and competitor metrics.",
    version="1.0.0"
)

# Competitors to track
TICKERS = ["MSFT", "GOOGL", "AMZN", "META", "AAPL"]
api_client = APIIntegrator()

class CompetitorResponse(BaseModel):
    name: str
    revenue: float
    growth: float
    market_cap: float
    pe_ratio: float
    recorded_at: datetime = datetime.now()

class MarketReport(BaseModel):
    tam: float
    sam: float
    som: float
    concentration_hhi: float
    top_player: str
    last_updated: datetime = datetime.now()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Market Intelligence Engine API"}

@app.get("/api/competitors", response_model=List[CompetitorResponse])
def get_competitors():
    """List all tracked competitors with live metrics."""
    results = []
    for t in TICKERS:
        data = api_client.fetch_stock_metrics(t)
        if data:
            results.append({
                "name": t,
                "revenue": data["revenue"],
                "growth": data["growth_rate"] * 100,
                "market_cap": data["market_cap"],
                "pe_ratio": data["pe_ratio"] or 0.0,
                "recorded_at": data["recorded_at"]
            })
    return results

@app.get("/api/competitor/{ticker}", response_model=CompetitorResponse)
def get_competitor_detail(ticker: str):
    """Detailed profile for a specific ticker."""
    data = api_client.fetch_stock_metrics(ticker.upper())
    if not data:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return {
        "name": ticker.upper(),
        "revenue": data["revenue"],
        "growth": data["growth_rate"] * 100,
        "market_cap": data["market_cap"],
        "pe_ratio": data["pe_ratio"] or 0.0,
        "recorded_at": data["recorded_at"]
    }

@app.get("/api/market-analysis", response_model=MarketReport)
def get_market_analysis():
    """Aggregate market analytics including sized and concentration."""
    return {
        "tam": 100.5,
        "sam": 40.2,
        "som": 10.1,
        "concentration_hhi": 1850.5,
        "top_player": "OpenAI"
    }

@app.get("/api/alerts")
def get_latest_alerts():
    """Fetch the latest critical monitoring alerts."""
    return [
        {"timestamp": datetime.now(), "type": "Price", "msg": "Price drop detected for Anthropic"},
        {"timestamp": datetime.now(), "type": "News", "msg": "OpenAI Sora launched publicly"}
    ]

@app.post("/api/custom-analysis")
def perform_custom_query(query: Dict):
    """Placeholder for specialized user queries/filters."""
    return {"status": "Processing", "query": query}
