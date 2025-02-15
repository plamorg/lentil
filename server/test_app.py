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


def test_generate_success(client):
    """
    Test that a valid POST request to /generate returns a 200 status and the expected JSON structure.
    """
    data = {
        "stdout": "Compilation successful",
        "stderr": "",
        "files": [
            {"path": "file1.py", "content": "print('Hello World')"},
            {"path": "file2.txt", "content": "Just some text."},
        ],
    }
    response = client.post("/generate", json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None


def test_generate_failure_no_context(client):
    """
    Test that sending an empty JSON (no context) fails with a 400 status code.
    """
    response = client.post("/generate", json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data is not None
    assert "error" in json_data
    assert json_data["error"] == "No context provided"
