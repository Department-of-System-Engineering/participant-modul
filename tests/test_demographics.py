# Tests for the demographics router.
# The database is mocked so no real PostgreSQL connection is needed.
# Each test uses the mock_db fixture from conftest.py.

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_demographics_by_group(client, mock_db):
    mock_db.fetchall.return_value = []
    response = client.get("/demographics/?group_ref=ETH-2026-001")
    assert response.status_code == 200
    assert response.json()["group_ref"] == "ETH-2026-001"
    assert isinstance(response.json()["demographics"], list)

def test_get_demographic_by_id_not_found(client, mock_db):
    mock_db.fetchone.return_value = None
    response = client.get("/demographics/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_start_demographics(client, mock_db):
    mock_db.fetchone.return_value = {
        "id": "d5e0c3b2-8a41-4f6e-9d27-1c5b0a7e3f98"
    }
    response = client.post("/demographics/", json={
        "participant_pseudonym": "teszt-alma-korte",
        "session_ref": "S-001",
        "group_ref": "ETH-2026-001",
        "language": "hu"
    })
    assert response.status_code == 201
    assert "demographics_id" in response.json()
    assert "display_url" in response.json()