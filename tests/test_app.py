import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "healthy"}


def test_get_tasks_returns_initial_list(client):
    res = client.get("/tasks")
    assert res.status_code == 200
    body = res.get_json()
    assert isinstance(body, list)
    assert len(body) > 0


def test_create_task_success(client):
    res = client.post("/tasks", json={"title": "Tugas baru"})
    assert res.status_code == 201
    body = res.get_json()
    assert body["title"] == "Tugas baru"
    assert body["done"] is False


def test_create_task_without_title_returns_400(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400


def test_get_task_not_found_returns_404(client):
    res = client.get("/tasks/9999")
    assert res.status_code == 404


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Akan diupdate"}).get_json()
    res = client.put(f"/tasks/{created['id']}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Akan dihapus"}).get_json()
    res = client.delete(f"/tasks/{created['id']}")
    assert res.status_code == 204
