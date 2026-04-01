from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Summon(Base):
    __tablename__ = "summons"
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String)
    cat_title = Column(String)
    rarity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)