from app import db, bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # "admin" or "viewer"
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=True, default=None)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
