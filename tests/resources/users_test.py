import falcon
from falcon import testing
from mock import call, MagicMock, mock_open
import pytest

from main import App


@pytest.fixture
def mock_store():
    return MagicMock()

@pytest.fixture
def client(mock_store):
    api = App(mock_store)
    return testing.TestClient(api)


def test_user_collection(client):
    doc= {
        "meta": {
            "code": 200,
            "message": "OK"
        },
        "data": {
            "balance": 2500,
            "details": None,
            "username": "jesus",
            "modified": 1560382164,
            "email": "jesus@resev.com",
            "created": 1560382164,
            "user_id": 2,
            "token": "gAAAAABdAYrUs9d181CPHUECFKm5VQQQIbaVq_Ss6oAiZT4VjdJQl_VB6nfyLBqX2uAb94kN5TKEkcN_eBj2yI1lEqwFpJ-KFA=="
        }
    }
    response = client.simulate_post(
        '/resev/v1/users', json={
	"username": "jesus",
	"email": "jesus@resev.com",
	"password": "dev_123456",
	"balance": 2500.0
})
    assert response.status == falcon.HTTP_200
