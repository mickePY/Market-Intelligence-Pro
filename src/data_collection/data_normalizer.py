import pandas as pd
from datetime import datetime
import re
from typing import Optional, Union, Dict

class DataNormalizer:
    """Normalize raw data from scrapers and APIs into database-ready formats."""
    
    @staticmethod
    def clean_currency(value: Union[str, float, int]) -> float:
        """Standardize currency to float (Remove symbols like $, €, etc.)."""
        if isinstance(value, (float, int)):
            return float(value)
        if not value:
            return 0.0
        # Remove anything that isn't a digit, period, or comma
        clean_val = re.sub(r'[^\d,.]', '', str(value))
        # Handle commas (European style) and convert to dot for float
        if ',' in clean_val and '.' in clean_val:
            clean_val = clean_val.replace(',', '') # 1,000.00 -> 1000.00
        elif ',' in clean_val:
            clean_val = clean_val.replace(',', '.') # 1000,00 -> 1000.00
            
        try:
            return float(clean_val)
        except ValueError:
            return 0.0

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse various date formats into standard datetime."""
        if not date_str:
            return datetime.now()
        
        try:
            # Add popular formats here (ISO, DD/MM/YYYY, etc.)
            return pd.to_datetime(date_str).to_pydatetime()
        except:
            return datetime.now()

    @staticmethod
    def normalize_sentiment(score: float, source: str) -> float:
        """Normalize sentiment scores from different APIs/libraries to [-1.0, 1.0]."""
        # TextBlob is already -1 to 1; NLTK VADER is also roughly -1 to 1 compound
        # If an API provides 0-100, normalize here
        if source == "social_api_x" and score > 1.0:
            return (score / 50.0) - 1.0 # 0-100 -> -1 to 1
        return max(-1.0, min(1.0, score))

    @staticmethod
    def format_company_name(name: str) -> str:
        """Trim, title case, and remove redundant indicators like LLC/Inc."""
        if not name: return "Unknown"
        clean = name.strip().title()
        # Remove common corporate suffixes
        clean = re.sub(r'\b(Llc|Inc|Corporation|Corp|Plc|Ltd|S\.a)\.?\b', '', clean, flags=re.IGNORECASE)
        return clean.strip()

    def process_scraping_payload(self, company_name: str, payload: Dict) -> Dict:
        """Standardize a full payload from web scrapers."""
        return {
            "company_name": self.format_company_name(company_name),
            "normalized_price": self.clean_currency(payload.get("price")),
            "timestamp": self.parse_date(payload.get("date")),
            "features": [f.strip() for f in payload.get("features", [])]
        }
