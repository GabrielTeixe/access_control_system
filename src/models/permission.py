from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base
from src.models.role_permission import role_permissions


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission(name='{self.name}')>"
