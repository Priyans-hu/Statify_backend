from sqlalchemy import Column, Integer, String

from app.database import Base


class StatusMaster(Base):
    __tablename__ = "status_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(100), nullable=False)
