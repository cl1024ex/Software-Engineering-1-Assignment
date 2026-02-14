from application.models import Reviews
from application.route import get_next_available_review_id


def test_next_review_id_empty_db():
    """
    This test verifies that when there are no reviews in the database,
    sp next available review ID starts at 1. It ensures that the function
    correctly identifies the starting point for review IDs.
    """
    Reviews.drop_collection()
    next_id = get_next_available_review_id()
    assert next_id == 1


def test_next_review_id_with_existing():
    """
    This test checks that the get_next_available_review_id function correctly
    identifies the next review ID when there are existing reviews in the 
    database. It ensures that the function can handle a populated database 
    and returns the correct next ID.
    """
    Reviews.objects.delete()
    Reviews(reviewID=1, attractionID=1, first_name="A", rating=5, review="Good", reported=False).save()
    Reviews(reviewID=2, attractionID=1, first_name="B", rating=4, review="Nice", reported=False).save()

    next_id = get_next_available_review_id()
    assert next_id == 3


def test_next_review_id_gap():
    """
    This test verifies that the get_next_available_review_id function
    correctly identifies the next review ID when there is a gap in the
    existing review IDs. It ensures that the function can handle
    non-sequential IDs and returns the correct next ID, which should
    be the smallest available ID that is not currently in use such as
    when review ID 2 is missing, the next available ID should be 2 instead of 3.

    """
    Reviews.objects.delete()
    Reviews(reviewID=1, attractionID=1, first_name="A", rating=5, review="Good", reported=False).save()
    Reviews(reviewID=3, attractionID=1, first_name="B", rating=4, review="Nice", reported=False).save()

    next_id = get_next_available_review_id()
    assert next_id == 2
