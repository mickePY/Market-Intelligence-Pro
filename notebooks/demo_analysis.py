import os
import sys
# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from src.data_collection.api_integrators import APIIntegrator
from src.data_collection.data_normalizer import DataNormalizer
from src.analysis.competitive.swot_analyzer import SWOTAnalyzer
from src.analysis.customer.sentiment_analyzer import SentimentAnalyzer
import json

def run_demo():
    print("--- 📊 DATA COLLECTION & ANALYSIS DEMO ---")
    
    # 1. API Integration
    api = APIIntegrator()
    print("\n[Step 1] Fetching Financial Metrics (Google)...")
    goog_metrics = api.fetch_stock_metrics("GOOGL")
    if goog_metrics:
        print(f"Success: Revenue: ${goog_metrics['revenue']/1e9:.1f}B, Growth: {goog_metrics['growth_rate']*100:.1f}%")
    
    # 2. Market Interest
    print("\n[Step 2] Fetching Google Trends (AI Interest)...")
    trends = api.fetch_market_interest(["ChatGPT", "Claude AI", "Gemini AI"])
    if not trends.empty:
        print(f"Recent Trends (Head):\n{trends.tail(5)}")

    # 3. Sentiment Analysis
    print("\n[Step 3] Analyzing Customer Sentiment (Sample)...")
    sent = SentimentAnalyzer()
    review = "I tried the new Gemini model and it is incredibly fast but lacks the depth of Claude 3."
    analysis = sent.analyze_text(review)
    print(f"Text: \"{review}\"")
    print(f"Result: {analysis['status'].upper()} (Score: {analysis['sentiment']:.2f})")
    print(f"Detected Topics: {analysis['topics']}")

    # 4. SWOT Generation
    print("\n[Step 4] Generating Automated SWOT (Google)...")
    swot = SWOTAnalyzer("googl", "Google Cloud")
    swot.analyze_financials(goog_metrics)
    swot.analyze_sentiment([0.2, 0.4, 0.1, -0.1])
    swot_report = swot.generate_swot_report()
    print(json.dumps(swot_report, indent=4))

if __name__ == "__main__":
    run_demo()
