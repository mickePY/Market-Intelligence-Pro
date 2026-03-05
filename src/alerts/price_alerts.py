import logging
from typing import Dict, List, Optional
from datetime import datetime

class AlertSystem:
    """Consolidated alerts for price changes, news sentiment, and market shifts."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_history = []

    def log_alert(self, type: str, message: str, level: str = "INFO"):
        """Centralized logging/store for alerts."""
        alert = {
            "timestamp": datetime.now(),
            "type": type.upper(),
            "message": message,
            "level": level
        }
        self.alert_history.append(alert)
        self.logger.info(f"[{type}] {message}")
        print(f"[{type}] {message}")

    def notify_price_change(self, competitor: str, current_price: float, old_price: float):
        """Send notifications (Slack, Email, Log) for significant price movements."""
        diff = current_price - old_price
        pct = (diff / old_price) * 100 if old_price > 0 else 0.0
        
        if abs(pct) > 5.0: # 5% Threshold logic
            level = "CRITICAL" if abs(pct) > 15.0 else "WARNING"
            status = "increase" if diff > 0 else "drop"
            msg = f"PRICE {status.upper()}: {competitor} at ${current_price:.2f} (Was ${old_price:.2f}, {pct:+.1f}%)"
            self.log_alert("Price Change", msg, level)

    def notify_sentiment_crash(self, competitor: str, current_score: float, previous_score: float):
        """Alert on major negative sentiment trends."""
        if current_score < -0.3 and previous_score > 0.0:
            msg = f"SENTIMENT CRASH: {competitor} brand perception plummeted to {current_score:.2f}"
            self.log_alert("Sentiment", msg, "CRITICAL")

    def notify_new_entrant(self, company_name: str, industry: str):
        """Alert on new market entrants."""
        msg = f"NEW COMPETITOR DETECTED: {company_name} is entering the {industry} segment."
        self.log_alert("Market Entry", msg, "INFO")

    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Fetch the most recent alerts for dashboard display."""
        return sorted(self.alert_history, key=lambda x: x["timestamp"], reverse=True)[:limit]
