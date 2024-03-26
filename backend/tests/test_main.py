def test_get_message():
    from app.main import get_message
    assert get_message() == {"message": "Hello World"}
