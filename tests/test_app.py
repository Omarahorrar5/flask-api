from app.main import create_app

def test_health():
    client = create_app().test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

def test_greet():
    client = create_app().test_client()
    resp = client.get("/api/greet/Sam")
    assert resp.get_json() == {"message": "Hello, Sam!"}