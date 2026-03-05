import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import List, Dict, Optional
import numpy as np

# Download required nltk resources if not present
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

class SentimentAnalyzer:
    """Analyze customer perception, sentiment trends, and topic extraction."""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict:
        """Perform full sentiment and basic topic analysis on a snippet."""
        if not text or len(text) < 5:
            return {"sentiment": 0.0, "subjectivity": 0.0, "topics": []}
        
        # NLTK Vader compound score (-1 to 1)
        sentiment_scores = self.sia.polarity_scores(text)
        compound = sentiment_scores['compound']
        
        # TextBlob for subjectivity and noun phrases (simple topic extraction)
        blob = TextBlob(text)
        subjectivity = blob.sentiment.subjectivity
        noun_phrases = list(blob.noun_phrases)

        return {
            "sentiment": compound,
            "subjectivity": subjectivity,
            "topics": noun_phrases[:5], # top 5
            "status": "positive" if compound > 0.05 else ("negative" if compound < -0.05 else "neutral")
        }

    def aggregate_competitor_sentiment(self, reviews: List[str]) -> Dict:
        """Calculate aggregate scores for a competitor over multiple reviews."""
        if not reviews: return {"avg_sentiment": 0.0, "mention_count": 0}
        
        results = [self.analyze_text(r) for r in reviews]
        sentiments = [r['sentiment'] for r in results]
        
        # Extract common topics (flatten lists)
        all_topics = []
        for r in results:
            all_topics.extend(r['topics'])
            
        # Basic frequency (limited logic for speed)
        from collections import Counter
        top_themes = Counter(all_topics).most_common(5)

        return {
            "avg_sentiment": float(np.mean(sentiments)),
            "std_deviation": float(np.std(sentiments)),
            "mention_count": len(reviews),
            "common_themes": [theme for theme, count in top_themes]
        }

    def detect_sentiment_shift(self, current_batch: List[float], past_avg: float) -> bool:
        """Alert if current sentiment deviates significantly (e.g. news crash)."""
        if not current_batch: return False
        
        current_avg = np.mean(current_batch)
        # Shift > 0.3 threshold
        if abs(current_avg - past_avg) > 0.3:
            return True
        return False
