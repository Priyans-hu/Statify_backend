from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

from app.database import Base


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status_code = Column(Integer, ForeignKey("status_master.id"), nullable=False)
    details = Column(JSON, nullable=True)
