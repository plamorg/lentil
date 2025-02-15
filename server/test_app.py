import pytest
from main import app


@pytest.fixture()
def setup_app():
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(setup_app):
    return setup_app.test_client()


@pytest.fixture()
def runner(setup_app):
    return setup_app.test_cli_runner()


def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"
