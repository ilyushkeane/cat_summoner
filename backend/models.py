from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    user_uuid = Column(String, primary_key=True, index=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    referrer = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    is_mobile = Column(Boolean, default=False)
    
    # Связи для JOIN-ов в коде Python
    summons = relationship("Summon", back_populates="owner")
    ui_events = relationship("UIEvent", back_populates="owner")

class Summon(Base):
    __tablename__ = "summons"
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String, ForeignKey("users.user_uuid"))
    session_id = Column(String) # Группировка кликов за один заход
    cat_title = Column(String)
    rarity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="summons")

class UIEvent(Base):
    __tablename__ = "ui_events"
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String, ForeignKey("users.user_uuid"))
    session_id = Column(String)
    event_name = Column(String) # 'open_info', 'close_info'
    timestamp = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="ui_events")
    
class MetricaLog(Base):
    __tablename__ = "metrica_logs"
    
    visit_id = Column(String, primary_key=True) # ym:s:visitID
    user_uuid = Column(String, index=True)      # Наш userID из параметров
    client_id = Column(String)                  # Внутренний ID Яндекса
    
    # Время
    start_time = Column(DateTime)               # ym:s:dateTime
    visit_duration = Column(Integer)            # Длительность в сек.
    
    # География
    country = Column(String)
    region = Column(String)
    city = Column(String)
    
    # Техника
    device = Column(String)                     # Mobile / Desktop / Tablet
    os = Column(String)                         # iOS / Android / Windows
    browser = Column(String)
    
    # Маркетинг
    source = Column(String)                     # Источник (ad / search / social)
    utm_source = Column(String, nullable=True)
    utm_medium = Column(String, nullable=True)
    utm_campaign = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    
    # Поведение
    page_views = Column(Integer)
    is_bounce = Column(Boolean)                 # Отказ