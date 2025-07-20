from app.services.organization_service import get_all_organizations_service


def get_all_organizations_controller():
    return get_all_organizations_service()
