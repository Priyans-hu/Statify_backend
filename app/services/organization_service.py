from app.models.organizations import Organizations
from app.schemas.organization_schema import OrganizationOut
from app.services.auth_service import db_session


def get_all_organizations_service() -> list[OrganizationOut]:
    with db_session() as db:
        orgs = db.query(Organizations).all()
        return [OrganizationOut.from_orm(org) for org in orgs]
