import pytest

from application import create_app
from fastapi.testclient import TestClient

# TODO fix to prevent db creation
@pytest.mark.skip
def test_home():
    app = create_app()
    with TestClient(app) as test_client:
        response = test_client.get("/")
        assert response.json().get("message") == "Welcome to the Piazza Project"
        assert response.status_code == 200