from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.base import Base


class Audit(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_email = Column(String(150), nullable=True)

    action = Column(String(100), nullable=False)
    detail = Column(String(255), nullable=True)

    ip_address = Column(String(50), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
