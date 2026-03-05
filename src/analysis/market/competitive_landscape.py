import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional

class CompetitiveLandscape:
    """Map competitor positioning, market share, and concentration (HHI)."""
    
    def __init__(self, segment: str):
        self.segment = segment
        self.competitors = []

    def add_competitor_data(self, name: str, revenue: float, quality_score: float, price_index: float):
        """Add competitor stats for mapping."""
        self.competitors.append({
            "name": name,
            "revenue": revenue,
            "quality": quality_score, # 1-10 (e.g. from sentiment + features)
            "price": price_index,     # 1-10 (Normalized price positioning)
            "market_share": 0.0
        })

    def calculate_market_stats(self) -> Dict:
        """Calculate market concentration and individual shares."""
        if not self.competitors: return {"hhi": 0.0, "total_revenue": 0.0}
        
        total_rev = np.sum([c["revenue"] for c in self.competitors])
        hhi = 0.0
        
        for comp in self.competitors:
            share = (comp["revenue"] / total_rev) * 100
            comp["market_share"] = share
            hhi += share ** 2 # HHI = sum of squared market shares
            
        return {
            "hhi": round(hhi, 2), # < 1500 (unconcentrated), > 2500 (highly concentrated)
            "total_revenue": round(total_rev, 2),
            "top_player": max(self.competitors, key=lambda x: x["market_share"])["name"]
        }

    def generate_perceptual_map_data(self) -> pd.DataFrame:
        """Prepare data for a 2D Price vs. Quality perceptual map."""
        if not self.competitors: return pd.DataFrame()
        
        df = pd.DataFrame(self.competitors)
        # Normalize/Scale if needed
        return df

    def identify_market_gap(self, x_grid: int = 10, y_grid: int = 10) -> Dict:
        """Find holes in the perceptual map where no competitor exists."""
        # Simple grid-based gap detection
        df = self.generate_perceptual_map_data()
        if df.empty: return {"gap_detected": False}
        
        # Look for regions with 0 competitors
        # (Assuming price/quality are on a 1-10 scale)
        occupied_quadrants = []
        for _, row in df.iterrows():
            q = (int(row['price']), int(row['quality']))
            occupied_quadrants.append(q)
            
        # Example: if lower-price/high-quality is empty
        gaps = []
        for x in range(1, x_grid + 1):
            for y in range(1, y_grid + 1):
                if (x, y) not in occupied_quadrants:
                    gaps.append((x, y))
                    
        return {
            "gap_detected": len(gaps) > 0,
            "prime_gap": "High Quality / Low Price" if (1, 10) in gaps else "Market Saturation High"
        }
