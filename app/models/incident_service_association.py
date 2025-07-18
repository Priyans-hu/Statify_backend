from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class IncidentServiceAssociation(Base):
    __tablename__ = "incident_services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
