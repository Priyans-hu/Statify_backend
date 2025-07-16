from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status_code = db.Column(db.Integer, db.ForeignKey('status_master.id'), nullable=False)
    details = db.Column(JSON, nullable=True)  # e.g., {"error": "...", "maintenance_duration": "..."}
