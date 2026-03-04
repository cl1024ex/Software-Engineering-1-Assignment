import pytest
from application import app, db
from application.models import User, Admin, Attractions, Reviews

import warnings

# Ignore all DeprecationWarnings in this test file
warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["MONGODB_SETTINGS"] = {
        "db": "test_database"
    }

    with app.test_client() as client:
        with app.app_context():
            # Clean database before each test
            User.drop_collection()
            Admin.drop_collection()
            Attractions.drop_collection()
            Reviews.drop_collection()
        yield client
