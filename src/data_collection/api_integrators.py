import yfinance as yf
from pytrends.request import TrendReq
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from src.data_collection.data_normalizer import DataNormalizer

class APIIntegrator:
    """Consolidated API fetching for Google Trends and YFinance."""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360) # US/Global search behavior
        self.normalizer = DataNormalizer()

    def fetch_stock_metrics(self, ticker: str) -> Optional[Dict]:
        """Fetch real-time financial metrics for a public competitor."""
        if not ticker: return None
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Key Profitability & Valuation metrics
            return {
                "market_cap": info.get("marketCap", 0.0),
                "revenue": info.get("totalRevenue", 0.0),
                "profit_margin": info.get("profitMargins", 0.0),
                "growth_rate": info.get("revenueGrowth", 0.0),
                "pe_ratio": info.get("forwardPE", 0.0),
                "recorded_at": datetime.now()
            }
        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            return None

    def fetch_market_interest(self, keywords: List[str], timeframe: str = 'today 3-m') -> pd.DataFrame:
        """Fetch Google Trends (Search Volume) for a set of keywords (competitors)."""
        if not keywords: return pd.DataFrame()
        
        try:
            self.pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            interest_over_time = self.pytrends.interest_over_time()
            if not interest_over_time.empty:
                # Remove 'isPartial' column from pytrends
                return interest_over_time.drop(columns=['isPartial'], errors='ignore')
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching Google Trends for {keywords}: {e}")
            return pd.DataFrame()

    def get_financial_history(self, ticker: str, period: str = "2y") -> pd.DataFrame:
        """Fetch historical revenue/earnings if public."""
        if not ticker: return pd.DataFrame()
        
        try:
            stock = yf.Ticker(ticker)
            # Returns annual/quarterly financials
            return stock.financials.transpose()
        except Exception as e:
            print(f"Error fetching financial history for {ticker}: {e}")
            return pd.DataFrame()
