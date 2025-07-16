from app import db

class StatusMaster(db.Model):
    __tablename__ = 'status_master'

    id = db.Column(db.Integer, primary_key=True)  # Status code
    status = db.Column(db.String(100), nullable=False)
