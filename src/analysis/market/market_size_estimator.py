from typing import Dict, List, Optional
import numpy as np

class MarketSizeEstimator:
    """Estimate and forecast market size (TAM/SAM/SOM)."""
    
    def __init__(self, target_segment: str = "AI/SaaS"):
        self.target_segment = target_segment
        self.raw_data = {
            "top_down": [], # External reports (e.g. Gartner)
            "bottom_up": [] # Competitor revenues (e.g. Sum of known players)
        }

    def add_industry_report(self, estimate: float, source: str, year: int):
        """Include a top-down estimate from an analyst/report."""
        self.raw_data["top_down"].append({
            "value": estimate,
            "source": source,
            "year": year
        })

    def add_competitor_revenue(self, revenue: float, company_name: str, share: float = 0.0):
        """Add bottom-up data from a specific competitor."""
        self.raw_data["bottom_up"].append({
            "value": revenue,
            "name": company_name,
            "estimated_market_share": share
        })

    def estimate_market_size_v2(self) -> Dict:
        """Calculate market size using both approaches (Weighted Average)."""
        td_values = [r["value"] for r in self.raw_data["top_down"]]
        bu_values = [r["value"] for r in self.raw_data["bottom_up"]]
        
        # Simple weighted avg: Top-down (40%), Bottom-up (60%)
        td_avg = np.mean(td_values) if td_values else 0.0
        bu_sum = np.sum(bu_values) if bu_values else 0.0
        
        # For Bottom-up, if we only know top 5 players, estimate total market
        if bu_sum > 0:
            avg_share = np.mean([r["estimated_market_share"] for r in self.raw_data["bottom_up"] if r["estimated_market_share"] > 0])
            if avg_share > 0:
                bu_extrapolated = bu_sum / (avg_share * len(bu_values))
            else:
                bu_extrapolated = bu_sum * 2.0 # Default multiplier
        else:
            bu_extrapolated = 0.0
            
        final_estimate = (td_avg * 0.4) + (bu_extrapolated * 0.6) if td_avg and bu_extrapolated else (td_avg or bu_extrapolated)
        
        return {
            "tam": round(final_estimate, 2),
            "sam": round(final_estimate * 0.4, 2), # Typical SaaS SAM/SOM proxy
            "som": round(final_estimate * 0.1, 2),
            "confidence": "Medium" if td_values and bu_values else "Low",
            "unit": "USD Billion"
        }

    def forecast_growth(self, current_size: float, CAGR: float = 0.15, years: int = 5) -> List[Dict]:
        """Project future market size based on Compound Annual Growth Rate."""
        projections = []
        for i in range(1, years + 1):
            val = current_size * (1 + CAGR) ** i
            projections.append({"year": datetime.now().year + i, "size": round(val, 2)})
        return projections
