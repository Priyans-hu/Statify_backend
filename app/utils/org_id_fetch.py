from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.organizations import Organizations

async def resolve_org_slug(org_slug):
        db: Session = SessionLocal()
        try:
            org = db.query(Organizations).filter_by(slug=org_slug).first()
            if org:
                return org
            else:
                raise ValueError("Organization not found")
        finally:
            db.close()