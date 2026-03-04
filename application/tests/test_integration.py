
def test_register_and_login(client):
    """
    This test verifies the user registration and login functionality of the
    application. It ensures that a new user can successfully register and
    then log in with the correct credentials.
    """
    response = client.post("/register", data={
        "email": "test@test.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }, follow_redirects=True)

    assert b"Home Page" in response.data

    response = client.post("/login", data={
        "email": "test@test.com",
        "password": "password123"
    }, follow_redirects=True)

    assert b"Home Page" in response.data


def test_add_attraction(client):
    """
    This test verifies the functionality of adding a new attraction to the
    application. It ensures that a user can successfully submit an attract
    ion for approval and that the appropriate success message is displayed.
    """
    from application.models import User
    user = User(user_id=1, email="u@test.com", first_name="U", last_name="Test")
    user.set_password("pass")
    user.save()

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "U"

    response = client.post("/add_attraction", data={
        "attraction_name": "Museum",
        "description": "Nice place",
        "location": "City"
    }, follow_redirects=True)

    assert b"pending approval" in response.data


def test_add_review(client):
    """
    This test verifies the functionality of adding a review for an attraction
    in the application. It ensures that a user can successfully submit a review
    for an existing attraction and that the appropriate success message is
    displayed.
    """
    from application.models import Attractions

    attraction = Attractions(
        attractionID="1",
        name="Park",
        description="Green",
        location="Town",
        status="approved",
        created_by=1
    )
    attraction.save()

    response = client.post("/add_review/1", data={
        "name": "Guest",
        "rating": "5",
        "review": "Great!"
    }, follow_redirects=True)

    assert b"Review added successfully" in response.data
