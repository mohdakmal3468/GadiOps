from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Target Roles from Hackathon Prompt: 'Fleet Manager', 'Driver', 'Financial Analyst', 'Safety Officer'
    role = Column(String, default="Driver", nullable=False)