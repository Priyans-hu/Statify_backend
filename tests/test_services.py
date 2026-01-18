import pytest


class TestServiceEndpoints:
    """Test cases for service endpoints."""

    def test_get_services_empty(self, client, auth_headers):
        """Test getting services when none exist."""
        response = client.get("/services", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert data["items"] == []
        assert data["total"] == 0

    def test_get_services_with_pagination(self, client, auth_headers):
        """Test pagination parameters."""
        response = client.get("/services?page=1&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "page_size" in data
        assert "total_pages" in data
        assert data["page"] == 1
        assert data["page_size"] == 10

    def test_create_service(self, client, auth_headers):
        """Test creating a new service."""
        service_data = {
            "service_name": "Test Service",
            "status_code": 1
        }
        response = client.post("/services", json=service_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["service_name"] == "Test Service"
        assert data["status_code"] == 1

    def test_create_service_missing_fields(self, client, auth_headers):
        """Test creating a service with missing required fields."""
        service_data = {"service_name": "Test Service"}
        response = client.post("/services", json=service_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    def test_update_service_status(self, client, auth_headers, db_session):
        """Test updating a service status."""
        # First create a service
        from app.models.services import Services
        service = Services(
            service_name="Test Service",
            status_code=1,
            org_id=1
        )
        db_session.add(service)
        db_session.commit()
        db_session.refresh(service)

        # Update status
        response = client.patch(
            f"/services/{service.id}/status",
            json={"status_code": 2},
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_delete_service(self, client, auth_headers, db_session):
        """Test deleting a service."""
        from app.models.services import Services
        service = Services(
            service_name="Test Service",
            status_code=1,
            org_id=1
        )
        db_session.add(service)
        db_session.commit()
        db_session.refresh(service)

        response = client.delete(f"/services/{service.id}", headers=auth_headers)
        assert response.status_code == 204

    def test_delete_nonexistent_service(self, client, auth_headers):
        """Test deleting a service that doesn't exist."""
        response = client.delete("/services/99999", headers=auth_headers)
        assert response.status_code == 404


class TestServicePagination:
    """Test pagination functionality."""

    def test_pagination_defaults(self, client, auth_headers):
        """Test default pagination values."""
        response = client.get("/services", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 20

    def test_pagination_custom_values(self, client, auth_headers):
        """Test custom pagination values."""
        response = client.get("/services?page=2&page_size=5", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert data["page_size"] == 5

    def test_pagination_invalid_page(self, client, auth_headers):
        """Test invalid page number."""
        response = client.get("/services?page=0", headers=auth_headers)
        assert response.status_code == 422  # Validation error for page < 1

    def test_pagination_max_page_size(self, client, auth_headers):
        """Test page size exceeding maximum."""
        response = client.get("/services?page_size=200", headers=auth_headers)
        assert response.status_code == 422  # Validation error for page_size > 100
