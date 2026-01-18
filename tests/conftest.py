import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from main import app


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_organization(db_session):
    """Create a sample organization for testing."""
    from app.models.organizations import Organizations
    org = Organizations(name="Test Organization", slug="test-org")
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)
    return org


@pytest.fixture
def sample_user(db_session, sample_organization):
    """Create a sample admin user for testing."""
    from app.models.users import Users
    from app.utils.auth_util import get_password_hash

    user = Users(
        username="testadmin",
        password=get_password_hash("testpassword"),
        org_id=sample_organization.id,
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(sample_user):
    """Generate an auth token for the sample user."""
    from app.utils.auth_util import create_access_token
    token = create_access_token(data={"sub": sample_user.username})
    return token


@pytest.fixture
def auth_headers(auth_token, sample_organization):
    """Return headers with authentication token and org."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "X-Org-Slug": sample_organization.slug
    }
