# 📊 Competitive Analysis & Market Intelligence Engine (CAMIE)
## Comprehensive Business Intelligence & Strategic Research Platform
### Production-Ready Data Analyst Project

---

## 🌎 Overview / Aperçu
**FR :** CAMIE est un système complet conçu pour la surveillance, l'analyse et l'extraction d'insights stratégiques sur la concurrence et le marché. Il automatise la collecte de données multi-sources, réalise des analyses comparatives poussées (SWOT, positionnement prix vs qualité) et génère des alertes critiques en temps réel.

**EN :** CAMIE is a comprehensive system designed for monitoring, analyzing, and extracting strategic insights on competition and the market. It automates multi-source data collection, performs advanced comparative analyses (SWOT, price vs. quality positioning), and generates real-time critical alerts.

---

## 🚀 Key Features / Fonctionnalités Clés
- **Multi-Source Data Ingestion**: Web scraping (static & dynamic), Financial APIs (YFinance), Search Trends (Google Trends), and News Aggregators.
- **Enterprise Data Warehouse**: Robust Star Schema design in PostgreSQL (or SQLite for dev) with history tracking (SCD Type 2).
- **Competitive Analysis Engine**: 
  - Automated quantified **SWOT Analysis**.
  - **Perceptual Mapping**: Real-time 2D visualization of Market Positioning.
  - **Pricing Strategy Analyzer**: Multi-competitor price tracking with automated change alerts.
- **Customer Intelligence**: Sentiment scoring and topic extraction using NLTK, VADER, and TextBlob.
- **Market Analytics**: TAM/SAM/SOM estimation and market concentration tracking (HHI index).
- **Executive Dashboard**: Premium Streamlit UI with glassmorphism, interactive Plotly charts, and export capabilities.
- **Automated Alerting**: Immediate notifications for price shifts, news crashes, or new entrants.
- **API Access**: Robust FastAPI integration for programmatic intelligence delivery.

---

## 🛠 Tech Stack / Stack Technique
- **Language**: Python 3.10+
- **Data Collection**: Scrapy, BeautifulSoup4, Selenium, Pytrends, YFinance.
- **Data Management**: SQLAlchemy, PostgreSQL, Pandas.
- **Analysis & ML**: Scikit-learn (Trends), NLTK/TextBlob (Sentiment), NumPy.
- **Visualization**: Streamlit, Plotly, Matplotlib.
- **API & Delivery**: FastAPI, Pydantic, APScheduler.
- **Environment**: Docker, Python-dotenv.

---

## 📐 Project Structure / Structure du Projet
```bash
├── api/                        # FastAPI Layer
├── config/                     # YAML/JSON configurations
├── docs/                       # Detailed Methodology & KPI guides
├── notebooks/                  # Demo & EDA notebooks
├── src/
│   ├── alerts/                 # Price/Sentiment alerting logic
│   ├── analysis/               # Core analytical engine
│   │   ├── competitive/        # SWOT, Positioning, Pricing logic
│   │   ├── customer/           # Sentiment & Brand loyalty
│   │   ├── market/             # Market size & HHI concentration
│   │   └── financial/          # Metrics & Valuation
│   ├── data_collection/        # Scrapers & API integrations
│   ├── data_management/        # DB schema & Warehouse management
│   ├── orchestration/          # APScheduler cron jobs
│   └── visualization/          # Main Streamlit Dashboard
├── tests/                      # Unit & logic testing
└── results/                    # Generated reports & profile logs
```

---

## 📊 Analytical Methodology / Méthodologie d'Analyse

### 1. Competitive SWOT Logic
Unlike qualitative SWOT, CAMIE uses **quantified metrics**:
- **Strengths**: Revenue > $10B, Growth > 25%, Sentiment > 0.4.
- **Weaknesses**: Unprofitability, Negative Sentiment, High P/E Ratio.
- **Opportunities**: Rapidly growing Google Trends interest in segment.
- **Threats**: Increasing Market Concentration (HHI > 2500) or 5+ new entrants/month.

### 2. Market Positioning (Perceptual Maps)
Uses a **2D Coordinate System** normalized between 0 and 10:
- **X-axis**: Price Index (Normalized across all competitors).
- **Y-axis**: Quality/Feat Score (Weighted avg of sentiment + number of features).
- **Core Insight**: Identifies "Blue Oceans" (High quality, low competition areas).

### 3. Sentiment & Social Listening
Uses the **VADER Compound score**:
- **Formula**: `S = (sum of pos - sum of neg) / cardinality`.
- Alerts are triggered if the **delta sentiment** exceeds 0.3 in a 24-hour window.

---

## 📈 Executive Insights Case Study
*Coming Soon: In-depth analysis of the AI LLM Market (OpenAI vs Anthropic vs Google).*

---

## 📂 Installation & Setup (FR/EN)

### 1. Prerequisites / Prérequis
- **Python 3.10+** (Recommended/Recommandé)
- **Git**

### 2. Installation
```powershell
# Clone the repository / Cloner le dépôt
git clone https://github.com/mickePY/Market-Intelligence-Pro.git
cd Market-Intelligence-Pro

# Install dependencies / Installer les dépendances
pip install -r requirements.txt
pip install fpdf2  # Required for PDF reports
```

### 3. Execution / Lancement
For a full production experience, run both the API and the Dashboard in separate terminals:
*Pour une expérience complète, lancez l'API et le Dashboard dans deux terminaux séparés :*

**Terminal 1: Internal Intelligence API (Backend)**
```powershell
uvicorn api.main:app --reload
```
*Access API Docs at: http://127.0.0.1:8000/docs*

**Terminal 2: Interactive Strategy Dashboard (Frontend)**
```powershell
# Windows PowerShell
$env:PYTHONPATH="."
streamlit run src/visualization/competitive_dashboard.py
```

### 4. Interactive Features / Utilisation
- **Date Filtering**: Change the "Analysis Focal Point" in the sidebar to see real-time historical data shifts (Connected to Yahoo Finance History).
- **PDF Export**: Generate professional executive reports directly from the sidebar.
- **Market Trends**: Real-time Google Trends ingestion with automated fallback for stability.

---

## 🛡 Disclaimer & Maintenance
*This system respects robots.txt and includes rate-limiting. For production deployment, use residential proxies for large-scale crawling.*
