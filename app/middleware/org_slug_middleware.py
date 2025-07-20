from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.utils.org_id_fetch import resolve_org_slug


class OrgSlugResolverMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        org_slug = request.query_params.get("org")

        if org_slug:
            org = await resolve_org_slug(org_slug)
            if org:
                request.state.org_id = org.id

        response: Response = await call_next(request)
        return response
