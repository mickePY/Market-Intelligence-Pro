from typing import Dict, List, Optional
import numpy as np

class SWOTAnalyzer:
    """Automated SWOT analysis based on competitor metrics, sentiment, and trends."""
    
    def __init__(self, competitor_id: str, name: str):
        self.competitor_id = competitor_id
        self.name = name
        self.scores = {
            "Strengths": [],
            "Weaknesses": [],
            "Opportunities": [],
            "Threats": []
        }

    def analyze_financials(self, metrics: Dict):
        """Analyze revenue, growth, and margins for SWOT points."""
        revenue = metrics.get("revenue", 0)
        growth = metrics.get("growth_rate", 0)
        margin = metrics.get("profit_margin", 0)

        # Financial Strengths
        if revenue > 1e10: # $10B threshold for dominance
            self.scores["Strengths"].append(f"Global dominance (Revenue > $10B)")
        elif revenue > 1e6: # $1M+ for established
            self.scores["Strengths"].append(f"Established market presence (Revenue > $1M)")

        if growth > 0.3: # 30%+ growth
            self.scores["Strengths"].append(f"Strong growth trajectory (+{growth*100:.1f}%)")
        elif growth < 0.05: # Below 5% growth
            self.scores["Weaknesses"].append(f"Stagnating growth (+{growth*100:.1f}%)")

        # Weaknesses
        if margin < 0:
            self.scores["Weaknesses"].append(f"Unprofitable (Margin: {margin*100:.1f}%)")

    def analyze_sentiment(self, sentiment_history: List[float]):
        """Evaluate public perception over time for SWOT mapping."""
        if not sentiment_history: return
        
        avg_sentiment = np.mean(sentiment_history)
        
        if avg_sentiment > 0.4:
            self.scores["Strengths"].append(f"High brand sentiment ({avg_sentiment:.2f})")
        elif avg_sentiment < -0.1:
            self.scores["Weaknesses"].append(f"Negative sentiment trend ({avg_sentiment:.2f})")

    def analyze_market_trends(self, market_data: Dict):
        """Identify opportunities and threats from external trends."""
        interest_trend = market_data.get("interest_trend", 0.0) # From Google Trends
        competitors_count = market_data.get("competitors_count", 1)
        
        # Opportunities
        if interest_trend > 0.2:
            self.scores["Opportunities"].append("Rising search interest (New demand)")
        if competitors_count <= 2:
            self.scores["Opportunities"].append("Low market concentration (Market consolidation)")

        # Threats
        if interest_trend < -0.2:
            self.scores["Threats"].append("Industry-wide declining interest")
        if competitors_count > 10:
            self.scores["Threats"].append("Highly fragmented/competitive environment")

    def generate_swot_report(self) -> Dict:
        """Consolidate SWOT points into a final JSON-ready report."""
        return {
            "competitor_id": self.competitor_id,
            "company_name": self.name,
            "swot": self.scores,
            "summary_score": self._calculate_overall_health()
        }

    def _calculate_overall_health(self) -> float:
        """Quantify overall health on a scale of 0 to 10."""
        s = len(self.scores["Strengths"]) * 2.0
        w = len(self.scores["Weaknesses"]) * 1.5
        o = len(self.scores["Opportunities"]) * 1.0
        t = len(self.scores["Threats"]) * 1.0
        
        score = (s + o) - (w + t)
        # Normalize to 0-10 (approximate)
        return max(0.0, min(10.0, 5.0 + score))
