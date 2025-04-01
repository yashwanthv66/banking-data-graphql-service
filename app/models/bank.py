from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    branches = relationship("Branch", back_populates="bank")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    ifsc = Column(String, unique=True, index=True)
    branch = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    district = Column(String)
    state = Column(String)
    bank_id = Column(Integer, ForeignKey("banks.id"))
    
    bank = relationship("Bank", back_populates="branches")