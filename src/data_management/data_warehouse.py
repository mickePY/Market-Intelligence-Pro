from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.data_management.database_manager import Base

class DataOrigin(enum.Enum):
    SCRAPY = "scrapy"
    API_NEWS = "news_api"
    API_FINANCE = "finance_api"
    API_SOCIAL = "social_api"
    MANUAL = "manual"

class Company(Base):
    __tablename__ = "dim_companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    website = Column(String(500))
    stock_ticker = Column(String(10), nullable=True) # e.g. MSFT
    twitter_handle = Column(String(255), nullable=True)
    linkedin_id = Column(String(255), nullable=True)
    industry = Column(String(255), default="Technology/AI")
    market_cap = Column(Float, nullable=True) # Current
    headquarters = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="company")
    metrics = relationship("FinancialMetric", back_populates="company")
    mentions = relationship("SentimentMention", back_populates="company")

class Product(Base):
    __tablename__ = "dim_products"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_companies.id"))
    name = Column(String(255), index=True)
    category = Column(String(255)) # LLM, Cloud, Hardware, etc.
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    company = relationship("Company", back_populates="products")
    price_history = relationship("PricingRecord", back_populates="product")

class PricingRecord(Base):
    __tablename__ = "fact_pricing"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("dim_products.id"))
    price = Column(Float)
    currency = Column(String(3), default="USD")
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    promotion_details = Column(String(500), nullable=True)
    source = Column(Enum(DataOrigin), default=DataOrigin.SCRAPY)
    
    product = relationship("Product", back_populates="price_history")

class FinancialMetric(Base):
    __tablename__ = "fact_financial_metrics"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_companies.id"))
    date = Column(DateTime, index=True)
    revenue = Column(Float, nullable=True)
    profit_margin = Column(Float, nullable=True)
    growth_rate = Column(Float, nullable=True)
    burn_rate = Column(Float, nullable=True) # Startup specific
    cash_flow = Column(Float, nullable=True)
    period = Column(String(10), default="Q") # Q1, Q2, Annual
    
    company = relationship("Company", back_populates="metrics")

class SentimentMention(Base):
    __tablename__ = "fact_sentiment_mentions"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_companies.id"))
    source_url = Column(String(1000))
    source_type = Column(String(50)) # Twitter, News, Reddit
    sentiment_score = Column(Float) # -1.0 to 1.0
    text_snippet = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    company = relationship("Company", back_populates="mentions")

class InnovationLog(Base):
    __tablename__ = "fact_innovations"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("dim_companies.id"))
    title = Column(String(500))
    innovation_type = Column(String(100)) # Product Launch, Merger, Patent
    impact_score = Column(Integer, default=5) # 1-10
    raw_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", foreign_keys=[company_id])
