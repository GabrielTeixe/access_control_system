from sqlalchemy import Integer,Column,String,DateTime,ForeignKey
from datetime import datetime
from src.database.base import Base

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer,primary_key=True,index=True)

    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    username = Column(String, nullable=False)

    status = Column(String,nullable=False) #Allowed/ Denied
    reason = Column(String,nullable=False)

    timestamp = Column(DateTime,default=datetime.utcnow)