from sqlalchemy import Column,Integer,String,Boolean
from src.database.base import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100), nullable=False)
    path = Column(String(150), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    required_role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)