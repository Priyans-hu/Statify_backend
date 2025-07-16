from app import db
from sqlalchemy.sql import func

class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(255), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    status_code = db.Column(db.Integer, db.ForeignKey('status_master.id'), nullable=False)
    domain = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = db.Column(db.Boolean, default=False)
