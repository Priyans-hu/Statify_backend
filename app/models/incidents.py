from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Incidents(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    status = Column(String(50), nullable=False, default="investigating")  # investigating, identified, monitoring, resolved
    is_scheduled = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
