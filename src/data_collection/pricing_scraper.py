from datetime import datetime
from typing import Dict, List, Optional
from src.data_collection.web_scraper import WebScraper
from src.data_collection.data_normalizer import DataNormalizer
import logging

class PricingScraper:
    """Specialized engine for competitor price monitoring and historical tracking."""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.normalizer = DataNormalizer()
        self.logger = logging.getLogger(__name__)

    def monitor_price_change(self, competitor_id: str, url: str, selector: str, previous_price: float = 0.0) -> Dict:
        """Fetch current price, normalize, and detect changes."""
        raw_result = self.scraper.scrape_competitor_pricing(url, selector)
        
        if "error" in raw_result:
            self.logger.warning(f"Error scraping {competitor_id}: {raw_result['error']}")
            return {"competitor_id": competitor_id, "current_price": 0.0, "status": "failed"}

        current_price = self.normalizer.clean_currency(raw_result.get("price"))
        
        # Calculate change
        change_pct = 0.0
        if previous_price > 0:
            change_pct = ((current_price - previous_price) / previous_price) * 100

        return {
            "competitor_id": competitor_id,
            "current_price": current_price,
            "previous_price": previous_price,
            "change_pct": round(change_pct, 2),
            "status": "success",
            "timestamp": datetime.now()
        }

    def batch_price_check(self, targets: List[Dict]) -> List[Dict]:
        """Perform price checks for multiple competitors in bulk."""
        results = []
        for target in targets:
            res = self.monitor_price_change(
                target['id'], 
                target['url'], 
                target['selector'], 
                target.get('prev_price', 0.0)
            )
            results.append(res)
        return results
