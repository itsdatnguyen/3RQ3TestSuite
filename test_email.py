def test_user_is_guest():
    user = {
        "guest": True,
    }

    assert user["guest"] == True
