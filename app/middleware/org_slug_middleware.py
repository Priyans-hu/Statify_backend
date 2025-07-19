from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.database import SessionLocal
from app.models.organizations import Organizations


class OrgSlugResolverMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path_parts = request.url.path.strip("/").split("/")

        # Assume URL pattern: /{org_slug}/...
        if len(path_parts) > 0:
            org_slug = path_parts[0]
            db: Session = SessionLocal()

            try:
                org = db.query(Organizations).filter_by(slug=org_slug).first()
                if org:
                    request.state.org_id = org.id

            finally:
                db.close()

        response: Response = await call_next(request)
        return response
