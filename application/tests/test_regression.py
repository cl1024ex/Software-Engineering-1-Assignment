
def test_make_admin_requires_admin(client):
    """
    This test verifies that only admin users can access the make_admin route
    to promote other users to admin status.
    It ensures that non-admin users are correctly prevented from accessing
    this functionality and receive an appropriate error message.
    """
    response = client.post("/make_admin/1", follow_redirects=True)
    assert b"not authorised" in response.data


def test_cannot_delete_approved_attraction(client):
    """
    This test verifies that an approved attraction cannot be deleted from the
    application. It ensures that the delete_attraction route correctly
    prevents deletion of attractions that have already been approved and that
    an appropriate error message is displayed to the user.
    """
    from application.models import Attractions

    attraction = Attractions(
        attractionID="1",
        name="Castle",
        description="Old",
        location="Hill",
        status="approved",
        created_by=1
    )
    attraction.save()

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/delete_attraction/1", follow_redirects=True)

    assert b"only delete pending attractions" in response.data


def test_report_review_sets_flag(client):
    """
    This test verifies that when a user reports a review, the reported flag
    for that review is correctly set to True in the database. It ensures
    that the report_review route functions as intended, allowing users to
    report inappropriate reviews and that the system properly updates the
    review's status to reflect that it has been reported.
    """
    from application.models import Reviews

    review = Reviews(
        reviewID=1,
        attractionID=1,
        first_name="A",
        rating=5,
        review="Nice",
        reported=False
    )
    review.save()

    client.post("/report_review/1", follow_redirects=True)

    updated = Reviews.objects(reviewID=1).first()
    assert updated.reported is True
