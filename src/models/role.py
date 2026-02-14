from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.models.role_permission import role_permissions


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)

    users = relationship("User", back_populates="role")

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
